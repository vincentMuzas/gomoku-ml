#!/bin/python3

from game_engine import game_engine
from QLock import QLock
from time import sleep

import socketserver, socket, threading, time

class TCPRequestHandler(socketserver.BaseRequestHandler):

    clients = []
    observers = []

    def setup(self):
        if (len(self.clients) == 2):
            self.observers.append(self.request)
        else:
            self.clients.append(self.request)
        


    def finish(self):
        try:
            self.clients.remove(self.request)
            if (len(self.clients)):
                self.clients[0].send("opponent left".encode())
        except:
            self.observers.remove(self.request)
        
        global game
        if (not len(self.clients)):
            game = game_engine()
        for observer in self.observers:
            observer.send("reset\n".encode())

    def handle(self):
        global game, lock, barrier


        try:
            index = self.clients.index(self.request)
        except:
            string = ""
            for line in game.get_board():
                for element in line:
                    string += str(element)
                string += '\n'
            self.request.send(string.encode())
            #noodle code
            while (1):
                if self.request.recv(1024).decode() == "":
                    return


        barrier.wait()

        self.request.send(str(index).encode())

        aquired = True
        if (index == 0):
            lock.acquire()
        else:
            while ( not lock.locked() ):
                pass
            lock.acquire()
        while 1:
            if (not aquired):
                while ( not lock.locked() ):
                    pass
                lock.acquire()
                aquired = True
            data = self.request.recv(1024).decode()
            print("data received:", data)
            if (not data):
                lock.release()
                break
            data = data.splitlines()[-1]
            if (data == "map"):
                string = ""
                for line in game.get_board():
                    for element in line:
                        string += str(element)
                    string += '\n'
                self.request.send(string.encode())
            elif (len(data.split(' ')) == 2):
                x, y =  data.split(' ')
                result = game.move(int(x), int(y))
                if (len(self.clients) > 1):
                    self.clients[not index].send((data + '\n').encode())
                print("player %d played %s %s" % (index, x, y))

                #envoi du move aux observers
                for observer in self.observers:
                    observer.send(("%d %s %s\n" % (index, x, y)).encode())


                self.request.send("ok\n".encode())
                if ("win the game" in result or "draw" in result):
                    self.clients[not index].send((result + '\n').encode())
                    self.clients[    index].send((result + '\n').encode())
                lock.release()
                aquired = False
            else:
                self.request.send("invalid\n".encode())


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

if __name__ == "__main__":

    HOST, PORT = "localhost", 0
    server = ThreadedTCPServer((HOST, PORT), TCPRequestHandler)

    game = game_engine()

    lock = QLock()
    barrier = threading.Barrier(2)

    with server:
        ip, port = server.server_address
        server_thread = threading.Thread(target=server.serve_forever)

        server_thread.daemon = True
        server_thread.start()

        print("Server running in port: %s:%d" % (ip, port))

        server.serve_forever()
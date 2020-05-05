#!/bin/python3

from game_engine import game_engine
from QLock import QLock

import socketserver, socket, threading, time

class TCPRequestHandler(socketserver.BaseRequestHandler):

    clients = []

    def setup(self):
        if (len(self.clients) < 2):
            self.clients.append(self.request)
        


    def finish(self):
        try:
            self.clients.remove(self.request)
        except:
            return
        if (len(self.clients)):
            self.clients[0].send("opponent left".encode())

    def handle(self):
        try:
            index = self.clients.index(self.request)
        except:
            return

        global game, lock

        self.request.send(str(index).encode())

        aquired = False
        while 1:
            if (not aquired):
                lock.acquire()
                aquired = True
            data = self.request.recv(1024).decode()
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

##
## Exemple de connection client
##
def client(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.connect((ip, port))
        sock.sendall(bytes(message, 'ascii'))
        response = str(sock.recv(1024), 'ascii')
        print("Received: {}".format(response))

if __name__ == "__main__":

    game = game_engine()

    lock = QLock()

    HOST, PORT = "localhost", 0

    server = ThreadedTCPServer((HOST, PORT), TCPRequestHandler)
    with server:
        ip, port = server.server_address
        server_thread = threading.Thread(target=server.serve_forever)

        server_thread.daemon = True
        server_thread.start()

        print("Server running in port: %s:%d" % (ip, port))

        server.serve_forever()
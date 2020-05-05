#!/usr/bin/python3.7

import tkinter as tk
from game_engine import game_engine
import sys, socket, threading


def reset_aspect_ratio(event):
	width = int((board.winfo_width() + board.winfo_height()) / 2)
	screen.geometry("{}x{}".format(width, width))
	global object_size
	object_size = width / 21
	for y in range(21):
		for x in range(21):
			x0 = x * object_size
			y0 = y * object_size
			x1 = x0 + object_size
			y1 = y0 + object_size
			board.coords(widgets[y * 21 + x], x0, y0, x1, y1)
	
	for pion in circles:
		obj = board.gettags(pion)
		x0 = int(obj[0]) * object_size
		y0 = int(obj[1]) * object_size
		x1 = x0 + object_size
		y1 = y0 + object_size
		board.coords(pion, x0, y0, x1, y1)

def exit_program(event):
	screen.destroy()

def get_item(event):
	posx = int(event.x / object_size)
	posy = int(event.y / object_size)
	if (posx > 21 or posy > 21):
		return
	index = posy * 21 + posx
	global circles, last_move
	if (board.gettags(widgets[index])[0] != "played"):
		sock.sendall(bytes("%d %d\n" % (posx, posy), 'ascii'))
		last_move = (posx, posy)


def ListenSocket(socket, color):
	global last_move, circles
	me = ("white", "black")[color == 1]
	oponnent = ("black", "white")[color == 1]
	print("in listensocket")
	while (1):
		line = socket.recv(1024).decode()
		if (line == ""):
			break
		line = line.strip()
		print(line)
		if (line == "ok"):
			posx, posy = last_move
		else:
			posx, posy = line.split(' ')
			posx, posy = int(posx), int(posy)
		index = posy * 21 + posx
		board.itemconfig(widgets[index], tags="played")
		draw_x = posx * object_size
		draw_y = posy * object_size
		circles.append(
			board.create_oval(draw_x, draw_y, draw_x + object_size, draw_y + object_size,
			fill=(me, oponnent)[line == "ok"], tags=[posx, posy]))
	print("out")

	

if __name__ == "__main__":

	## connection au serveur
	if (len(sys.argv) != 3):
		sys.exit(84)
	IP = sys.argv[1]
	PORT = int(sys.argv[2])
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((IP, PORT))
	response = str(sock.recv(1), 'ascii')
	if (not response):
		sys.exit(84)

	color = int(response) + 1
	last_move = None

	# creation de fenetre
	screen = tk.Tk()
	screen.title("PLAYER IS COLOR %s" % (("WHITE", "BLACK")[color != 1]))
	screen.bind('<Control-c>', exit_program)
	screen.bind('r', reset_aspect_ratio)

	#create the canvas
	board = tk.Canvas(screen, width=500, height=500, background="#CB945C")
	board.pack(side="left", fill="both", expand=True)


	screen.update_idletasks()
	widgets = []
	circles = []
	object_size = board.winfo_height() / 21
	for y in range(21):
		for x in range(21):
			x0 = x * object_size
			y0 = y * object_size
			x1 = x0 + object_size
			y1 = y0 + object_size
			widgets.append(board.create_rectangle(x0, y0, x1, y1, tags={"x": x, "y": y}))

	board.bind("<ButtonPress-1>", get_item)

	threading.Thread(target=ListenSocket, args=(sock, color)).start()

	screen.mainloop()

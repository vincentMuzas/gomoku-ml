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

def ListenSocket(socket):
	global circles
	while (1):
		line = socket.recv(1024).decode()
		if (line == ""):
			break
		line = line.strip()
		player, posx, posy = line.split(' ')
		posx, posy = int(posx), int(posy)
		draw_x = posx * object_size
		draw_y = posy * object_size
		circles.append(
			board.create_oval(draw_x, draw_y, draw_x + object_size, draw_y + object_size,
			fill=("white", "black")[int(player)], tags=[posx, posy])
		)

	

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
	screen.title("observer")
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

	lines = sock.recv(1024).decode().splitlines()
	for posy, line in enumerate(lines):
		for posx, case in enumerate(line):
			if (case == "0"):
				continue
			draw_x = posx * object_size
			draw_y = posy * object_size
			circles.append(
				board.create_oval(draw_x, draw_y, draw_x + object_size, draw_y + object_size,
				fill=("white", "black")[int(case) - 1], tags=[posx, posy])
			)




	threading.Thread(target=ListenSocket, args=[sock]).start()

	screen.mainloop()

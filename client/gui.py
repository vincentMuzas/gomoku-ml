#!/usr/bin/python3.7

import tkinter as tk
from game_engine import game_engine
from PIL import Image, ImageTk


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

def exit_program(event):
	screen.destroy()

def get_item(event):
	posx = int(event.x / object_size)
	posy = int(event.y / object_size)
	if (posx > 21 or posy > 21):
		return
	index = posy * 21 + posx
	print(posx, posy)
	try:
		board.itemconfig(widgets[index], fill='black')
	except:
		pass

	

if __name__ == "__main__":
	engine = game_engine()
	screen = tk.Tk()
	screen.title("Gomoku UI")
	screen.bind('<Control-c>', exit_program)
	screen.bind('r', reset_aspect_ratio)

	#create the canvas
	board = tk.Canvas(screen, width=500, height=500, background="#CB945C")
	board.pack(side="left", fill="both", expand=True)


	screen.update_idletasks()
	widgets = []
	object_size = board.winfo_height() / 21
	for y in range(21):
		for x in range(21):
			x0 = x * object_size
			y0 = y * object_size
			x1 = x0 + object_size
			y1 = y0 + object_size
			widgets.append(board.create_rectangle(x0, y0, x1, y1, tags={"x": x, "y": y}))

	board.bind("<ButtonPress-1>", get_item)

	screen.mainloop()
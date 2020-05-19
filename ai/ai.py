#!/usr/bin/python3.7

import socket
import random
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean, median
from collections import Counter
import sys

LR = 1e-3
goal_steps = 50
score_requirement = 50
initial_games = 10000

IP, PORT = sys.argv[1:3]
PORT = int(PORT)

def random_games_data():

	lauched = False

	for episode in range(initial_games):
		sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock1.connect((IP, PORT))
		sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock2.connect((IP, PORT))

		if (not lauched):
			input("press <enter> to start generating random data\n")
			lauched = True
		
		map = [[0 for x in range(21)] for y in range(21)]

		response1 = str(sock1.recv(1), 'ascii')
		response2 = str(sock2.recv(1), 'ascii')

		if (response1 == "" or response2 == ""):
			print("server not found")
			sys.exit()
		
		player1 = int(response1) + 1
		player2 = int(response2) + 1

		if (player1 in [1, 2] and player2 in [1, 2] and player1 != player2):
			pass
		else:
			print("error on player")
			sys.exit()

		turn = 0
		for _ in range(goal_steps):

			while (1):
				x = random.randrange(0, 20)
				y = random.randrange(0, 20)
				if (map[y][x] != 0):
					continue
			map[y][x] = (turn % 2) + 1
			(sock1, sock2)[turn % 2].send("{} {}\n".format(x, y).encode())

			rep = (sock1, sock2)[turn % 2].recv(100)
			if ("ok" not in rep):
				sock1.close()
				sock2.close()
				break

			rep = (sock1, sock2)[not (turn % 2)].recv(100)
			try:
				otherx, othery = rep.split(' ')
			except:
				sock1.close()
				sock2.close()
			if (int(otherx) != x and int(othery) != y):
				sock1.close()
				sock2.close()
				break
			turn += 1

random_games_data()
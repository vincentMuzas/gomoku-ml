#!/usr/bin/python3.7

import socket
import random
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean, median
from collections import Counter
import numpy as np
import sys

LR = 1e-3
goal_steps = 50
score_requirement = 50
initial_games = 10000

IP, PORT = sys.argv[1:3]
PORT = int(PORT)

def random_games_data():

	lauched = False
	training_data = [[], []]
	scores = [[], []]
	accepted_scores = [[], []]

	for episode in range(initial_games):
		sock1 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock1.connect((IP, PORT))
		sock2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock2.connect((IP, PORT))

		score = [0, 0]
		game_memory = [[], []]
		prev_observation = [[], []]

		if (not lauched):
			input("press <enter> to start generating random data\n")
			lauched = True
		
		map = [[0 for x in range(21)] for y in range(21)]

		response1 = str(sock1.recv(10), 'ascii')
		response2 = str(sock2.recv(10), 'ascii')

		if (response1 == "" or response2 == ""):
			print("server not found")
			sys.exit()
		
		player1 = int(response1) + 1
		player2 = int(response2) + 1

		if (player1 in [1, 2] and player2 in [1, 2] and player1 != player2):
			pass
		else:
			print("error on player", player1, player2)
			sys.exit()

		turn = 0
		for _ in range(goal_steps):

			while (1):
				x = random.randrange(0, 20)
				y = random.randrange(0, 20)
				if (map[y][x] == 0):
					break
			map[y][x] = (turn % 2) + 1
			(sock1, sock2)[turn % 2].send("{} {}\n".format(x, y).encode())

			print("turn", turn)
			rep = (sock1, sock2)[turn % 2].recv(100).decode()
			print(rep)
			if ("win" in rep):
				score[turn % 2] = score_requirement
			if ("ok" not in rep):
				sock1.close()
				sock2.close()
				break

			rep = (sock1, sock2)[not (turn % 2)].recv(100).decode()
			try:
				otherx, othery = rep.split(' ')
			except:
				sock1.close()
				sock2.close()
				break
			if (int(otherx) != x and int(othery) != y):
				sock1.close()
				sock2.close()
				break
			action[turn % 2] = [x, y]
			if len(prev_observation) > 0:
				game_memory[turn % 2].append([prev_observation, action])
			prev_observation[turn % 2] = map
			score[turn % 2] += 1
			turn += 1

		for i in range(2):
			if (score[i] >= score_requirement):
				accepted_score[i].append(score)
				for data in game_memory[i]:
					training_data[i].append(data)

		scores[0].append(score[0])
		scores[1].append(score[1])
	
	training_data_save[0] = np.array(training_data[0])
	training_data_save[1] = np.array(training_data[1])

	np.save("saved_0.npy", training_data_save[0])
	np.save("saved_1.npy", training_data_save[1])

	print('average accepted score:', mean(accepted_scores[0]))
	print('median accepted score:', median(accepted_scores[0]))
	print(Counter(accepted_scores[0]))

	return (training_data[0])

random_games_data()


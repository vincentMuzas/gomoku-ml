#!/usr/bin/python3.7

import random
import socket
import tflearn
from tflearn.layers.core import input_data, dropout, fully_connected
from tflearn.layers.estimator import regression
from statistics import mean, median
from collections import Counter
import numpy as np
from game_engine import game_engine

LR = 1e-3
goal_steps = 441
score_requirement = 1
initial_games = 10000

IP, PORT = sys.argv[1:3]
PORT = int(PORT)

def random_games_data():

	lauched = False
	training_data = [[], []]
	scores = [[], []]
	accepted_scores = [[], []]

	for episode in range(initial_games):
		## NOUVELLE PARTIE
		with game_engine() as engine:

			score = [0, 0]
			game_memory = [[], []]
			prev_observation = [[], []]

			if (not lauched):
				input("press <enter> to start generating random data\n")
				lauched = True

			map = [[0 for x in range(21)] for y in range(21)]

			# BOUCLE DES TOURS
			for turn in range(goal_steps):
				player = turn % 2

				x = y = 10
				while (engine.map()[y][x] != 0):
					x = random.randrange(0, 21)
					y = random.randrange(0, 21)
				
				try:
					result = engine.move(y, x)
				except:
					break
				if ("win the game" in result):
					player = int(result.split()[1])
					score[player] = goal_steps - turn
					score[not player] = 0
					break
				if (result is "draw"):
					score = [0, 0]
					break
					

#
#			response1 = str(sock1.recv(10), 'ascii')
#			response2 = str(sock2.recv(10), 'ascii')
#
#			if (response1 == "" or response2 == ""):
#				print("server not found")
#				sys.exit()
#			
#			while 1:
#				try:
#					player1 = int(response1) + 1
#					break
#				except:
#					pass
#			while 2:
#				try:
#					player2 = int(response2) + 1
#					break
#				except:
#					pass
#
#			if (player1 in [1, 2] and player2 in [1, 2] and player1 != player2):
#				pass
#			else:
#				print("error on player", player1, player2)
#				sys.exit()
#
#			turn = 0
#			for _ in range(goal_steps):
#
#				while (1):
#					x = random.randrange(0, 20)
#					y = random.randrange(0, 20)
#					if (map[y][x] == 0):
#						break
#				map[y][x] = (turn % 2) + 1
#				(sock1, sock2)[turn % 2].sendall(bytes("%d %d\n" % (x, y), 'ascii'))
#
#				print("turn %d: %d %d" % (turn, x, y))
#				rep = (sock1, sock2)[turn % 2].recv(100).decode()
#				print(rep)
#				if ("player %d win" % (player1, player2)[turn % 2] in rep):
#					score[turn % 2] = 441 - turn
#					break
#				if ("ok" not in rep):
#					sock1.close()
#					sock2.close()
#					break
#
#				rep = (sock1, sock2)[not (turn % 2)].recv(100).decode()
#				try:
#					otherx, othery = rep.split(' ')
#					int(otherx), int(othery)
#				except:
#					sock1.close()
#					sock2.close()
#					break
#				if (int(otherx) != x and int(othery) != y):
#					sock1.close()
#					sock2.close()
#					break
#				action = [x, y]
#				if len(prev_observation) > 0:
#					game_memory[turn % 2].append([prev_observation, action])
#				prev_observation[turn % 2] = map
#				score[turn % 2] = 0
#				turn += 1
#
#			for i in range(2):
#				if (score[i] >= score_requirement):
#					accepted_score[i].append(score)
#					for data in game_memory[i]:
#						training_data[i].append(data)
#
#			scores[0].append(score[0])
#			scores[1].append(score[1])
#	
	training_data_save[0] = np.array(training_data[0])
	training_data_save[1] = np.array(training_data[1])

	np.save("saved_0.npy", training_data_save[0])
	np.save("saved_1.npy", training_data_save[1])

	print('average accepted score:', mean(accepted_scores[0]))
	print('median accepted score:', median(accepted_scores[0]))
	print(Counter(accepted_scores[0]))

	return (training_data[0])

random_games_data()


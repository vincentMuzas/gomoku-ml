#!/usr/bin/python3.7

import random
import socket
from keras.engine.topology import Input
from keras.engine.training import Model
from keras.layers import add
from keras.layers.convolutional import Conv2D
from keras.layers.core import Activation, Dense, Flatten
from keras.layers.normalization import BatchNormalization
from keras.regularizers import l2
from keras.optimizers import SGD
from statistics import mean, median
from collections import Counter
import numpy as np
from game_engine import game_engine


# Learning rate
LR = 1e-3

board_size = 21

# nombre de tours max par parties
goal_steps = pow(board_size, 2)

# score requis pour enregistrer la partie (1 = gagnant, 0 = perdant ou égalitée, max = goal_steps)
score_requirement = 1

# nombre de games a générer
initial_games = 100

white_stack = [[[False for _ in range(board_size)] for _ in range(board_size)] for _ in range(8)]
black_stack = [[[False for _ in range(board_size)] for _ in range(board_size)] for _ in range(8)]
black_play = [[True for _ in range(board_size)] for _ in range(board_size)]
white_play = [[False for _ in range(board_size)] for _ in range(board_size)]

# Print iterations progress
def printProgressBar (iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def random_games_data():

	lauched = False
	training_data = []
	scores = []
	accepted_scores = []

	for episode in range(initial_games):
		## NOUVELLE PARTIE
		engine = game_engine()


		white_stack = [[[False for _ in range(board_size)] for _ in range(board_size)] for _ in range(8)]
		black_stack = [[[False for _ in range(board_size)] for _ in range(board_size)] for _ in range(8)]

		score = 0
		game_memory = []
		prev_observation = []

		if (not lauched):
			input("press <enter> to start generating random data\n")
			lauched = True
		
		#nice progress bar
		printProgressBar(episode + 1, initial_games, suffix="%d/%d" % (episode + 1, initial_games), length=50)

		map = [[0 for x in range(21)] for y in range(21)]

		# BOUCLE DES TOURS
		for turn in range(goal_steps):
			player = turn % 2

			x = y = 10
			while (engine.get_board()[y][x] != 0):
				x = random.randrange(0, 21)
				y = random.randrange(0, 21)
			
			stack = (white_stack, black_stack)[player]
			## copie de la derniere stack
			curent_stack = [[0 for _ in range(board_size)] for _ in range(board_size)]
			for a in range(board_size):
				for b in range(board_size):
					curent_stack[a][b] = stack[0][a][b]
			## insert le dernier play
			curent_stack[y][x] = True
			## insert la current stack dans la stack
			stack = stack[:-1].insert(0, curent_stack)
			game_state = [[[False for _ in range(board_size)] for _ in range(board_size)] for _ in range(17)]
			for layer in range(0, 8):
				for a in range(board_size):
					for b in range(board_size):
						game_state[layer][a][b] = black_stack[layer][a][b]
			for layer in range(0, 8):
				for a in range(board_size):
					for b in range(board_size):
						game_state[layer + 8][a][b] = white_stack[layer][a][b]
			game_state[16] = (white_play, black_play)[player]
			game_memory.append(game_state)

			try:
				result = engine.move(y, x)
			except:
				break
			if ("win the game" in result):
				score = goal_steps - turn
				break
			if (result is "draw"):
				score = [0, 0]
				break

		if (score >= score_requirement):
			accepted_scores.append(score)
			training_data.append(game_memory)
		scores.append(score)

	print('average accepted score:', mean(accepted_scores))
	print('median accepted score:', median(accepted_scores))
	print(Counter(accepted_scores))

	fd = open("training_data.txt", mode="w")
	print(training_data, file=fd)
	fd.close()

	return (training_data)

training_data = random_games_data()
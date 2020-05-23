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
	training_data = [[], []]
	scores = [[], []]
	accepted_scores = [[], []]

	for episode in range(initial_games):
		## NOUVELLE PARTIE
		engine = game_engine()

		score = [0, 0]
		game_memory = [[], []]
		prev_observation = [[], []]

		if (not lauched):
			input("press <enter> to start generating random data\n")
			lauched = True
		printProgressBar(episode + 1, initial_games, suffix="%d/%d" % (episode + 1, initial_games), length=50)

		map = [[0 for x in range(21)] for y in range(21)]

		# BOUCLE DES TOURS
		for turn in range(goal_steps):
			player = turn % 2

			x = y = 10
			while (engine.get_board()[y][x] != 0):
				x = random.randrange(0, 21)
				y = random.randrange(0, 21)
			
			try:
				result = engine.move(y, x)
			except:
				break
			if ("win the game" in result):
				player = int(result.split()[1]) - 1
				score[player] = goal_steps - turn
				score[not player] = 0
				break
			if (result is "draw"):
				score = [0, 0]
				break

		for i, team_score in enumerate(score):
			if (team_score >= score_requirement):
				accepted_scores[i].append(team_score)
				for data in game_memory[i]:
					training_data[i].append(data)

		scores[0].append(score[0])
		scores[1].append(score[1])

	training_data_save = [np.array(training_data[0]), np.array(training_data[1])]

	np.save("saved_0.npy", training_data_save[0])
	np.save("saved_1.npy", training_data_save[1])

	print('average accepted score:', mean(accepted_scores[0]))
	print('median accepted score:', median(accepted_scores[0]))
	print(Counter(accepted_scores[0]))

	return (training_data[0])

random_games_data()


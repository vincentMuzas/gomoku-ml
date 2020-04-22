#!/usr/bin/python3.7

from game_engine import game_engine

import json

if __name__ == "__main__":
    game = game_engine()

    result = "ok"
    while (result == "ok"):
        play = input("player move:")
        if (play == "map"):
            for line in game.get_board():
                print(line)
            continue
        elif (play == "history"):
            print(game.get_history())
        else:
            play = play.split(' ', 1)
            result = game.move(int(play[1]), int(play[0]))
    
    print(result)
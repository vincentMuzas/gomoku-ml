#!/usr/bin/python3.7

from game_engine import game_engine

if __name__ == "__main__":
    game = game_engine()

    result = "ok"
    while (result == "ok"):
        play = input("player move:")
        if (play == "map"):
            for line in game.get_board():
                print(line)
            continue
        else:
            play = play.split(' ', 1)
            result = game.move(int(play[1]), int(play[0]))
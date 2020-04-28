#!/usr/bin/python3.7

import json

class game_engine:

    save_file = "history.json"

    def __init__(self):
        self.board = [[0 for x in range(21)] for y in range(21)]
        self.history = json.loads(self.import_save_file())
        self.local_history = {}
        self.test_directions = [
            [-1, -1], [-1, 0], [-1, +1],
            [0, -1], [0, +1],
            [+1, -1], [+1, 0], [+1, +1]
        ]
        self.player = 1

    def move(self, posy, posx):
        if (posy not in range(21) or posx not in range(21)):
            raise Exception("invalid position: " + posx + " " + posy)
        if (self.board[posy][posx] != 0):
            raise Exception("invalid play: " + posx + " " + posy)
        
        self.local_history[str(len(self.local_history))] = {"y": posy, "x": posx, "p": self.player}
        self.board[posy][posx] = self.player
        #test if the player win
        for direction in self.test_directions:
            locy = posy - (direction[0] * 5)
            locx = posx - (direction[1] * 5)
            for i in range(5):
                for j in range(5):
                    testy = locy + (direction[0] * i) + (direction[0] * j)
                    testx = locx + (direction[1] * i) + (direction[1] * j)
                    if testx not in range(21) or testy not in range(21) or self.board[testy][testx] != self.player:
                        break
                    if (j == 4):
                        index = 0
                        for key in self.history:
                            index = int(key) + 1
                        self.history[str(index)] = self.local_history

                        # Write the history in a file
                        file = open(self.save_file, mode="w")
                        file.write(json.dumps(self.history, sort_keys=True, indent=4, separators=(',',':')))
                        file.close()

                        return ("player {} win the game".format(self.player))
        self.player = (1, 2)[self.player == 1]
        if (len(self.local_history) == 441):
            return ("draw")
        return (["ok", ("black", "white")[self.player == 1]])

    def import_save_file(self):
        try:
            file = open(self.save_file, mode="r")
            content = file.read()
            content = (content, '{}')[len(content) == 0]
            file.close()
        except OSError:
            #le fichier n'existe pas
            content = '{}'
        return (content)

    def get_board(self):
        return (self.board)
    
    def get_last_move(self):
        return (self.local_history[-1])
    
    def get_history(self):
        return (self.local_history)
#!/usr/bin/python3.7

class game_engine:

    def __init__(self):
        self.board = [[0 for x in range(21)] for y in range(21)]
        self.last_move = None
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
        
        self.last_move = [posy, posx, self.player]
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
                        return ("player {} win the game".format(self.player))
        self.player = (1, 2)[self.player == 1]
        return ("ok")


    def get_board(self):
        return (self.board)
    
    def get_last_move(self):
        return (self.get_last_move)
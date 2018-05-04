#!/usr/bin/env python3

'''
  Chess board class
  Andrew Callahan, Anthony Luc, Kevin Trinh
  Machine Learning
  04/28/2018
'''

import chessboard
import chess_ai
from chess_ai import *


if __name__ == "__main__":
    c = chessboard.Chessboard()

    def make_user_move():
        m = input("Their move ('u' for undo): ")

        if m == "u":
            c.board.pop()
            c.board.pop()
            print(c, "\n")
            return

        c.move_uci(m)
        print(c, "\n")

        make_ai_move()

    def make_ai_move():
        m = get_network_move(c)
        move = next(m)
        print("ai_move:", move[0])
        c.move_uci(str(move[0]))
        print(c, "\n")

    player = input("Playing 'w' or 'b'? ")
    if player == "w":
        m = get_network_move(c)
        c.move_uci(str(next(m)[0]))
        print(c, "\n")

    while True:
        make_user_move()


    
#!/usr/bin/env python3

'''
	Chess AI utilizing a neural network
	Andrew Callahan, Anthony Luc, Kevin Trinh
	Machine Learning
	03/20/2018
'''

DATAFILE = '../data/games.json'

import json
import chessboard

if __name__ == '__main__':
  games = json.load(open(DATAFILE))
  c = chessboard.Chessboard()
  print(c)
  for move in games[1]["moves"]:
    c.move(move)
    print(c)
    print()


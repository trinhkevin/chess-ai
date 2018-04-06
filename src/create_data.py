#!/usr/bin/env python3

'''
	Creates feature map containing all games
	Andrew Callahan, Anthony Luc, Kevin Trinh
	Machine Learning
	03/20/2018
'''

import json
import chessboard

INFILE = '../data/games.csv'
OUTFILE = '../data/games.json'

# Creates games object containing all the games
def create_data():
  games = []
  with open(INFILE) as file:
    next(file)
    for line in file:
      c = chessboard.Chessboard()
      for move in line[12].split(" "):
        c.move(move)
      games.append(c)
  return games

# Writes game object (in json) to file
def write_data(data):
	with open(OUTFILE, 'w') as file:
		json.dump(data, file)

# Main Execution
if __name__ == '__main__':
	games = create_data()
	write_data(games)

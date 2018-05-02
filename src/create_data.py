#!/usr/bin/env python3

'''
	Creates feature map containing all games
	Andrew Callahan, Anthony Luc, Kevin Trinh
	Machine Learning
	03/20/2018
'''

import json
import chessboard
import pickle

INFILE = '../data/games.csv'
OUTFILE = '../data/games.json'

# Creates games object containing all the games
def create_data():
  games = []
  with open(INFILE) as file:
    next(file)
    for line in file:
      c = chessboard.Chessboard()
      for move in line.split(",")[12].split(" "):
        c.move(move)
      games.append(c)
  return games

# Writes game object (in json) to file
def write_data(data):
	with open(OUTFILE, 'wb') as file:
		pickle.dump(data, file)

def load_data():
  with open(OUTFILE, 'rb') as file:
    return pickle.load(file)

# Main Execution
'''
if __name__ == '__main__':

  games = create_data()
  write_data(games)

  print(load_data())
  '''

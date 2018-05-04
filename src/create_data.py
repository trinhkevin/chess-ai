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

INFILEVAL = '../data/data_uci.pgn'
INFILE = '../data/games.csv'
OUTFILE = '../data/games.json'
STOCKFISH = '../data/stockfish.csv'

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

def create_val_data():
  games = []
  gevals = []
  with open(INFILEVAL) as file:
    next(file)
    for line in file:
      if (line.strip() == '' or line[0] == '['):
        continue
      c = chessboard.Chessboard()
      for move in line.split(" "):
        if move[0] == '1' or move[0] == '0':
          continue
        c.move_uci(move.lower())
      games.append(c)
  with open(STOCKFISH) as file:
    next(file)
    for line in file:
      evals = []
      for e in line.split(',')[1].split(' '):
        try:
          evals.append(int(e))
        except:
          evals.append(None)
      gevals.append(evals)
  return (games, gevals)

# Writes game object (in json) to file
def write_data(data):
	with open(OUTFILE, 'wb') as file:
		pickle.dump(data, file)

def load_data():
  with open(OUTFILE, 'rb') as file:
    return pickle.load(file)

if __name__ == '__main__':  
  games = create_val_data()
  write_data(games)
  print(load_data())

#!/usr/bin/env python3

'''
	Creates feature map containing all games
	Andrew Callahan, Anthony Luc, Kevin Trinh
	Machine Learning
	03/20/2018
'''

import json

INFILE = '../data/games.csv'
OUTFILE = '../data/games.json'

# Creates games object containing all the games
def create_data():
	games = []
	with open(INFILE) as file:
		next(file)
		for line in file:
			line = line.strip().split(',')
			game = {}
			game["turns"] = line[4]
			game["victory_status"] = line[5]
			# 0 = white, 1 = black, 2 = draw
			if line[6] == "white":
				game["winner"] = 0
			elif line[7] == "black":
				game["winner"] = 1
			else:
				game["winner"] = 2
			moves = []
			for move in line[12].split(" "):
				moves.append(move)
			game["moves"] = moves
			game["opening_eco"] = line[13]
			games.append(game)
	return games

# Writes game object (in json) to file
def write_data(data):
	with open(OUTFILE, 'w') as file:
		json.dump(data, file)

# Main Execution
if __name__ == '__main__':
	games = create_data()
	write_data(games)

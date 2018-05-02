#!/usr/bin/env python3

from sklearn.neural_network import MLPClassifier
from create_data import load_data
import chessboard
import chess
import pickle
import warnings

def square_value(square):
	return ord(square[0]) - ord('a') + (int(square[1]) - 1) * 8

def square_string(value):
	return str(chr(int(ord('a') + int(value) % 8))) + str(int(value/8 + 1))

def encode_move(move):
	i2 = 0
	diff =  square_value(move[2:4]) - square_value(move[0:2]) 
	if(len(move) == 4 or move[4] == 'q' or move[4] == 'Q'):
		if diff > 0:
			if diff % 8 == 0:
				i2 = diff / 8 # 1-7
			elif diff < 8:
				i2 =  diff + 7 # 8-14
			elif diff % 9 == 0:
				i2 = diff / 9 + 14 #15-21
			elif diff % 7 == 0:
				i2 = diff / 7 + 21 # 22 - 28
		else:
			if diff % 8 == 0:
				i2 = diff / -8 + 28 #29 - 35
			elif diff > -8:
				i2 = -diff + 35 #36 - 42
			elif diff % 7 == 0:
				i2 = diff / -7 + 42 #43 - 49
			elif diff % 9 == 0:
				i2 = diff / -9 + 49 #50 - 56
		if diff == 10:
			i2 = 57
		elif diff == 6:
			i2 = 58
		elif diff == 15:
			i2 = 59
		elif diff == 17:
			i2 = 60
		elif diff == -10:
			i2 = 61
		elif diff == -17:
			i2 = 62
		elif diff == -15:
			i2 = 63
		elif diff == -6:
			i2 = 64
	else:
		if(move[4] == 'b' or move[4] == 'B'):
			i2 = 64 +  diff - 6
		elif(move[4] == 'n' or move[4] == 'N'):
			i2 = 67 + diff - 6 
		elif(move[4] == 'r' or move[4] == 'R'):
			i2 = 70 + diff - 6
	return square_value(move[2:4]) * 73 + i2

def decode_move(move):
	destval = int(move / 73)
	startval = 0
	suffix = ''
	i2 = int(move) % 73

	if i2 < 8:
		startval = destval - i2 * 8
	elif i2 < 15:
		startval = destval - (i2 - 7)
	elif i2 < 22:
		startval = destval - (i2 - 14) * 9
	elif i2 < 29:
		startval = destval - (i2 - 21) * 7
	elif i2 < 36:
		startval = destval - (i2 - 28) * -8
	elif i2 < 43:
		startval = destval - (i2 - 35) * -1
	elif i2 < 50:
		startval = destval - (i2 - 42) * -7
	elif i2 < 57:
		startval = destval - (i2 - 49) * -9
	elif i2 == 57:
		startval = destval - 10
	elif i2 == 58:
		startval = destval - 6
	elif i2 == 59:
		startval = destval - 15
	elif i2 == 60:
		startval = destval - 17
	elif i2 == 61:
		startval = destval + 10
	elif i2 == 62:
		starval = destval + 17
	elif i2 == 63:
		startval = destval + 15
	elif i2 == 64:
		startval = destval + 6
	elif i2 < 68:
		startval = destval - (i2 + 6 - 64)
		suffix = 'b'
	elif i2 < 71:
		startval = destval - (i2 + 6 - 67)
		suffx = 'n'
	elif i2 < 74:
		startval = destval - (i2 + 6 - 70)
		suffix = 'r'

	return square_string(startval) + square_string(destval) + suffix

def train():
	warnings.filterwarnings(action='ignore', category=DeprecationWarning)
	clf = MLPClassifier(solver='sgd', alpha=1e-5, hidden_layer_sizes=(900,100), random_state=1, verbose = 0)
	inputs = None
	classes = None
	with open('netinputs.pkl' , 'rb') as file:
	  inputs = pickle.load(file)
	with open('netclasses.pkl', 'rb') as file:
	  classes = pickle.load(file)

	if(len(inputs) != len(classes)):
	  exit()
	print("training")
	first = True
	for i in range(len(inputs)):
	  if (i%1000 == 0):
	    print("{}%".format(float(i) / len(inputs) * 100.))
	  if first:
	    clf.partial_fit([inputs[i]], [classes[i]], classes = range(1, 4673))
	    first = False
	  else:
	    clf.partial_fit([inputs[i]], [classes[i]])

	with open('network.pkl' , 'wb') as file:
	  pickle.dump(clf, file)
	
def formatData():
	try:
		games = load_data()
	except:
		print("Couldn't load data")

	print("Data loaded!")
	inputs = list()
	classification = list()
	i = 0
	for game in games:
		print(str(i) + " / " + str(len(games)))
		while len(game.board.move_stack):
			move = game.board.peek()
			game.board.pop()
			game.networkInput()
			inputs.append(game.inputs)
			classification.append(encode_move(move.uci()))
		i = i+1

	print(inputs)
	print(classification)

	with open('netinputs.pkl', 'wb') as file:
		pickle.dump(inputs, file)
	with open('netclasses.pkl', 'wb') as file:
		pickle.dump(classification, file)

	print("Files written")

if __name__ == '__main__':
  train()
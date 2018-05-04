#!/usr/bin/env python3

'''
	Chess AI utilizing a neural network
	Andrew Callahan, Anthony Luc, Kevin Trinh
	Machine Learning
	04/05/2018
'''

from sklearn.neural_network import MLPClassifier
import json
import chessboard
import math
import random
import copy
import chess # https://python-chess.readthedocs.io/en/v0.23.0/core.html
import pickle
from chess_network import *

DATAFILE = '../data/games.json'
C = 1
ITERATIONS = 200
clf = None
val_clf = None

with open('network_val.pkl', 'rb') as file:
  val_clf = pickle.load(file)
with open('network.pkl' , 'rb') as file:
  clf = pickle.load(file)

pieces = ['p', 'b','n','r','q']
values = [1 , 3, 3, 5, 9]
class AI:

  def __init__(self, board):
    self.tree = StateNode(board)

  def monteCarlo(self, board):
    self.tree = StateNode(board)
    for i in range(ITERATIONS):
      MCTS(self.tree, network = False)

    result = self.tree.getBestChild()
    self.tree = result

    return self.tree


class NetworkAI:

  def __init__(self, board):
    self.tree = StateNode(board)

  def monteCarlo(self, board):
    self.tree = StateNode(board)
    for i in range(ITERATIONS):
      MCTS(self.tree, network = True)

    result = self.tree.getBestChild()
    self.tree = result

    return self.tree


class StateNode:

  def __init__(self, board, move=None,prob = 0):
    self.visits = 0
    self.value = prob * 50
    self.board = board
    self.children = set()
    self.turn = self.board.getTurn()
    self.move = move

  def isTerminal(self):
    return self.board.board.is_game_over()

  def terminalValue(self):
    if self.board.board.result() == '1/2-1/2':
      return 0
    elif self.board.board.result() == '1-0':
      return 1
    elif self.board.board.result() == '0-1':
      return -1
    else:
      print('Error: invalid terminal')
      exit(1)

  def createNetworkChildren(self):
    for m, k in get_network_move(self.board):
      board = copy.deepcopy(self.board)
      board.move_uci(m.uci())
      child = StateNode(board, m, k)
      self.children.add(child)

  def createChildren(self):
     for move in self.board.getLegalMoves():
      board = copy.deepcopy(self.board)
      board.board.push(move)
      child = StateNode(board, move)
      self.children.add(child)
  def getBestChild(self):
    '''
    # If there are no possible children,
    # set the node terminal and give it a value
    if len(self.children) == 0:
      self.terminal = True
      if self.board.is_stalemate():
        self.terminalValue = 0
      else:
        # White's turn, so white lost
        if self.board.getTurn():
          self.terminalValue = -1
        # Black's turn, so black lost
        else:
          self.terminalValue = 1
      return None
    '''

    # Else, find the best child
    bestChild = None
    for child in self.children:
      if bestChild is None or child.value/child.visits  > bestChild.value/bestChild.visits:
        bestChild = child;
    return bestChild

  def UCB_sample(self):
    result = None
    resultUCB = None
    for child in self.children:
      candidateUCB = UCB(child.value, self.visits, child.visits)
      if result is None or candidateUCB > resultUCB:
        result = child
        resultUCB = candidateUCB
    return result

  def playout(self):
    testBoard = self.board.copy()
    while testBoard.result() == '*':
      captures = list()
      legalMoves = list()
      for move in testBoard.legal_moves:
          legalMoves.append(move)
      move = legalMoves[random.randint(0, len(legalMoves) - 1)]

      '''   
      moveIndex = random.randint(0, - 1)
      index = 0
      move = None
      for legalMove in testBoard.legal_moves:
        if index == moveIndex:
          move = legalMove
          break
        index += 1
      '''
      testBoard.push(move)
      mat = countBoardMaterial(testBoard)
      if abs(mat) >= 9:
        return -1 if mat < 0 else 1

    if testBoard.is_stalemate():
      return 0
    elif testBoard.is_game_over():
      return -1 if testBoard.turn else 1
    return 0
    if testBoard.result() == '1/2-1/2':
      return 0
    else:
      return -1 if testBoard.result() == '0-1' else 1

  def updateValue(self, winner):
    value = -1
    if winner == 0:
      value = 0
    if self.turn:
      if winner == 1:
        value = 1
    else:
      if winner == -1:
        value =1
    self.value += value

def UCB(v, N, n_i):
  return v + C * math.sqrt(math.log(N)/n_i)

def monteCarlo(chessboard):
  root = StateNode(chessboard)
  for i in range(ITERATIONS):
    MCTS(root)
  return root.getBestChild()

def countMaterial(chessboard):
  s = chessboard.board.board_fen()
  result = 0

  for c in s:
    if c in pieces:
      result -= values[pieces.index(c)]
    elif c.lower() in pieces:
      result += values[pieces.index(c.lower())]
  return result
def countBoardMaterial(board):
  s = board.board_fen()
  result = 0

  for c in s:
    if c in pieces:
      result -= values[pieces.index(c)]
    elif c.lower() in pieces:
      result += values[pieces.index(c.lower())]
  return result
def MCTS(state, network = True):
  if state.isTerminal():
    return state.terminalValue()
  state.visits += 1
  if len(state.children) == 0:
    if(network):
      state.createNetworkChildren()
    else:
      state.createChildren()
  for child in state.children:
    if child.visits == 0:
      child.visits = 1
      child.value = 0
      winner = child.playout()
      child.updateValue(winner)
      state.updateValue(winner)
      return winner
  next_state = state.UCB_sample()
  winner = MCTS(next_state)
  state.updateValue(winner)
  return winner

def playoutRepeat(board):
  wwins = 0.
  plays = 0.
  for i in range(0, 1000):
    print(i)
    testBoard = board.copy()
    while testBoard.result() == '*':
      captures = list()
      legalMoves = list()
      for move in testBoard.legal_moves:
        if(testBoard.is_capture(move)):
          captures.append(move)
        else:
          legalMoves.append(move)

      if(len(captures)):
        move = captures[random.randint(0, len(captures) - 1)]
      else:
        move = legalMoves[random.randint(0, len(legalMoves) - 1)]

      testBoard.push(move)

    if testBoard.result() == '1/2-1/2':
      wwins = wwins + 0.5
    else:
      wwins = wwins + (0 if testBoard.result() == '0-1' else 1)

    print(testBoard.result())
    print(testBoard.fen())
    plays = plays + 1
  return (wwins/plays)

def get_network_move(c):
  c.networkInput()
  moves = clf.predict_proba([c.inputs])[0]
  l = dict()
  for i in range(len(moves)):
    l[moves[i]] = clf.classes_[i]
  for k in sorted(l,reverse = True):
    m = decode_move(l[k])
    try:
      m = chess.Move.from_uci(m)
    except:
      continue
    if m in c.board.legal_moves:
      yield (m, k)

if __name__ == '__main__':
  c = chessboard.Chessboard()
  c.networkInput()


  ai2 = NetworkAI(c)
  ai1 = AI(c)

  while not c.board.is_game_over():
    if(c.board.turn):
      r = ai1.monteCarlo(c)
    else:
      r = ai2.monteCarlo(c)

    print(r.move.uci())
    c.move_uci(r.move.uci())
    print(c)

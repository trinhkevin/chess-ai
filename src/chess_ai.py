#!/usr/bin/env python3




'''
	Chess AI utilizing a neural network
	Andrew Callahan, Anthony Luc, Kevin Trinh
	Machine Learning
	04/05/2018
'''

# https://python-chess.readthedocs.io/en/v0.23.0/core.html


DATAFILE = '../data/games.json'
C = 1.41
ITERATIONS = 500

from sklearn.neural_network import MLPClassifier
import json
import chessboard
import math
import random
import copy
import chess





clf = MLPClassifier(solver='sgd', alpha=1e-5, hidden_layer_sizes=(951, 951), random_state=1, verbose = True)


class AI:
  def __init__(self, board):
    self.tree =StateNode(board)

  def monteCarlo(self):
    for i in range(ITERATIONS):
      for j in range(0,20):
        print("*") 
      MCTS(self.tree)
    '''
    curr = root
    while len(curr.children):
      print(curr.getBestChild().move)
      curr = curr.getBestChild()
    '''
    result = self.tree.getBestChild()
    self.tree = result
    return self.tree
class StateNode:
  def __init__(self, board, move=None):
    self.visits = 0
    self.value = 0
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
      if bestChild is None or child.value / child.visits > bestChild.value / bestChild.visits:
        bestChild = child;
    return bestChild

  def UCB_sample(self):
    result = None
    resultUCB = None
    for child in self.children:
      candidateUCB = UCB(child.value/child.visits, self.visits, child.visits)
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
        if(testBoard.is_capture(move)):
          captures.append(move)
        else:
          legalMoves.append(move)

      if(len(captures)):
        move = captures[random.randint(0, len(captures) - 1)]
      else:
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
    value = 0
    
    if winner == 0:
      value = 0.5
    if self.turn:
      if winner == 1:
        value = 1
    else:
      if winner == -1:
        value =1
    self.value += value
    self.board.networkInput()
    clf.fit([self.board.inputs] , [value * 2])


def UCB(v, N, n_i):
  return v + C * math.sqrt(math.log(N)/n_i)

def monteCarlo(chessboard):
  root = StateNode(chessboard)
  for i in range(ITERATIONS):
    MCTS(root)
  return root.getBestChild()

def MCTS(state):
  if state.isTerminal():
    return state.terminalValue()
  state.visits += 1
  if len(state.children) == 0:
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




if __name__ == '__main__':
  c = chessboard.Chessboard()
  c.move_uci("e2e4")
  c.move_uci("d7d5")
  c.move_uci("e4d5")
  c.move_uci("d8d5")
  c.move_uci("b1c3")
  c.move_uci("e8d7")
  c.move_uci("c3d5")
  print(c.board.fen())
  c.board.pop()
  print(c.board.fen())
  #print(playoutRepeat(c))

  '''c = chessboard.Chessboard()
  ai = AI(c)
  for i in range(0, 100):
    print(ai.monteCarlo().move)'''


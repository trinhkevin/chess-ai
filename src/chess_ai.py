#!/usr/bin/env python3

'''
	Chess AI utilizing a neural network
	Andrew Callahan, Anthony Luc, Kevin Trinh
	Machine Learning
	04/05/2018
'''

DATAFILE = '../data/games.json'
C = 1.41
ITERATIONS = 500

import json
import chessboard
import math
import random
import copy

class StateNode:
  def __init__(self, board, move=None):
    self.visits = 0
    self.value = 0
    self.board = board
    self.children = set()
    self.terminalValue = 0
    self.terminal = False
    self.turn = self.board.getTurn()
    self.move = move

  def createChildren(self):
    if not self.board.getLegalMoves().count():
      self.terminal = True
      if self.board.stalemate():
        self.terminalValue = 0
      else:
        # White's turn, so white lost
        if self.board.getTurn():
          self.terminalValue = -1
        # Black's turn, so black lost
        else:
          self.terminalValue = 1
      return

    for move in self.board.getLegalMoves():
      board = copy.deepcopy(self.board)
      board.move_uci(move)
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
      if bestChild is None or child.value > bestChild.value:
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
    if self.terminal:
      return self.terminalValue
    testBoard = self.board.copy()
    terminal = False
    while not terminal:
      
      legalMoves = [x for x in testBoard.legal_moves]
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
      if testBoard.is_game_over() or testBoard.is_stalemate():
        terminal = True
    if testBoard.is_stalemate():
      return 0
    elif testBoard.is_game_over():
      return -1 if testBoard.turn else 1

  def updateValue(self, winner):
    if self.turn:
      if winner == 1:
        self.value += 1
      elif winner == -1:
        self.value -=1
    else:
      if winner == 1:
        self.value -= 1
      elif winner == -1:
        self.value +=1

def UCB(v, N, n_i):
  return v + C * math.sqrt(math.log(N)/n_i)

def monteCarlo(chessboard):
  root = StateNode(chessboard)
  for i in range(ITERATIONS):
    MCTS(root)
  '''
  curr = root
  while len(curr.children):
    print(curr.getBestChild().move)
    curr = curr.getBestChild()
  return root.getBestChild()
  '''

def MCTS(state):
  if state.terminal:
    return state.terminalValue
  state.visits += 1
  if len(state.children) == 0:
    state.createChildren()
  for child in state.children:
    if child.visits == 0:
      child.visits = 1
      child.value = 0
      winner = child.playout()
      state.updateValue(winner)
      return winner
  next_state = state.UCB_sample()
  winner = MCTS(next_state)
  state.updateValue(winner)
  return winner

if __name__ == '__main__':
  c = chessboard.Chessboard()
  print(type(c.board.legal_moves))
  for i in range(0, 10):
    print(c)
    print()
    move = monteCarlo(c).move
    c.move_uci(move)
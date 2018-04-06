#!/usr/bin/env python3

'''
	Chess AI utilizing a neural network
	Andrew Callahan, Anthony Luc, Kevin Trinh
	Machine Learning
	03/20/2018
'''

DATAFILE = '../data/games.json'
C = 1.41


import json
import chessboard
import math




class StateNode:
  def __init__(self, board):
    self.visits = 0
    self.value = 0
    self.board = board
    self.children = set()
    self.terminalValue = 0
    self.terminal = False
    self.turn = 0

  def createChildren(self):
    for move in self.board.legal_moves:
      board = self.board.copy()
      board.move_uci(move)
      child = StateNode(board)
      self.children.add(child)

  def getBestChild(self):
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

    # Else, find the best child
    bestChild = None
    for child in children:
      if bestChild is None or child > bestChild:
        bestChild = child;
    return bestChild

  def UCB_sample(self):
    result = None
    resultUCB = -1
    for child in self.children:
      candidateUCB = UCB(child.value, self.visits, child.visits)
      if result is None or candidateUCB > resultUCB:
        result = child
        resultUCB = candidateUCB
    return result

  def playout(self):
    pass

  def update_value(self, winner):
    if (winner == self.turn):
      self.value = self.value + 1
    else:
      self.value = self.value - 1


def UCB(v, N, ni):
  return v + C * math.sqrt(math.log(N)/ni)

def monte_carlo(board):
  #select

  #expand

  #simulate

  #backup

def MCTS(state):
  state.visits = state.visits + 1
  if (state.terminal):
    return
  if (len(state.children) == 0):
    state.createChildren()
  for child in state.children:
    if(child.visits == 0):
      child.visits = 1
      child.value = 0
      winner = child.playout()
      state.update_value(winner)
      return winner
  next_state = state.UCB_sample()
  winner = MCTS(next_state)
  state.update_value(winner)
  return winner

if __name__ == '__main__':
  games = json.load(open(DATAFILE))
  c = chessboard.Chessboard()
  print(c)
  print()
  for move in games[1]["moves"]:
    c.move(move)
    print(c)
    print()
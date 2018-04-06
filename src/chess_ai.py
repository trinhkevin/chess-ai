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


class stateNode:
  def __init__(self, board):
    self.visits = 0
    self.value = 0
    self.board = board
    self.children = set()
    self.terminalValue = 0
    self.terminal = False
    self.turn = 0

  def createChildren(self):
    

  def getBestChild(self):
    # If there are no possible children,
    # set the node terminal and give it a value
    if(len(children) == 0):
      self.terminal = True
      if self.board.is_stalemate():
        self.terminalValue = 0
      else:
        # White's turn, so white lost
        if self.board.turn:
          self.terminalValue = 0
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
    pass

  def playout(self):
    pass


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
      child.playout()
      return
  
      #expand 
      #break
  



if __name__ == '__main__':
  games = json.load(open(DATAFILE))
  c = chessboard.Chessboard()
  print(c)
  print()
  for move in games[1]["moves"]:
    c.move(move)
    print(c)
    print()
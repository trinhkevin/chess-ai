#!/usr/bin/env python3

'''
  Chess board class
  Andrew Callahan, Anthony Luc, Kevin Trinh
  Machine Learning
  03/22/2018
'''

import chess

class Chessboard(object):
  def __init__(self):
    self.board = chess.Board()

  def __str__(self):
    return str(self.board)

  def move(self, _move):
    self.board.push_san(_move)

  def checkmate(self):
    return self.board.is_game_over()

  def stalemate(self):
    return self.board.is_stalemate()

  def draw(self):
    return self.board.is_insufficient_material()

  def check(self):
    return self.board.is_check()

if __name__ == '__main__':
  c = Chessboard()
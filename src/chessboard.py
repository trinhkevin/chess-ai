#!/usr/bin/env python3

'''
  Chess board class
  Andrew Callahan, Anthony Luc, Kevin Trinh
  Machine Learning
  03/22/2018
'''

import chess
import copy
from bitarray import bitarray

'''
will use this later for visual representation of board
import chess.png
'''

'''
951 total bits (neurons):

data : size

p1piece : 8x8x6
p2piece : 8x8x6
turn : 1
p1_castling : 2
p2_castling : 2
no_progress : 100 (half moves)
'''

class Chessboard(object):
  def __init__(self):
    self.board = chess.Board()
    self.inputs = bitarray(951)
    
  def __str__(self):
    return str(self.board)

  def move_uci(self, _move):
    self.board.push(_move)

  def move(self, _move):
    self.board.push_san(_move)

  def checkmate(self):
    return self.board.is_game_over()

  def is_stalemate(self):
    return self.board.is_stalemate()

  def draw(self):
    return self.board.is_insufficient_material()

  def check(self):
    return self.board.is_check()

  def getTurn(self):
    return self.board.turn

  def turns(self):
    s = []
    while True:
      try:
        move = self.board.pop()
      except IndexError:
        break
      s.append(move)
    t = []
    while len(s) > 0:
      t.append(self.board.copy())
      move = s.pop()
      self.board.push(move)
    return t

  def networkInput(self):
    index = 0

    # White pieces
    for p in ['P', 'R' , 'N' ,'B', 'Q' ,'K']:
      for i in range(0,64):
          if(self.board.piece_at(i) and self.board.piece_at(i).symbol() == p):
              self.netinputs[index] = 1
          else:
              self.netinputs[index] = 0
          index = index + 1

    # Black pieces
    for p in ['p' , 'r' , 'n' , 'b' , 'q' ,'k']:
      for i in range(0,64):
        if(self.board.piece_at(i) and self.board.piece_at(i).symbol() == p):
            self.netinputs[index] = 1
        else:
            self.netinputs[index] = 0
        index = index + 1
    
    # Turn (White = 1, Black = 0)
    self.inputs[index] = self.board.turn
    index += 1

    # White castling
    self.inputs[index] = self.board.has_kingside_castling_rights(chess.WHITE)
    index += 1
    self.inputs[index] = self.board.has_queenside_castling_rights(chess.WHITE)
    index += 1

    # Black castling
    self.inputs[index] = self.board.has_kingside_castling_rights(chess.BLACK)
    index += 1
    self.inputs[index] = self.board.has_queenside_castling_rights(chess.BLACK)
    index += 1
    
    # Turns since last capture or pawn move
    for i in range(0, 100):
      if i == self.board.halfmove_clock:
        inputs[index + i] = 1;
      else:
        inputs[index + i] = 0;

if __name__ == '__main__':
  c = Chessboard()
  c.move("e4")
  c.move("e5")
  c.move("Qh5")
  c.move("Nc6")
  c.move("Bc4")
  c.move("Nf6")

  for i in c.board.legal_moves:
    print(str(i))
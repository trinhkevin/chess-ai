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
872 total bits (neurons):

data : size

p1piece : 8x8x6
p2piece : 8x8x6
p1_castling : 2
p2_castling : 2
no_progress : 100 (half moves)
'''

class Chessboard(object):
  def __init__(self):
    self.board  = chess.Board()
    self.inputs = bitarray(950)
    
  def __str__(self):
    return str(self.board)

  def move_uci(self, _move):
    self.board.push(chess.Move.from_uci(_move))

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

  def getTurn(self):
    return self.board.turn

  def getLegalMoves(self):
    return self.board.legal_moves

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

  def copy(self):
    return self.board.copy()

  def networkInput(self):
    index = 0

    if(self.board.turn):
      # White pieces
      for p in ['P', 'R' , 'N' ,'B', 'Q' ,'K']:
        for i in range(0,64):
            if(self.board.piece_at(i) and self.board.piece_at(i).symbol() == p):
                self.inputs[index] = 1
            else:
                self.inputs[index] = 0
            index = index + 1

      # Black pieces
      for p in ['p' , 'r' , 'n' , 'b' , 'q' ,'k']:
        for i in range(0,64):
          if(self.board.piece_at(i) and self.board.piece_at(i).symbol() == p):
              self.inputs[index] = 1
          else:
              self.inputs[index] = 0
          index = index + 1
    else:
      # Black pieces
      for p in ['p' , 'r' , 'n' , 'b' , 'q' ,'k']:
        for i in range(0,64):
          if(self.board.piece_at(i) and self.board.piece_at(i).symbol() == p):
              self.inputs[index] = 1
          else:
              self.inputs[index] = 0
          index = index + 1
      # White pieces
      for p in ['P', 'R' , 'N' ,'B', 'Q' ,'K']:
        for i in range(0,64):
          if(self.board.piece_at(i) and self.board.piece_at(i).symbol() == p):
              self.inputs[index] = 1
          else:
              self.inputs[index] = 0
          index = index + 1

    if self.board.turn:
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
    else:
       # Black castling
      self.inputs[index] = self.board.has_kingside_castling_rights(chess.BLACK)
      index += 1
      self.inputs[index] = self.board.has_queenside_castling_rights(chess.BLACK)
      index += 1

      # White castling
      self.inputs[index] = self.board.has_kingside_castling_rights(chess.WHITE)
      index += 1
      self.inputs[index] = self.board.has_queenside_castling_rights(chess.WHITE)
      index += 1

    
    # Turns since last capture or pawn move
    for i in range(0, 100):
      if i == self.board.halfmove_clock:
        self.inputs[index + i] = 1;
      else:
        self.inputs[index + i] = 0;

if __name__ == '__main__':
  c = Chessboard()
  c.networkInput()
  print(c.inputs)
  for i in c.board.legal_moves:
    print(str(i))
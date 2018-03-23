#!/usr/bin/env python3

'''
  Chess board class
  Andrew Callahan, Anthony Luc, Kevin Trinh
  Machine Learning
  03/22/2018
'''

import chess
from bitarray import bitarray

'''
will use this later for visual representation of board
import chess.pgn
'''

#p1piece -> 8x8x6
#p2piece -> ''
#repetitions -> 8x8x2
#turn -> 1
#p1 castling -> 2
#p2 castling -> 2
#no-progress -> 50

#951 total bits (neurons)


class Chessboard(object):
  def __init__(self):
    self.board = chess.Board()
    self.netinputs = bitarray(951)

  
    
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
  def getinputbits(self):
    return self.netinputs
  def geninputbits(self):
    index = 0
    #putting piece locations in
    for p in ['P', 'R' , 'N' ,'B', 'Q' ,'K', 'p' , 'r' , 'n' , 'b' , 'q' ,'k']:
        for i in range(0,64):
            if(self.board.piece_at(i) and self.board.piece_at(i).symbol() == p):
                self.netinputs[index] = True
            else:
                self.netinputs[index] = False
            index = index + 1
            
    for i in range(0,128):
        self.netinputs[index + i] = False
    index = index + 128 # skipping repetitions for now
    # ------------------------------------------------------
    
    self.netinputs[index] = self.board.turn
    index = index + 1
    
    
    self.netinputs[index] = self.board.has_kingside_castling_rights(True)
    index = index + 1
    self.netinputs[index] = self.board.has_queenside_castling_rights(True)
    index = index + 1
    self.netinputs[index] = self.board.has_kingside_castling_rights(True)
    index = index + 1
    self.netinputs[index] = self.board.has_queenside_castling_rights(True)
    index = index + 1
    
    for i in range(0,50):
        self.netinputs[index + i] = 0
        #somehow figure this out?
    
    

if __name__ == '__main__':
  c = Chessboard()
  c.geninputbits()
  print(c)
  print(c.getinputbits())
# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 11:29:41 2021

@author: User
"""
import pygame
from constraints import WHITE,GREEN,SQUARE_SIZE,BLUE
from board import Board

class Game:
    def __init__(self,screen):
        self._init()
        self.screen = screen
        
    def update(self):
        self.board.draw(self.screen)
        self.draw_valid_moves(self.valid_moves)
        pygame.display.update()
        
    def _init(self):
        self.selected = None
        self.board = Board()
        self.turn = BLUE
        self.valid_moves = {}
        
    def winner(self):
        return self.board.winner()
        
    def reset(self):
        self._init()
        
    def select(self,row,col):
        if self.selected:
            #print("select")
            result = self._move(row, col)
            if not result:
                #print("no move")
                self.selected = None
                self.select(row, col)
        
        piece = self.board.get_piece(row, col)
        #print(self.turn)
        if piece != 0 and piece.color == self.turn:
            self.selected = piece
            self.valid_moves = self.board.get_valid_moves(piece)
            return True
        
        return False
    
    def _move(self,row,col):
        piece = self.board.get_piece(row, col)
        if self.selected and piece == 0 and (row,col) in self.valid_moves:
            #print(self.valid_moves)
            self.board.move(self.selected, row, col)
            skipped = self.valid_moves[(row,col)]
            if skipped:
                self.board.remove(skipped)
            self.change_turn()
            #print(self.turn)
        else:
            return False
        
        return True
    
    
    def draw_valid_moves(self,moves):
        for move in moves:
            row,col = move
            pygame.draw.circle(self.screen, GREEN, (col*SQUARE_SIZE + SQUARE_SIZE//2,row * SQUARE_SIZE + SQUARE_SIZE//2), 15)
    
    def change_turn(self):
        self.valid_moves = {}
        if self.turn == BLUE:
            self.turn = WHITE
        else:
            self.turn = BLUE
            
            
    def get_board(self):
        return self.board
    
    
    def ai_move(self,board):
        self.board = board
        self.change_turn()
            
            
            
            
            
            
            
            
            
            
            
            
            
        
        
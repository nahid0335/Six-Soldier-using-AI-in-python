# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 23:49:40 2021

@author: User
"""
import pygame
from constraints import BLACK,ROWS,COLS,RED,SQUARE_SIZE,WHITE,BLUE
from piece import Piece

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 6
        self.red_kings = self.white_kings = 0
        self.create_board()
        
    def draw_cubes(self,screen):
        screen.fill(BLACK)
        for row in range(ROWS):
            for col in range(row%2,COLS,2):
                pygame.draw.rect(screen,RED,(col*SQUARE_SIZE,row*SQUARE_SIZE,SQUARE_SIZE,SQUARE_SIZE))
         
            
    def evaluate(self):
        return self.white_left - self.red_left
    
    
    def get_all_pieces(self,color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece !=0  and piece.color == color:
                    pieces.append(piece)
        return pieces
        
        
                
    def move(self,piece,row,col):
        self.board[piece.row][piece.col],self.board[row][col] = self.board[row][col],self.board[piece.row][piece.col]
        piece.move(row,col)
        '''
        if row == ROWS-1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings +=1
            else:
                self.red_kings +=1
       '''         
    def get_piece(self,row,col):
        return self.board[row][col]
            
    
    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if row<2:
                    self.board[row].append(Piece(row,col,WHITE))
                elif row>2:
                    self.board[row].append(Piece(row, col, BLUE))
                else:
                    self.board[row].append(0)
                    
                    
    def draw(self,screen):
        self.draw_cubes(screen)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(screen)
                    
                    
    def remove(self,pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == BLUE:
                    self.red_left -= 1
                else:
                    self.white_left -= 1
                    
                    
                    
    def winner(self):
        if self.red_left <=0:
            return WHITE
        elif self.white_left <=0:
            return BLUE
        
        return None
                    
                    
                    
    def get_valid_moves(self,piece):
        moves = {}
        left = piece.col -1
        right = piece.col + 1
        up = piece.row-1
        down = piece.row+1
        row = piece.row
        col = piece.col
        
        moves.update(self._traversleft(row,left,-1,-1,piece.color))
        moves.update(self._traversright(row,right,COLS,1,piece.color))
        moves.update(self._traversup(up,col,-1,-1,piece.color))
        moves.update(self._traversdown(down,col,ROWS,1,piece.color))
        #print(moves)
        '''
        if piece.color == BLUE or piece.king:
            moves.update(self._travers_left(row, max(row-3,-1), -1,piece.color, left))
            moves.update(self._travers_right(row, max(row-3,-1), -1,piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._travers_left(row+1, min(row+3,1), 1,piece.color, left))
            moves.update(self._travers_right(row+1, min(row+3,1), 1,piece.color, right))
        '''
        return moves
        
        
        
        
        
    def _traversleft(self,row,col,stop,step,color,skipped = []):
        moves = {}
        last = []
        for l in range(col,stop,step):
            if l<0:
                break
            
            current = self.board[row][l]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(row,l)] = last + skipped
                else:
                    moves[(row,l)] = last
                    
                    
                if last:
                    moves.update(self._traversleft(row,l-1,-1,-1,color, skipped=last))
                    moves.update(self._traversup(row-1,l,-1,-1,color,skipped=last))
                    moves.update(self._traversdown(row+1,l,ROWS,1,color,skipped=last))
                break
            elif current.color == color:
                return moves
            else:
                if last:
                    break
                last = [current]
            
        return moves
    
    
    def _traversright(self,row,col,stop,step,color,skipped = []):
        moves = {}
        last = []
        for l in range(col,stop,step):
            if l>=COLS:
                break
            
            current = self.board[row][l]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(row,l)] = last + skipped
                else:
                    moves[(row,l)] = last
                    
                    
                if last:
                    moves.update(self._traversright(row,l+1,COLS,1,color,skipped=last))
                    moves.update(self._traversup(row-1,l,-1,-1,color,skipped=last))
                    moves.update(self._traversdown(row+1,l,ROWS,1,color,skipped=last))
                break
            elif current.color == color:
                return moves
            else:
                if last:
                    break
                last = [current]
            
        return moves
    
    
    def _traversup(self,row,col,stop,step,color,skipped = []):
        moves = {}
        last = []
        for r in range(row,stop,step):
            if r<0:
                break
            
            current = self.board[r][col]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,col)] = last + skipped
                else:
                    moves[(r,col)] = last
                    
                    
                if last:
                    moves.update(self._traversleft(r,col-1,-1,-1,color, skipped=last))
                    moves.update(self._traversright(r,col+1,COLS,1,color,skipped=last))
                    moves.update(self._traversup(r-1,col,-1,-1,color,skipped=last))
                break
            elif current.color == color:
                return moves
            else:
                if last:
                    break
                last = [current]
            
        return moves
        
    
    
    
    
    def _traversdown(self,row,col,stop,step,color,skipped = []):
        moves = {}
        last = []
        moves = {}
        last = []
        for r in range(row,stop,step):
            if r>=ROWS:
                break
            
            current = self.board[r][col]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,col)] = last + skipped
                else:
                    moves[(r,col)] = last
                    
                    
                if last:
                    moves.update(self._traversleft(r,col-1,-1,-1,color, skipped=last))
                    moves.update(self._traversright(r,col+1,COLS,1,color,skipped=last))
                    moves.update(self._traversdown(r+1,col,ROWS,1,color,skipped=last))
                break
            elif current.color == color:
                return moves
            else:
                if last:
                    break
                last = [current]
            
        return moves
        
        
        
    def _travers_left(self,start,stop,step,color,left,skipped = []):
        moves = {}
        last = []
        for r in range(start,stop,step):
            if left<0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,left)] = last + skipped
                else:
                    moves[(r,left)] = last
                    
                    
                if last:
                    if step == -1:
                        row = max(r-3,0)
                    else:
                        row = min(r+3,ROWS)
                        
                    moves.update(self._travers_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._travers_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
                
            left -=1
            
        return moves
            
    
    def _travers_right(self,start,stop,step,color,right,skipped = []):
        moves = {}
        last = []
        for r in range(start,stop,step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r,right)] = last
                    
                    
                if last:
                    if step == -1:
                        row = max(r-3,0)
                    else:
                        row = min(r+3,ROWS)
                        
                    moves.update(self._travers_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._travers_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]
                
            right +=1
        
        return moves
                    
                    
                    
                    
                    
                    
                    
        
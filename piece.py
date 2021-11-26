# -*- coding: utf-8 -*-
"""
Created on Wed Nov 24 00:25:06 2021

@author: User
"""
import pygame
from constraints import SQUARE_SIZE,GREY,CROWN

class Piece:
    PADDING = 15
    OUTLINE = 2
    
    def __init__(self,row,col,color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calculate_position()
        
        
    def calculate_position(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE//2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE//2
        
        
    def make_king(self):
        self.king = True
        
    def draw(self,screen):
        radius = SQUARE_SIZE//2 - self.PADDING
        pygame.draw.circle(screen,GREY,(self.x,self.y),radius+self.OUTLINE)
        pygame.draw.circle(screen,self.color,(self.x,self.y),radius)
        if self.king:
            screen.blit(CROWN,(self.x-CROWN.get_width()//2,self.y-CROWN.get_height()//2))
        
        
    def move(self,row,col):
        self.row = row
        self.col = col
        self.calculate_position()
        
        
    def __repr__(self):
        return str(self.color)
        
        
        
        
        
        
        
        
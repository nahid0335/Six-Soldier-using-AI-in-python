# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 21:42:50 2021

@author: Tamzid
"""

import pygame
from constraints import WIDTH, HEIGHT,SQUARE_SIZE,WHITE,BLUE
from game import Game
from minimax.algorithm import minimax
import random





pygame.init()
FPS = 60
screen = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Six Soldier")


def get_row_col_from_mouse(pos):
    x,y =pos
    row = y //SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row,col



def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(screen)
    game.reset()
    
    
    randomTurn = random.randint(0,2)
    if randomTurn :
        game.turn = WHITE
        print("Computer gets the First turn !!")
    else:
        game.turn = BLUE
        print("Player gets the First turn !!")
    
    while run:
        clock.tick(FPS)
        
        if game.turn == WHITE:
            alpha = float('-inf')
            beta = float('inf')
            value, new_board = minimax(game.get_board(), 4,alpha,beta, WHITE, game)
            game.ai_move(new_board)
        
        if game.winner() != None:
            result = game.winner()
            if(result == WHITE):
                print("!!Winner computer!!")
                pieces = game.get_board().get_all_pieces(WHITE)
                for piece in pieces:
                    piece.make_king()
            else:
                print("!!Winner Player!!")
                pieces = game.get_board().get_all_pieces(BLUE)
                for piece in pieces:
                    piece.make_king()
            run = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                #print(pos)
                row,col = get_row_col_from_mouse(pos)
                game.select(row, col)
        
        game.update()
                    
                
        
                
    pygame.quit()
    
    
main()
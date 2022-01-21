# -*- coding: utf-8 -*-
"""
Created on Fri Nov 26 16:27:18 2021

@author: User
"""
from copy import deepcopy
import pygame
from constraints import WHITE,BLUE

def minimax(position,depth,alpha,beta,max_player,game):
    #position = board
    #max_player -> True = max, Flase = min player
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position,WHITE,game):
            evaluation = minimax(move, depth-1,alpha,beta, False, game)[0]
            maxEval = max(maxEval,evaluation)
            alpha = max(alpha,evaluation)
            if maxEval == evaluation:
                best_move = move
            if beta<=alpha:
                break
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position,BLUE,game):
            evaluation = minimax(move, depth-1,alpha,beta, True, game)[0]
            minEval = min(minEval,evaluation)
            beta = min(beta,evaluation)
            if minEval == evaluation:
                best_move = move
            if beta <= alpha:
                break
        return minEval, best_move
    
    
    
def simulate_move(piece,move,board,game,skip):
    board.move(piece,move[0],move[1])
    if skip:
        board.remove(skip)
        
    return board
    
    
def get_all_moves(board,color,game):
    moves = []
    
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        
        for move,skip in valid_moves.items():
            #draw_moves(game,board,piece)
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row,piece.col)
            new_board = simulate_move(temp_piece,move,temp_board,game,skip)
            moves.append(new_board)
            
    return moves


def draw_moves(game,board,piece):
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.screen)
    pygame.draw.circle(game.screen, (50,100,50), (piece.x,piece.y), 50,5)
    game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    pygame.time.delay(150)            
            
            
            
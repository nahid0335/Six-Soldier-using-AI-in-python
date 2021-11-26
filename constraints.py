# -*- coding: utf-8 -*-
"""
Created on Tue Nov 23 23:26:30 2021

@author: User
"""
import pygame

WIDTH, HEIGHT = 300,500
ROWS, COLS = 5,3
SQUARE_SIZE = 100

#RGB
RED = (255,0,0)
WHITE = (255,255,255)
BLACK = (0,0,0)
BLUE = (0,0,255)
GREY = (128,128,128)
BLUE = (0,0,255)
GREEN = (0,255,0)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'),(45,25))
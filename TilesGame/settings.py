import random, os, sys
import pygame as pg

# game options/settings
TITLE = "Tilemap Game"
WIDTH, HEIGHT = 1024, 768
FPS = 60
run = True
ARIAL_FONT = 'arial'
HS_FILE = "highscore.txt"
TILESIZE = 32
GRIDWIDTH = WIDTH/TILESIZE
GRIDHEIGHT = HEIGHT/TILESIZE

#colors
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
YELLOW = (255, 255, 0)
LIGHTBLUE = (0, 155, 155)
DARKGREY = (40,40,40)
LIGHTGREY = (100,100,100)
BGCOLOR = DARKGREY


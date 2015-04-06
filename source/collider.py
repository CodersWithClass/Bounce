import pygame
import sys
from pygame.locals import *
from pygame import gfxdraw
import gamelog
import random
pygame.init()
clock = pygame.time.Clock()
framerate = 60
resX = 400
resY = 400

SCREEN = pygame.display.set_mode((resX, resY))
pygame.display.set_caption("Bounce")
WHITE = (255, 255, 255)
BLUE = (20, 192, 255)
RED = (255, 0, 0)
GREEN = (0, 168, 0)
myLog = gamelog.Logger(SCREEN)
myLog.maxlines = 10


##Start of paddle configuration
import math
point1 = (100, 100)
point2 = (200, 200)
mouse = (0, 0)
while True:
    SCREEN.fill(WHITE) #Blanks screen

    pygame.gfxdraw.filled_circle(SCREEN, mouse[0], mouse[1], 10, RED)
    pygame.gfxdraw.aacircle(SCREEN, mouse[0], mouse[1], 10, RED)
    
    pygame.gfxdraw.filled_circle(SCREEN, point1[0], point1[1], 10, BLUE)
    pygame.gfxdraw.aacircle(SCREEN, point1[0], point1[1], 10, BLUE)
    
    pygame.gfxdraw.filled_circle(SCREEN, point2[0], point2[1], 10, BLUE)
    pygame.gfxdraw.aacircle(SCREEN, point2[0], point2[1], 10, BLUE)
    
    pygame.draw.line(SCREEN, BLUE, point1, point2, 10)
    pygame.draw.line(SCREEN, GREEN, mouse, point1, 3)
    pygame.draw.line(SCREEN, GREEN, mouse, point2, 3)
    

    for event in pygame.event.get(): #Event handler--all events go here!
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[K_LMETA] or keys[K_RMETA]:
                if keys[K_q] or keys[K_w]:
                    pygame.quit()
                    sys.exit()
        if event.type == MOUSEMOTION:
            mouse = pygame.mouse.get_pos()

    pygame.display.update()
    clock.tick(framerate)

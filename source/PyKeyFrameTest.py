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
import pykeyframe
point1 = (100, 100)
point2 = (200, 200)
mouse = (0, 0)

circlecolorfade = pykeyframe.Action((255, 0, 0), (0, 0, 255), 30)
ballmovement = pykeyframe.Action((100, 100), (200, 200), 30)
ballsize = pykeyframe.Action(10, 100, 30)
circlecolorfade.render()
ballmovement.render()
ballsize.render()
while True:
    SCREEN.fill(WHITE) #Blanks screen
    circlecolorfade.step()
    ballmovement.step()
    ballsize.step()
    pygame.draw.circle(SCREEN, circlecolorfade.position, ballmovement.position, ballsize.position)
    
    #This is how you make your animations go in reverse after they initially play once.
    if circlecolorfade.done:
        circlecolorfade.reverse() #Makes the animation run backwards
        circlecolorfade.rewind() #Resets animator to its untriggered state
    if ballmovement.done:
        ballmovement.reverse()
        ballmovement.rewind()
    if ballsize.done:
        ballsize.reverse()
        ballsize.rewind()
        
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
        if event.type == MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0]:
                circlecolorfade.trigger()
                ballmovement.trigger()
                ballsize.trigger()
                
    pygame.display.update()
    clock.tick(framerate)

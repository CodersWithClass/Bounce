import pygame, sys
from pygame.locals import *
import pykeyframe
import pygame.gfxdraw
import slideshow
pygame.init()
resX = 1366
resY = 768
dispmidpointX = resX / 2
clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((resX, resY))
BLACK = (0 , 0, 0)
WHITE = (255, 255, 255)
YELLOW = (255, 255, 74)
pygame.display.set_caption('Caption Goes Here')

#Credits
creditspush = pykeyframe.Action(resY, resY - 500, 20)
creditspush.render()
creditspush.trigger()
credits = slideshow.Slideshow(SCREEN, 1000, 500, ['../assets/credits1.png', '../assets/credits2.png'], wrap=False)

while True:
    SCREEN.fill(BLACK) 
    creditspush.step()
    credits.display((dispmidpointX - 500, creditspush.position))
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            keys = pygame.key.get_pressed()
            if keys[K_ESCAPE]:
                pygame.quit()
                sys.exit()
            if keys[K_LEFT]:
                credits.backstep()
            if keys[K_RIGHT]:
                credits.step()
            
                
    clock.tick(120)
    pygame.display.update()

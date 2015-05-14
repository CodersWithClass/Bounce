import pygame, sys
from pygame.locals import *
import gamelog
pygame.init()
resX = 800
resY = 800
clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((resX, resY))
WHITE = (255, 255, 255)
pygame.display.set_caption('Caption Goes Here')
myLog = gamelog.Logger(SCREEN, 'myLog.txt', 20, 20)
while True:
    SCREEN.fill(WHITE)   
    myLog.log(pygame.time.get_ticks())
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    clock.tick(120)
    pygame.display.update()

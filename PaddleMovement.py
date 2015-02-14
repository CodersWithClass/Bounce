import pygame, sys
from pygame.locals import *
from pygame import gfxdraw
import GameLog
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
myLog = GameLog.Logger(SCREEN)
myLog.maxlines = 10


##Start of paddle configuration
import math
target_theta = 0 #The position the paddle should be in
current_theta = 0#The current position of the paddle
d_theta = 0 #Change of angle
max_d_theta = 5 #Maximum change of angle
scale = 1

paddle_center = (resX / 2, resY / 2)
paddle = [(-50, -10), (50, -10), (50, 10), (-50, 10)] #Relative position of points in paddle in relationship to center point
polar_coords = []
pointlist = [(0, 0), (0, 0), (0, 0), (0, 0)]
for coords in paddle: #Converts coordinates into polar coordinates
    dist = math.sqrt(coords[0] ** 2 + coords[1] ** 1)
    new_coords = (dist,
                  math.degrees(math.asin(coords[1] / dist)coords[0])))
    polar_coords.append(new_coords)
##End of paddle configuration
while True:
    SCREEN.fill(WHITE) #Blanks screen
    
    target_theta += d_theta
    current_theta += (target_theta - current_theta) * .1
    myLog.log(current_theta)
    for num in range(0, len(polar_coords)):
        items = polar_coords[num]

        pointlist[num] = (items[0] * math.cos(math.radians(items[1] + current_theta)) + paddle_center[0],
                          items[0] * math.sin(math.radians(items[1] + current_theta)) + paddle_center[1])
    print(pointlist)
    pygame.draw.polygon(SCREEN, BLUE, pointlist, 0)

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
            if keys[K_LEFT] or keys[K_RIGHT]: #Directional control defaults to look for arrows before WASD
                if keys[K_LEFT] and not keys[K_RIGHT]:
                    d_theta = max_d_theta
                if keys[K_RIGHT] and not keys[K_LEFT]:
                    d_theta = -max_d_theta
            elif keys[K_a] or keys[K_d]:
                if keys[K_a] and not keys[K_d]: 
                    d_theta = max_d_theta
                if keys[K_d] and not keys[K_a]:
                    d_theta = -max_d_theta
        if event.type == KEYUP:
            keys = event.key
            if keys == K_LEFT or keys == K_RIGHT or keys == K_a or keys == K_d:
                d_theta = 0

    pygame.display.update()
    clock.tick(framerate)

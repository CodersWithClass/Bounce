import pygame
import sys
import math
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
PI = math.pi
myLog = gamelog.Logger(SCREEN)
myLog.maxlines = 10

mouse = (0, 0)

##Start of paddle configuration
#***ALL ANGLE MEASUREMENTS ARE IN RADIANS!!!***
target_theta = 0 #The position the paddle should be in (radians)
current_theta = 0#The current position of the paddle
d_theta = 0 #Change of angle
max_d_theta = PI * 7 / 180 #Maximum change of angle
max_theta = 45
min_theta = -45
damp = .2 #Dampening factor of the feedback loop--controls how "heavy" the paddle feels by affecting response time

paddle_center = (resX / 2, resY / 2)
paddle = [(-50, -10), (50, -10), (50, 10), (-50, 10)] #Relative position of points in paddle in relationship to center point
polar_coords = []
pointlist = [(0, 0), (0, 0), (0, 0), (0, 0)]
for coords in paddle: #Converts coordinates into polar coordinates, in radians
    dist = math.sqrt(coords[0] ** 2 + coords[1] ** 1)
    new_coords = (dist,
                  math.atan2(coords[1], coords[0]))
    polar_coords.append(new_coords)
##End of paddle configuration
screencolor = WHITE
while True:
    SCREEN.fill(screencolor) #Blanks screen
    
    ###START PADDLE CODE#################################################################################
    target_theta -= d_theta
    #print(target_theta)
    current_theta += (target_theta - current_theta) * damp
    #myLog.log(current_theta)
    for num in range(0, len(polar_coords)):
        items = polar_coords[num]

        pointlist[num] = (items[0] * math.cos(items[1] + current_theta) + 
                          paddle_center[0],
                          items[0] * math.sin(items[1] + current_theta) + 
                          paddle_center[1])
    pygame.draw.polygon(SCREEN, BLUE, pointlist, 0)
    pygame.gfxdraw.aapolygon(SCREEN, pointlist, BLUE)
    pygame.draw.line(SCREEN, RED, pointlist[0], pointlist[1], 1)
    
    ##END PADDLE CODE
    
    ##BEGIN BOUNCE CODE
    centerpoint = (int(pointlist[0][0] + (pointlist[1][0] - pointlist[0][0]) / 2), 
                   int(pointlist[0][1] + (pointlist[1][1] - pointlist[0][1]) / 2))
    pygame.draw.circle(SCREEN, GREEN, centerpoint, 10)
    velXi = (mouse[0] - centerpoint[0])
    velYi = (mouse[1] - centerpoint[1])
   # myLog.log(str(velXi) + ';' + str(velYi))
    length = math.sqrt(velXi**2 + velYi**2)
    pygame.draw.line(SCREEN, GREEN, centerpoint, mouse, 3)
    thetaV1 = -(math.atan2(velYi, velXi))
    thetaV2 = thetaV1 + 2*current_theta
    velXf = -(math.cos(thetaV2) * length) + centerpoint[0]
    velYf = -(math.sin(thetaV2) * length) + centerpoint[1]
    pygame.draw.line(SCREEN, GREEN, centerpoint, (velXf, velYf), 3)
    myLog.log(math.degrees(thetaV2))

    ###END BOUNCE CODE#################################################################################
    
    pygame.gfxdraw.filled_circle(SCREEN, mouse[0], mouse[1], 10, RED)
    pygame.gfxdraw.aacircle(SCREEN, mouse[0], mouse[1], 10, RED)
    
    ##BEGIN COLLIDER CODE
    p1 = pointlist[0]#Upper left corner of paddle mesh
    p2 = pointlist[1]#Upper right corner of paddle mesh
    b = mouse#Ball position
    theta1 = -math.atan2((b[1] - p1[1]), (b[0] - p1[0])) + current_theta #Ball's polar position relative to p1
    theta2 = -(current_theta - math.atan2((p2[1] - b[1]), (p2[0] - b[0])))  #Ball's polar position relative to p2
    d1 = math.sqrt((b[1] - p1[1])**2 + (b[0] - p1[0])**2) #Straight-line distance between paddle and ball--this forms the hypontenuse of the right triangle which we will use to determine tangency
    d2 = math.sqrt((b[1] - p2[1])**2 + (b[0] - p2[0])**2)
    
    if abs(theta1) <= PI/2 and abs(theta2) <= PI/2 and dist < 10:
        screencolor = (0, 255, 0)
    else:
        screencolor = WHITE
    pygame.draw.line(SCREEN, RED, b, p1, 3)
    pygame.draw.line(SCREEN, RED, b, p2, 3)
    dist = d1 * math.sin(theta1)
    #myLog.log(str(math.degrees(theta1)) + ";" + str(math.degrees(theta2)))
    ###END COLLIDER CODE
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
        if event.type == MOUSEMOTION: 
            mouse = pygame.mouse.get_pos()

    pygame.display.update()
    clock.tick(framerate)

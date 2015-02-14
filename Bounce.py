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
class Ball:
    def __init__(self, surf, color, coords, radius, velocity, acceleration, attr = None):
    #Creates an instance of Ball
        self.coords = list(coords)
        self.color = list(color)
        self.vel = list(velocity)
        self.acc = list(acceleration)
        self.property = attr #Special property--not used now but can be implemented for something else if needed 
        self.surf = surf
        self.radius = radius

    def update(self): #Updates the ball's position, velocity, and is where the physics for the ball happen.
        self.vel = [self.vel[0] + self.acc[0], self.vel[1] + self.acc[1]]
        self.coords = [self.coords[0] + self.vel[0], self.coords[1] + self.vel[1]]
        
    def bounceY(self):
        self.vel[1] = -self.vel[1]- self.acc[1]
        
    def bounceX(self):
        self.vel[0] = -self.vel[0] - self.acc[0]
        
    def draw(self):
        pygame.gfxdraw.aacircle(self.surf, int(self.coords[0]), int(self.coords[1]), self.radius, self.color) #Draws a smooth circle outline without those jagged pixellated edges
        pygame.gfxdraw.filled_circle(self.surf, int(self.coords[0]), int(self.coords[1]), self.radius, self.color) #Draws the filled center of the circle
        #Circles are kinda like chocolate truffles--smooth on the outside, filled on the inside...
        
class BallGroup:
    def __init__(self):
        self.objects = []
        self.size = 0 #Keeps track of how many balls are in list
    def add(self, instance):
        self.objects.append(instance)
    def draw(self):
        for items in self.objects:
            items.draw()
    def remove(self, obj):#Because "kill" sounds too morbid...
        del(obj)
        
    def update(self):
        count = 0
        
        while count < len(self.objects):#Allows the list to become modifiable due to advanced for loops being immutable                            
            items = self.objects[count]
            items.update()
            if items.coords[1] > resY:
                del(self.objects[count])
                items.bounceY()
            if items.coords[0] > resX or items.coords[0] < 0:
                #del(self.objects[count])
                items.bounceX()
            if items.coords[1] > resY + 200:
                del(self.objects[count])
 
            count += 1
            
        self.size = len(self.objects)
        
   
        
    def clear(self): #Deletes all objects in group
        for num in range(0, len(self.objects)):
            del(self.objects[-1])


myGroup = BallGroup()
frames = 0 #counts how many frames the screen has drawn
mouse = (0, 0)
while True:
    if pygame.mouse.get_pressed() == (1, 0, 0):
        myGroup.add(Ball(SCREEN, RED, (random.randint(10, 390), random.randint(10, 390)), 10, (random.randint(-10, 10), random.randint(-10, 10)), (0, .5)))
    frames += 1
    if frames % 60 == 0: #Drops a ball from top of screen every nth interval.
        myGroup.add(Ball(SCREEN, RED, (int(resX / 2), 0), 10, (0, 0), (0, .5)))
        
    SCREEN.fill(WHITE) #Blanks screen
    if pygame.mouse.get_focused():
        myLog.log(mouse) #Prints out debug text on the left hand side of screen
    myGroup.update() #Updates physics on balls
    myGroup.draw() #Draws balls on screen
    
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

#Setup thingies#########################
import pygame, sys
from pygame.locals import *
from pygame import gfxdraw
import gamelog
import math

pygame.init()
clock = pygame.time.Clock()
framerate = 60
resX = 800
resY = 400

SCREEN = pygame.display.set_mode((resX, resY))
pygame.display.set_caption("Bounce")

PI = math.pi

WHITE = (255, 255, 255) #Defines colors for graphics
BLACK = (0, 0, 0)
BLUE = (0, 106, 255)
RED = (255, 0, 0)
YELLOW = (255, 189, 0)
GREEN = (0, 168, 0)

WHITE = (0, 0, 0) #Defines colors for graphics
BLACK = (255, 255, 255)
BLUE = (0, 255, 255)
RED = (255, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

colorlist = [RED, YELLOW, GREEN, BLUE] #List of colors for balls--the RNG will select a random color to make the next ball.
attrlist = ["RED", "YELLOW", "GREEN", "BLUE"]
myLog = gamelog.Logger(SCREEN)
myLog.maxlines = 10
myLog.color = BLACK
#End Setup Thingies##############

#Scoring#########
score = 0
consecutive = 0 #How many balls in a row did the user hit?
strikes = 0 #How many times did user miss?
#End Scoring#####

#Ball and BallGroup Class to check for compatibility with final game
class Ball:
    def __init__(self, surf, color, coords, radius, velocity, acceleration, attr = None):
    #Creates an instance of Ball

        self.coords = list(coords)
        self.color = list(color)
        self.vel = list(velocity)
        self.acc = list(acceleration)
        self.property = attr #Special property--not used now but can be implemented for something else if needed 
        self.blurlist = []
        self.surf = surf
        self.radius = radius
        self.goalcollide = False #Is ball colliding with goal zone?

    def update(self): #Updates the ball's position, velocity, and is where the physics for the ball happen.
        self.vel = [self.vel[0] + self.acc[0], self.vel[1] + self.acc[1]]
        
        self.coords = [self.coords[0] + self.vel[0], 
                       self.coords[1] + self.vel[1]]
        
        self.blurlist = []
        self.goalcollide = self.coords[1] <= 25 + self.radius
    def bounceY(self):
        self.vel[1] = -self.vel[1]- self.acc[1]
        
    def bounceX(self):
        self.vel[0] = -self.vel[0] - self.acc[0]
        
    def draw(self):

        #Draw a smooth circle outline without those jagged pixellated edges
        pygame.gfxdraw.aacircle(self.surf, int(self.coords[0]), 
                                int(self.coords[1]), self.radius, self.color) 
        #Draw the filled center of the circle 
        pygame.gfxdraw.filled_circle(self.surf, int(self.coords[0]),                                      
                                     int(self.coords[1]), self.radius, self.color)
        #Circles are kinda like chocolate truffles--smooth on the outside, filled on the inside...
        

#Goal Code Start########
tol = 20 #Adds a bit of "give" to the goals to count "close" shots.
BLUEGOAL = range(0 - tol, int(resX / 4) + tol)
GREENGOAL = range(int(resX / 4) - tol, int(resX / 2) + tol)
YELLOWGOAL = range(int(resX / 2) - tol, int(resX * 3 / 4) + tol)
REDGOAL = range(int(resX * 3 / 4) - tol, int(resX) + tol)
GOALHEIGHT = 25
goallist = [REDGOAL, YELLOWGOAL, GREENGOAL, BLUEGOAL]
#Goal Code End########

#Other bits of initialization code
ballcolor = 0
mouse = (0, 0)
myBall = Ball(SCREEN, RED, 
                    mouse, 10, 
                    (0, 0), (0, 0))


ballGroup = [myBall]
backcolor = WHITE
count = 0 #Counter variable for list iteration to make list mutable
#End init. code


##Start of paddle configuration#################################################################
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
    new_coords = (dist, math.atan2(coords[1], coords[0]))
    polar_coords.append(new_coords)
screencolor = WHITE
##End of paddle configuration#################################################################
centerpoint = (int(pointlist[0][0] + (pointlist[1][0] - pointlist[0][0]) / 2), 
                int(pointlist[0][1] + (pointlist[1][1] - pointlist[0][1]) / 2))

while True:
    SCREEN.fill(screencolor)
   
    #Edits current ball's parameters (ball being used as cursor)
    myBall.coords = mouse
    myBall.color = colorlist[ballcolor]
    myBall.property = attrlist[ballcolor]
    #End cursor properties
    
    
    
    ###START PADDLE MOVEMENT CODE #################################################################
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
    
    ##END PADDLE MOVEMENT CODE #################################################################
    
    
    ###### BALL UPDATE CODE ########################################
    
    while count < len(ballGroup):#Allows the list to become modifiable due to advanced for loops being immutable       
            items = ballGroup[count]
            items.update()
            if (items.coords[0] >= resX - items.radius or 
                    items.coords[0] <= items.radius):
                items.bounceX()
                
            if items.coords[1] < GOALHEIGHT and count != 0:
                #items.bounceY()
                if int(items.coords[0]) in goallist[attrlist.index(items.property)]: #Correct Goal
                    consecutive += 1
                    score += 1
                    backcolor = (0, 255, 0)
                else: #Incorrect Goal
                    backcolor = (180, 0, 0)
                    consecutive = 0
                    strikes += 1
                    
                del(ballGroup[count]) #Deletes ball from system if it hits goal zone and collision registered.
                
                
            ##BEGIN COLLIDER CODE#################################################################
            
            p1 = pointlist[0]#Upper left corner of paddle mesh
            p2 = pointlist[1]#Upper right corner of paddle mesh

            theta1 = -math.atan2((items.coords[1] - p1[1]), (items.coords[0] - p1[0])) + current_theta #Ball's polar position relative to p1
            theta2 = -(current_theta - math.atan2((p2[1] - items.coords[1]), (p2[0] - items.coords[0])))  #Ball's polar position relative to p2
            d1 = math.sqrt((items.coords[1] - p1[1])**2 + (items.coords[0] - p1[0])**2) #Straight-line distance between paddle and ball--this forms the hypontenuse of the right triangle which we will use to determine tangency
            d2 = math.sqrt((items.coords[1] - p2[1])**2 + (items.coords[0] - p2[0])**2)
            dist = d1 * math.sin(theta1)
            
            if abs(theta1) <= PI/2 and abs(theta2) <= PI/2 and dist < 10:
                screencolor = (0, 255, 0)
                #Paddle physics are only enabled if the ball is in contact with the ball
                
                #PADDLE PHYSICS##################################################################
                #This section includes any code that modifies the ball's velocity as a direct result of the paddle
                # myLog.log(str(items.vel[0]) + ';' + str(items.vel[1]))
                length = math.sqrt(items.vel[0]**2 + items.vel[1]**2)
                thetaV1 = -(math.atan2(items.vel[1], items.vel[0]))
                thetaV2 = thetaV1 + 2*current_theta
                items.vel[0] = (math.cos(thetaV2) * length) 
                items.vel[1] = (math.sin(thetaV2) * length)   
                #myLog.log(math.degrees(thetaV2)) #Outputs angle of reflected velocity if uncommented
                
                #END PADDLE PHYSICS##################################################################
            
            else:
                screencolor = WHITE
            pygame.draw.line(SCREEN, RED, items.coords, p1, 3)
            pygame.draw.line(SCREEN, RED, items.coords, p2, 3)
            #myLog.log(str(math.degrees(theta1)) + ";" + str(math.degrees(theta2))) #Outputs ball's relative angles from edges of paddle when uncommented
            
            ###END COLLIDER CODE    
                
            count += 1
            items.draw()
    #####END BALL UPDATE CODE -- everything else is outside the loop ###############################
            
    count = 0    #Resets the loop  
    #####Draws Goals###########################################
            
    for num in range(0, 4):
        pygame.draw.rect(SCREEN, colorlist[3 - num],
                                 ((resX / 4) * num, 0, (resX / 4), GOALHEIGHT))
    #####End goal code###########################################    
    
    myLog.log("SCORE: " + str(score) + "; " + 
              str(consecutive) + " IN A ROW; " + 
              str(strikes) + " STRIKES") 
            
        
   
    
    
    ###EVENT HANDLER CODE###########################################################################   
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
            if keys[K_UP]:
                ballcolor += 1
                if ballcolor >= 4:
                    ballcolor = 0
            if keys[K_DOWN]:
                ballcolor -= 1
                if ballcolor < 0:
                    ballcolor = 3
            if keys[K_ESCAPE]:
                score = 0
                strikes = 0
                consecutive = 0
                backcolor = WHITE
        if event.type == MOUSEMOTION:
            mouse = pygame.mouse.get_pos()
        if event.type == MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed() == (1, 0, 0):
                ballGroup.append(Ball(SCREEN, colorlist[ballcolor], 
                                 mouse, 10, (0, 10), (0, 0), 
                                 attrlist[ballcolor]))
        if event.type == KEYUP:
            keys = event.key
            if keys == K_LEFT or keys == K_RIGHT or keys == K_a or keys == K_d:
                d_theta = 0

    pygame.display.update()
    clock.tick(framerate)
    ###END EVENT HANDLER CODE###########################################################################
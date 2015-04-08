#Setup thingies#########################
import pygame, sys
from pygame.locals import *
from pygame import gfxdraw
import gamelog
import random
import pykeyframe
import math

pygame.init()
clock = pygame.time.Clock()
framerate = 60
resX = 1366
resY = 768

SCREEN = pygame.display.set_mode((resX, resY))
pygame.display.set_caption("Bounce")

PI = math.pi

WHITE = (255, 255, 255) #Defines colors for graphics
BLACK = (0, 0, 0)
BLUE = (0, 106, 255)
RED = (255, 0, 0)
YELLOW = (255, 189, 0)
GREEN = (0, 168, 0)

WHITE = (255, 255, 255) #Defines prettier colors for graphics
BLACK = (0, 0, 0)
BLUE = (0, 177, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 74)
GREEN = (0, 255, 44)

colorlist = [RED, YELLOW, GREEN, BLUE] #List of colors for balls--the RNG will select a random color to make the next ball.
attrlist = ["RED", "YELLOW", "GREEN", "BLUE"]
myLog = gamelog.Logger(SCREEN)
myLog.maxlines = 10
myLog.color = WHITE
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
GOALHEIGHT = 35
goallist = [REDGOAL, YELLOWGOAL, GREENGOAL, BLUEGOAL]
#Goal Code End########

#Launcher Code Start#######
launcherY = 75 #Launchers always start 75 pixels from top of screen
launchtime = None
#Launcher Code End########

#Other bits of initialization code
ballcolor = 0
mouse = (0, 0)


ballGroup = []
count = 0 #Counter variable for list iteration to make list mutable
ballsize = 10
#End init. code


##Start of paddle configuration#################################################################
#***ALL ANGLE MEASUREMENTS ARE IN RADIANS!!!***
target_theta = 0 #The position the paddle should be in (radians)
current_theta = 0#The current position of the paddle
d_theta = 0 #Change of angle
max_d_theta = PI * 4 / 180 #Paddle Rotation Speed
max_theta = PI/4 + .25
min_theta = -PI/4 - .25
damp = .3 #Dampening factor of the feedback loop--controls how "heavy" the paddle feels by affecting response time

paddlecolor = pykeyframe.Action(colorlist[-1], colorlist[-1], 15)
paddlecolor.render()

paddle_height = 13
paddle_width = 90

paddle_center = (int(resX / 2), resY  - (paddle_width + 100))

paddle = [(-paddle_width, -paddle_height), 
          (paddle_width, -paddle_height), 
          (paddle_width, paddle_height), 
          (-paddle_width, paddle_height)] #Relative position of points in paddle in relationship to center point
polar_coords = []
pointlist = [(0, 0), (0, 0), (0, 0), (0, 0)]
for coords in paddle: #Converts coordinates into polar coordinates, in radians
    dist = math.sqrt(coords[0] ** 2 + coords[1] ** 1)
    new_coords = (dist, math.atan2(coords[1], coords[0]))
    polar_coords.append(new_coords)
##End of paddle configuration#################################################################

##MENU CODE BEGIN
state = "logo" #State machine logic
debug = False #Debug mode prints out log data to screen
finished = False #Is animation done moving?
cwcsplash = pygame.image.load('../assets/CodersWithClass{}Bounce.png')
cwcrect = cwcsplash.get_rect(center = (int(resX / 2), int(resY / 2))) #bounding box for centering CWC logo
goalactionlist = []
curtainsurf = pygame.Surface(cwcrect.size, depth = 32)#Color depth seems to be the main performance drag here. 32-bit works better sometimes, 24-bit others. Blame this if your game lags!
for num in range(0,len(goallist)): #Adds animation to the onscreen buttons
    goalactionlist.append(pykeyframe.Action(-1, GOALHEIGHT, 7))
    goalactionlist[num].render()
    
curtainfade = pykeyframe.Action(255, 0, 12) #Animates fading in/out the "curtain" -- black transparent/opaque surface that gives the "fade-in/out" effect
curtainfade.render()
curtainfade.trigger()


menu_options = ["play", "scores", "about", "exit"] #What the buttons on the top say
menuselect = 0#What the player is currently selecting
easteregg = None #Easter Egg Variable
okay = pygame.mixer.Sound("../assets/Complete.ogg")
#MENU CODE END
while True:
    SCREEN.fill(BLACK)  
            
    if state == "play":
        gametime = pygame.time.get_ticks()
        paddlecolor.step()
        
        
        ###START PADDLE MOVEMENT CODE #################################################################
        if target_theta < min_theta:
            target_theta = min_theta
        if target_theta > max_theta:
            target_theta = max_theta
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
        pygame.draw.polygon(SCREEN, paddlecolor.position, pointlist, 0)
        pygame.gfxdraw.aapolygon(SCREEN, pointlist, paddlecolor.position)
        pygame.draw.line(SCREEN, RED, pointlist[0], pointlist[1], 1) #Collision mesh for paddle
        
        centerpoint = (int(pointlist[0][0] + (pointlist[1][0] - pointlist[0][0]) / 2), 
                    int(pointlist[0][1] + (pointlist[1][1] - pointlist[0][1]) / 2))
        pygame.draw.circle(SCREEN, RED, centerpoint, 10)
        ##END PADDLE MOVEMENT CODE #################################################################
        
        ##Ball launcher code########################################
        if launchtime != None:
            myLog.log(str(launchtime - gametime))#Gives a countdown until ball is to be launched
        else:
            myLog.log(str(len(ballGroup)) + " balls on screen")
        
        if len(ballGroup) == 0 and launchtime == None: #Only tries to launch a ball if there aren't any on the field and one hasn't been queued. It'd be pretty hard to catch two balls otherwise!
            myLog.log("ABOUT TO LAUNCH!")
            if bool(random.getrandbits(1)): #Gets a random True/False. True: launch from left side, False: launch from right
                launcherX = ballsize + 1 #The +1 is so that the ball doesn't somehow magically get stuck inside the wall and infinitely bounce 
            else:
                launcherX = resX - (ballsize + 1)

            launchtime = gametime + random.randint(250, 2000) #Launches the ball some time in the future from current time. FUUUUTURE!!!
        pygame.draw.circle(SCREEN, RED, (launcherX, launcherY), ballsize)
        if gametime >= launchtime and launchtime != None:
            launchtime = None #There already is a ball on the field, so no need to use launchtime to suppress launcher.
            ballspeed = random.randint(7, 20)
            
            launcherdiffX = launcherX - centerpoint[0] #Differences in coordinates between paddle and ball launcher
            launcherdiffY = launcherY - centerpoint[1] 
            launcherdist = math.sqrt(launcherdiffX ** 2 + launcherdiffY ** 2)
            
            coeff = ballspeed / launcherdist #Multiplicative coefficient used to scale down velocity to match a set value
            velX = -launcherdiffX * coeff #These are negative to make ball travel backwards from launcher to center of paddle
            velY = -launcherdiffY * coeff
            ballvel = (velX, velY)
            ballGroup.append(Ball(SCREEN, colorlist[ballcolor], 
                             (launcherX, launcherY), ballsize, ballvel, (0, 0), 
                             attrlist[ballcolor]))
        #END BALL LAUNCHER CODE ########################################
        
        ###### BALL UPDATE CODE ########################################
        while count < len(ballGroup):#Allows the list to become modifiable due to advanced for loops being immutable       
                items = ballGroup[count]
                items.update()
                ##CODE THING THAT DELETES BALLS WHEN THEY DISAPPEAR OFF BOTTOM OF SCREEN
                if items.coords[1] >= resY + items.radius:
                    del[ballGroup[count]]
                ##END CODE THING THAT DISAPPEAR OFF BOTTOM
                
                ##MAKES BALL BOUNCE ON WALLS
                if (items.coords[0] >= resX - items.radius or 
                        items.coords[0] <= items.radius):
                    items.bounceX()
                ##END WALL BOUNCE CODE
                
                
                if items.coords[1] < GOALHEIGHT:
                    #items.bounceY()
                    if int(items.coords[0]) in goallist[attrlist.index(items.property)]: #Correct Goal
                        consecutive += 1
                        score += 1
                    else: #Incorrect Goal
                        consecutive = 0
                        strikes += 1
                        
                    del(ballGroup[count]) #Deletes ball from system if it hits goal zone and collision registered.
                    
                if items.coords[1] >= centerpoint[1] - polar_coords[0][0]:
                    ##BEGIN COLLIDER CODE#################################################################
                    
                    p1 = pointlist[0]#Upper left corner of paddle mesh
                    p2 = pointlist[1]#Upper right corner of paddle mesh
        
                    theta1 = -math.atan2((items.coords[1] - p1[1]), (items.coords[0] - p1[0])) + current_theta #Ball's polar position relative to p1
                    theta2 = -(current_theta - math.atan2((p2[1] - items.coords[1]), (p2[0] - items.coords[0])))  #Ball's polar position relative to p2
                    d1 = math.sqrt((items.coords[1] - p1[1])**2 + (items.coords[0] - p1[0])**2) #Straight-line distance between paddle and ball--this forms the hypontenuse of the right triangle which we will use to determine tangency
                    d2 = math.sqrt((items.coords[1] - p2[1])**2 + (items.coords[0] - p2[0])**2)
                    dist = d1 * math.sin(theta1)
                    
                    if abs(theta1) <= PI/2 and abs(theta2) <= PI/2 and dist < 10 and dist > -10:
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
                   
                #pygame.draw.line(SCREEN, RED, items.coords, p1, 3)
                #pygame.draw.line(SCREEN, RED, items.coords, p2, 3)
                #myLog.log(str(math.degrees(theta1)) + ";" + str(math.degrees(theta2))) #Outputs ball's relative angles from edges of paddle when uncommented
                
                ###END COLLIDER CODE    
                    
                count += 1
                items.draw()
        #####END BALL UPDATE CODE -- everything else is outside the loop ###############################
                
        count = 0    #Resets the loop  
        #####Draws Goals###########################################
                
        for num in range(0, 4):
            pygame.draw.rect(SCREEN, colorlist[3 - num],
                                     (int(resX / 4) * num, 0, int(resX / 4) + 2, GOALHEIGHT))
        #####End goal code###########################################    
        
        #myLog.log("SCORE: " + str(score) + "; " + 
        #          str(consecutive) + " IN A ROW; " + 
        #          str(strikes) + " STRIKES") 
        #myLog.log(pygame.time.get_ticks() - starttime)
            
    ##MAIN MENU CODE#################################################################################
    elif state == "logo" or state == "logofadeout": #All these are elif statements so they don't get evaluated if they don't need to. This saves lots of time when running the state machine.
        curtainfade.step()
        curtainsurf.set_alpha(curtainfade.position)
        SCREEN.blit(cwcsplash, cwcrect.topleft)
        SCREEN.blit(curtainsurf, cwcrect.topleft)
        
    if curtainfade.done and state == "logo":
        curtainfade.reverse()
        curtainfade.rewind()
        curtainfade.trigger()
        state = "logofadeout"
        
    elif curtainfade.done and state == "logofadeout":
        state = "menustart"        

    elif "menu" in state: #Any state that contains the word "Menu"
        if state == "menustart":
            goalactionlist[0].trigger()
            goalactionlist[0].step()
            pygame.draw.rect(SCREEN, colorlist[-1], (0, 0, int(resX / 4), goalactionlist[0].position))
            for num in range(1, len(goallist)):
                goalactionlist[num].step()
                if goalactionlist[num - 1].done: #If the goal behind this one is done moving, make this one start. This gives a sequential animation effect.
                    goalactionlist[num].trigger()
            if goalactionlist[-1].done:
                for num in range(0,len(goallist)): #Re-renders buttons to "pop-out" when highlighted in main menu sequence
                    goalactionlist[num] = (pykeyframe.Action(GOALHEIGHT, int(GOALHEIGHT * 2.5), 7))
                    goalactionlist[num].render()
                state = "menu"  
        elif state == "menu":
            for num in range(len(goallist)):
                #goalactionlist[num].step()
                if menuselect == num:
                    goalactionlist[num].step()
                    goalactionlist[num].trigger()
                else:
                    goalactionlist[num].done = False
                    goalactionlist[num].backstep()
        
        elif state == "menuplay":
            goalactionlist[0].done = False
            goalactionlist[0].backstep()
            state = "play"
    #if state == "menuabout":
        for items in menu_options:
            num = menu_options.index(items)  
            menufont = pygame.font.Font(None, goalactionlist[num].position)
            label = menufont.render(items, 1, BLACK)
            fontrect =  label.get_rect()
            fontrect.center = (((int(resX / 4) * num) + int(resX / 8)),
                                int(goalactionlist[num].position / 2))
            
            pygame.draw.rect(SCREEN, colorlist[3 - num],
                             (int(resX / 4) * num, 0, int(resX / 4) , goalactionlist[num].position))
            SCREEN.blit(label, fontrect.topleft)
    ##END MENU CODE#################################################################################            
            
#EVENT HANDLER CODE########
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            keys = pygame.key.get_pressed()
            
            if state == "logo" or state == "logofadeout": #Easter egg!
                if keys[K_s] and keys[K_a] and keys[K_m]:
                    easteregg = "sam"
                    okay.play()
                    
            if state == "menu": #Menu controls
                if keys[K_LEFT] or keys[K_RIGHT]: #Directional control defaults to look for arrows before WASD
                    if keys[K_LEFT] and not keys[K_RIGHT]:
                        menuselect -= 1
                        if menuselect <= -1:
                            menuselect = len(menu_options) - 1
                    if keys[K_RIGHT] and not keys[K_LEFT]:
                        menuselect += 1
                        if menuselect >= len(menu_options):
                            menuselect = 0
                elif keys[K_a] or keys[K_d]:
                    if keys[K_a] and not keys[K_d]: 
                        menuselect -= 1
                        if menuselect <= -1:
                            menuselect = len(menu_options) - 1
                    if keys[K_d] and not keys[K_a]:
                        menuselect += 1
                        if menuselect >= len(menu_options):
                            menuselect = 0
                if (keys[K_SPACE] or keys[K_RETURN]) and (menuselect == 0 or menuselect == 3):
                    state += menu_options[menuselect]
                    windowfade = pykeyframe.Action(BLACK, colorlist[3 - menuselect], 20)
                    print(state)
                    
            if state == "play":
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
                
                if keys[K_UP] or keys[K_DOWN]: #Directional control defaults to look for arrows before WASD
                    if keys[K_UP] and not keys[K_DOWN]:
                        d_theta = max_d_theta
                    if keys[K_DOWN] and not keys[K_UP]:
                        d_theta = -max_d_theta
                elif keys[K_s] or keys[K_w]:
                    if keys[K_w] and not keys[K_s]: 
                        d_theta = max_d_theta
                    if keys[K_s] and not keys[K_w]:
                        d_theta = -max_d_theta
                
        if event.type == KEYUP:
            keys = event.key
            if state == "play":
                if keys == K_LEFT or keys == K_RIGHT or keys == K_a or keys == K_d:
                    d_theta = 0
    clock.tick(60)
    pygame.display.update()

    
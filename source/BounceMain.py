#    "Bounce" (c) 2015 CodersWithClass{}
#    See bottom of code for license and terms of use
'''
TODO:
-Tell player high score at end of game, and if record broken
-Savefiles, stats, etc.
-Instructions
-Paddle skips color
-Inconsistent speed change
-Ball sometimes won't go through paddle
-Try again button on game over screen
-Randomize colors
-Make the ball die after certain amount of time
-Let players regain lives after a specific number of consecutive shots
-Create a log file that outputs error codes to file after a crash.
'''

#Setup thingies for Pygame. This includes display information, all necessary imports and dependencies (including external files), and major constants. #########################
import pygame
import sys
import os
from pygame.locals import *
from pygame import gfxdraw
import gamelog
import random
import pykeyframe
import math
import slideshow
from platform import system

#Determines if the computer is a Mac or not. If it's a Mac, control key commands change to Command key
isaMac = system() == "Darwin"

pygame.init()
clock = pygame.time.Clock()
framerate = 60

version = "Bounce v0.21 Preview Release"

oops = [] #List of exceptions thrown during execution. Helps in creating a watchdog.

#Import files
okay = pygame.mixer.Sound("../assets/Complete.ogg")
cwcsplash = pygame.image.load('../assets/CodersWithClass{}Bounce.png')
bouncetitle = pygame.image.load('../assets/BounceTitle.png')
keyimage = pygame.image.load('../assets/BounceKeys.png')

try:
    savefile = open('../savefile.txt', 'r')
    highscore = savefile.readline()
    highscore = int(highscore[:len(highscore) - 1])
    
except Exception:
    savefile = open('../savefile.txt', 'w')
    savefile.write('0\n')
bounceicon = pygame.image.load('../assets/bounce.ico')
bounceleft = pygame.mixer.Sound('../assets/BounceLeft.ogg') #Sound the ball makes when it hits the left edge of the display. It makes a different sound depending on 


#Set up display
pygame.display.set_icon(bounceicon)
pygame.display.set_caption("Bounce", "Bounce")
displayinfo = pygame.display.Info()
resX = displayinfo.current_w #Sets up Pygame Window and scales it to fit your screen
resY = displayinfo.current_h
if isaMac:
    resY -= 22 #This compensates for the height of the taskbar, so the screen actually fills entire screen.
    SCREEN = pygame.display.set_mode((resX, resY), pygame.HWSURFACE|pygame.NOFRAME) #This makes a kinda-full-screen window in Mac--basically a regular window without the buttons or menu bar.
else:
    SCREEN = pygame.display.set_mode((resX, resY), pygame.HWSURFACE|pygame.FULLSCREEN)#Plays in full 
pygame.mouse.set_visible(False) #Makes the mouse invisible. This discourages people from trying to use it as an input device

#Screen position constants
dispmidpointX = int(resX / 2)
dispmidpointY = int(resY / 2)

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

#Goal Constants Start########
#This creates constants for the goal collision system.
TOL = 20 #Adds a bit of "give" to the goals to count "close" shots.
BLUEGOAL = range(0 - TOL, int(resX / 4) + TOL)
GREENGOAL = range(int(resX / 4) - TOL, dispmidpointX + TOL)
YELLOWGOAL = range(dispmidpointX - TOL, int(resX * 3 / 4) + TOL)
REDGOAL = range(int(resX * 3 / 4) - TOL, int(resX) + TOL)
GOALHEIGHT = 35
goallist = [REDGOAL, YELLOWGOAL, GREENGOAL, BLUEGOAL]
#Goal Constants End########

#End Setup Thingies##############

#Scoring#########
score = 0
highscore = 0 #High score
consecutive = 0 #How many balls in a row did the user hit?
strikes = 0 #How many times did user miss?
maxstrikes = 5 #Maximum number of strikes
strikelist = [] #List of strike "icons" to display on scoreboard
for num in range(maxstrikes):
    strikelist.append(pykeyframe.Action(GREEN, RED, 10))
    strikelist[num].render()
scorefont = pygame.font.Font(None, 80)
scorelabel = scorefont.render("9001", 1, WHITE)
#End Scoring#####

#versioning info
versionfont = pygame.font.Font(None, 50)
versionlabel = versionfont.render(version, 1, WHITE)
versionrect = versionlabel.get_rect()
versionrect.bottomright = (resX - 10, resY - 10)
#End versioning info

#Credits


#Ball and BallGroup Class to check for compatibility with final game
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
        self.goalcollide = False #Is ball colliding with goal zone?

    def update(self): #Updates the ball's position, velocity, and is where the physics for the ball happen.
        self.vel = [self.vel[0] + self.acc[0], self.vel[1] + self.acc[1]]
        self.coords = [self.coords[0] + self.vel[0], 
                       self.coords[1] + self.vel[1]]
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


#Launcher Code Start#######
launcherY = 75 #Launchers always start 75 pixels from top of screen
launcherX = 0
launchtime = None
launchdir = False
#Launcher Code End########

#Other bits of initialization code
ballcolor = 0
paddlecolor = 0
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

paddlecolorfade = pykeyframe.Action(colorlist[0], colorlist[0], 15)
paddlecolorfade.render()

paddle_height = 13
paddle_width = 90

paddle_center = (dispmidpointX, resY  - (paddle_width + 100))

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

#Image optimization by converting image surfaces to same format as display
bouncetitle = bouncetitle.convert()

#Credits
creditspush = pykeyframe.Action(resY, resY - 550, 20)
creditspush.render()
creditspush.trigger()
credits = slideshow.Slideshow(SCREEN, 1000, 550, ['../assets/credits1.png', '../assets/credits2.png'], wrap=False)


##MENU CODE BEGIN
state = "keys" #State machine logic
#state = "menustart"
debug = False #Debug mode prints out log data to screen
finished = False #Is animation done moving?

cwcrect = cwcsplash.get_rect(center = (dispmidpointX, dispmidpointY)) #bounding box for centering CWC logo
keyrect = keyimage.get_rect(center = (dispmidpointX, dispmidpointY))

bouncerect = bouncetitle.get_rect(center = (dispmidpointX, dispmidpointY))
bouncecurtain = pygame.Surface(bouncerect.size, depth = 32)

goalactionlist = []
curtainsurf = pygame.Surface(cwcrect.size, depth = 32)#Color depth seems to be the main performance drag here. 32-bit works better sometimes, 24-bit others. Blame this if your game lags!
for num in range(0,len(goallist)): #Adds animation to the onscreen buttons
    goalactionlist.append(pykeyframe.Action(-1, GOALHEIGHT, 7))
    goalactionlist[num].render()
    
curtainfade = pykeyframe.Action(255, 0, 45) #Animates fading in/out the "curtain" -- black transparent/opaque surface that gives the "fade-in/out" effect
curtainfade.render()
curtainfade.trigger()

menu_options = ["play", "scores", "about", "exit"] #What the buttons on the top say
menuselect = 0#What the player is currently selecting
easteregg = None #Easter Egg Variable

#MENU CODE END

####ARROW MENU SETUP CODE################################################
arrowchoicefont = pygame.font.Font(None, 50)
titlefont = pygame.font.Font(None, 175)
arrowchoicelist = ["quit", "retry", "continue", "yes", "no", "continue"] #Creates the choices that appear on the "arrow menu"
arrowlabellist = [] #Creates label surfaces that actually display font
arrowlabelrectlist = [] #Creates rectangle objects for each text that helps with alignment
for items in arrowchoicelist:
    arrowlabellist.append(arrowchoicefont.render(items, 1, WHITE))
    arrowlabelrectlist.append(arrowlabellist[arrowchoicelist.index(items)].get_rect())
pauselabel = titlefont.render("paused", 1, WHITE)
pauserect = pauselabel.get_rect()
pauserect.center = (dispmidpointX, dispmidpointY)

quitlabel = titlefont.render("quit?", 1, WHITE)
quitrect = quitlabel.get_rect()
quitrect.center = (dispmidpointX, dispmidpointY)

retrylabel = titlefont.render("retry?", 1, WHITE)
retryrect = retrylabel.get_rect()
retryrect.center = (dispmidpointX, dispmidpointY)

surelabel = titlefont.render("sure?", 1, WHITE)
surerect = surelabel.get_rect()
surerect.center = (dispmidpointX, dispmidpointY)

exitlabel = titlefont.render("exit?", 1, WHITE)
exitrect = exitlabel.get_rect()
exitrect.center = (dispmidpointX, dispmidpointY)

confirmscreen = pygame.surface.Surface((resX, resY))
pausescreen = pygame.surface.Surface((resX, resY))
gameoverscreen = pygame.surface.Surface((resX, resY))

confcurtain = pykeyframe.Action(-resY, 0, 20)
pausecurtain = pykeyframe.Action(-resY, 0, 20)
gameovercurtain = pykeyframe.Action(-resY, 0, 20)
confcurtain.render()
confcurtain.trigger()
pausecurtain.render()
pausecurtain.trigger()
gameovercurtain.render()
gameovercurtain.trigger()

gameoverfont = pygame.font.Font(None, 100)
gameoverlabel = gameoverfont.render("game over.", 1, WHITE)
gameoverrect = gameoverlabel.get_rect()
gameoverrect.center = (dispmidpointX, 250)
####END ARROW MENU SETUP CODE################################################   
while True:
    try:
        SCREEN.fill(BLACK)  
        #myLog.log(clock.get_fps())
        myLog.log(state)
        if state == "play" or state == "paused":
            gametime = pygame.time.get_ticks()
            paddlecolorfade.step()
            
            
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
            pygame.draw.polygon(SCREEN, paddlecolorfade.position, pointlist, 0)
            pygame.gfxdraw.aapolygon(SCREEN, pointlist, paddlecolorfade.position)
            #pygame.draw.line(SCREEN, RED, pointlist[0], pointlist[1], 1) #Collision mesh for paddle
            
            centerpoint = (int(pointlist[0][0] + (pointlist[1][0] - pointlist[0][0]) / 2), 
                        int(pointlist[0][1] + (pointlist[1][1] - pointlist[0][1]) / 2))
            #pygame.draw.circle(SCREEN, RED, centerpoint, 10)
            
            if len(ballGroup) != 0:# and ballGroup[0].vel[1] > 0:
                thetapredict = -(math.atan2(centerpoint[1] - launcherY, centerpoint[0] - launcherX )) + 2*current_theta
                for num in range(1, 9):
                    if num % 2 == 0:
                        pygame.draw.line(SCREEN, paddlecolorfade.position, (centerpoint[0] + (math.cos(thetapredict) * (num * 20)),
                                                                      centerpoint[1] + (math.sin(thetapredict) * (num * 20))), 
                                         (centerpoint[0] + (math.cos(thetapredict) * ((num + 1) * 20)), 
                                          centerpoint[1] + (math.sin(thetapredict) * ((num + 1) * 20))), 5) #Draws dashed "prediction line" showing ball's projected trajectory
            ##END PADDLE MOVEMENT CODE #################################################################
            
            ##Ball launcher code########################################
            #if launchtime != None:
            #    myLog.log(str(launchtime - gametime))#Gives a countdown until ball is to be launched
            #else:
            #    myLog.log(str(len(ballGroup)) + " balls on screen")
            
            if launchtime == None and len(ballGroup) == 0: #Only tries to launch a ball if there aren't any on the field and one hasn't been queued. It'd be pretty hard to catch two balls otherwise!
                myLog.log("ABOUT TO LAUNCH!")
                ballcolor = random.randint(0, 3)
                launchdir = random.getrandbits(1)
                if launchdir: #Gets a random True/False. True: launch from left side, False: launch from right
                    launcherX = ballsize + 1 #The +1 is so that the ball doesn't somehow magically get stuck inside the wall and infinitely bounce 
                else:
                    launcherX = resX - (ballsize + 1)
    
                launchtime = gametime + random.randint(250, 2000) #Launches the ball some time in the future from current time. FUUUUTURE!!!
                
                ballspeed = random.randint(5, score + 5)
                
                launcherdiffX = launcherX - centerpoint[0] #Differences in coordinates between paddle and ball launcher
                launcherdiffY = launcherY - centerpoint[1] 
                launcherdist = math.sqrt(launcherdiffX ** 2 + launcherdiffY ** 2)
                
                coeff = ballspeed / launcherdist #Multiplicative coefficient used to scale down velocity to match a set value
                velX = -launcherdiffX * coeff #These are negative to make ball travel backwards from launcher to center of paddle
                velY = -launcherdiffY * coeff
        
                ballvel = (velX, velY)
            arrowscale = (launchdir * 2) - 1
            arrowsize = 20
            pygame.gfxdraw.aapolygon(SCREEN, ((launcherX - arrowsize + (arrowscale * arrowsize), 
                                               launcherY + arrowsize),
                                              (launcherX + arrowsize + (arrowscale * arrowsize), 
                                               launcherY + arrowsize),
                                              (launcherX + (arrowscale * arrowsize), 
                                               launcherY - int(arrowsize * 0.8))), colorlist[ballcolor])
            pygame.gfxdraw.filled_polygon(SCREEN, ((launcherX - arrowsize + (arrowscale * arrowsize) + 1, 
                                               launcherY + arrowsize - 1),
                                              (launcherX + arrowsize + (arrowscale * arrowsize), 
                                               launcherY + arrowsize),
                                              (launcherX + (arrowscale * arrowsize), 
                                               launcherY - int(arrowsize * 0.8) + 1)), colorlist[ballcolor])
            if launchtime != None and  gametime >= launchtime:
                launchtime = None #There already is a ball on the field, so no need to use launchtime to suppress launcher.
                ballGroup.append(Ball(SCREEN, colorlist[ballcolor], 
                                 (launcherX, launcherY), ballsize, ballvel, (0, 0), 
                                 attrlist[ballcolor]))
            #END BALL LAUNCHER CODE ########################################
            
            ###### BALL UPDATE CODE ########################################
            while count < len(ballGroup):#Allows the list to become modifiable due to advanced for loops being immutable       
                items = ballGroup[count]
                
                if state != "paused":
                    pygame.mixer.music.unpause()
                    items.update()
                    ##CODE THING THAT DELETES BALLS WHEN THEY DISAPPEAR OFF BOTTOM OF SCREEN
                    if items.coords[1] >= resY + items.radius:
                        del[ballGroup[count]]
                        strikes += 1
                        
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
                        
                    if (items.coords[1] >= centerpoint[1] - polar_coords[0][0] and 
                        attrlist.index(items.property) == paddlecolor):
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
                            while dist < 10 and dist > -30: #This keeps ball from getting "stuck" in paddle by repeatedly trying to move the ball outside the paddle until ball is a set distance away, but also prevents game from hanging if ball bounces "the other way"
                                items.coords[0] += items.vel[0]
                                items.coords[1] += items.vel[1]
                                dist = d1 * math.sin(theta1)
                        
                                theta1 = -math.atan2((items.coords[1] - p1[1]), (items.coords[0] - p1[0])) + current_theta #Ball's polar position relative to p1
                                d1 = math.sqrt((items.coords[1] - p1[1])**2 + (items.coords[0] - p1[0])**2) #Straight-line distance between paddle and ball--this forms the hypontenuse of the right triangle which we will use to determine tangency
                            #myLog.log(math.degrees(thetaV2)) #Outputs angle of reflected velocity if uncommented
                            
                            #END PADDLE PHYSICS##################################################################
                       
                    #pygame.draw.line(SCREEN, RED, items.coords, p1, 3)
                    #pygame.draw.line(SCREEN, RED, items.coords, p2, 3)
                    #myLog.log(str(math.degrees(theta1)) + ";" + str(math.degrees(theta2))) #Outputs ball's relative angles from edges of paddle when uncommented
                    
                    ###END COLLIDER CODE    
                else:
                    pygame.mixer.music.pause()        
                count += 1
                items.draw()
            #####END BALL UPDATE CODE -- everything else is outside the loop ###############################
                    
            count = 0    #Resets the loop  
            #####Draws Goals###########################################
                    
            for num in range(0, 4):
                pygame.draw.rect(SCREEN, colorlist[3 - num],
                                         (int(resX / 4) * num, 0, int(resX / 4) + 2, GOALHEIGHT))
            #####End goal code###########################################    
            
            #####Scoreboard Code#####################
            if strikes > 0 and strikes <= maxstrikes:
                strikelist[-strikes].trigger()
            if strikes >= maxstrikes:
                state = "gameover"
            for num in range(maxstrikes):
                strikelist[num].step()
                pygame.gfxdraw.filled_circle(SCREEN, resX - ((num + 1) * 50), resY - 75, 14, strikelist[num].position)
                pygame.gfxdraw.aacircle(SCREEN, resX - ((num + 1) * 50), resY - 75, 14, strikelist[num].position)
            #myLog.log("SCORE: " + str(score) + "; " + 
            #          str(consecutive) + " IN A ROW; " + 
            #          str(strikes) + " STRIKES") 
            #myLog.log(pygame.time.get_ticks() - starttime)  
            scorelabel = scorefont.render("score: " + str(score), 1, WHITE)
            scorerect = scorelabel.get_rect()
            scorerect.bottomleft = (50, resY - 60)
            SCREEN.blit(scorelabel, scorerect.topleft)
        
        ##MAIN MENU CODE#################################################################################
        elif state == "keys": #Shows the beginning help image with key controls
            SCREEN.blit(keyimage, keyrect.topleft)
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
                savefile = open('../savefile.txt', 'r')
                highscore = savefile.readline()
                highscore = int(highscore[:len(highscore) - 1])
                
                pygame.mixer.music.load('../assets/BounceMenu.ogg')
                pygame.mixer.music.play()
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
                creditspush.done = False
                creditspush.backstep()
            elif state == "menuplay":
                goalactionlist[0].done = False
                goalactionlist[0].backstep()
                state = "newgame"
            elif state =="menuexit":
                state = "exitsure"
                myLog.log(blag)
                confcurtain.trigger()
            
            
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
                
    
            SCREEN.blit(bouncetitle, bouncerect.topleft)
            SCREEN.blit(versionlabel, versionrect.topleft)
            if state == "menuabout":
                creditspush.trigger()
                myLog.log("GIANT CIRCLE!")
                creditspush.step()
            credits.display((dispmidpointX - 500, creditspush.position))
        ##END MENU CODE#################################################################################            
        ##BEGIN PAUSE MENU CODE#################################################################################
        elif "sure" in state:
            confirmscreen.fill(BLACK)

            confcurtain.trigger()
            confcurtain.done = False
            confcurtain.step()
            
            
            #Confirmation Menu
            pygame.gfxdraw.aapolygon(confirmscreen, ((dispmidpointX, 10), #Upwards-pointing arrow
                                              (dispmidpointX - 40, 80),
                                              (dispmidpointX + 40, 80)), WHITE) 
            pygame.gfxdraw.filled_polygon(confirmscreen, ((dispmidpointX, 11),
                                                   (dispmidpointX - 39, 79),
                                                   (dispmidpointX + 39, 79)), WHITE) 
            
            pygame.gfxdraw.aapolygon(confirmscreen, ((dispmidpointX, resY - 10), #Downwards-pointing arrow
                                              (dispmidpointX - 40, resY - 80),
                                              (dispmidpointX + 40, resY - 80)), WHITE) 
            pygame.gfxdraw.filled_polygon(confirmscreen, ((dispmidpointX, resY - 11),
                                                   (dispmidpointX - 39, resY - 79),
                                                   (dispmidpointX + 39, resY - 79)), WHITE) 
            
            if state == "retrysure":
                confirmscreen.blit(retrylabel, retryrect.topleft)   
            elif state == "quitsure":
                confirmscreen.blit(quitlabel, quitrect.topleft)   
            elif state == "clearsure":
                confirmscreen.blit(surelabel, surerect.topleft)        
            elif state == "exitsure":
                confirmscreen.blit(exitlabel, exitrect.topleft)
                     
            arrowlabelrectlist[4].centerx = dispmidpointX #no button
            arrowlabelrectlist[4].bottom = resY - 100
            confirmscreen.blit(arrowlabellist[4], arrowlabelrectlist[4].topleft)
            
            arrowlabelrectlist[3].centerx = dispmidpointX #yes button
            arrowlabelrectlist[3].top = 100
            confirmscreen.blit(arrowlabellist[3], arrowlabelrectlist[3].topleft)
        if "sure" not in state:
            confcurtain.trigger()
            confcurtain.done = False
            confcurtain.backstep()
            
            if state == "paused":
                #Pause Menu
                pausescreen.fill(BLACK)
                pausecurtain.trigger()
                pausecurtain.done = False
                pausecurtain.step()
                pygame.gfxdraw.aapolygon(pausescreen, ((dispmidpointX, 10), #Upwards-pointing arrow
                                                  (dispmidpointX - 40, 80),
                                                  (dispmidpointX + 40, 80)), WHITE) 
                pygame.gfxdraw.filled_polygon(pausescreen, ((dispmidpointX, 11),
                                                       (dispmidpointX - 39, 79),
                                                       (dispmidpointX + 39, 79)), WHITE) 
                
                pygame.gfxdraw.aapolygon(pausescreen, ((dispmidpointX, resY - 10), #Downwards-pointing arrow
                                                  (dispmidpointX - 40, resY - 80),
                                                  (dispmidpointX + 40, resY - 80)), WHITE) 
                pygame.gfxdraw.filled_polygon(pausescreen, ((dispmidpointX, resY - 11),
                                                       (dispmidpointX - 39, resY - 79),
                                                       (dispmidpointX + 39, resY - 79)), WHITE) 
                
                pygame.gfxdraw.aapolygon(pausescreen, ((10, dispmidpointY), #Leftwards-pointing arrow
                                                  (80, dispmidpointY - 40),
                                                  (80, dispmidpointY + 40)), WHITE) 
                pygame.gfxdraw.filled_polygon(pausescreen, ((11, dispmidpointY),
                                                       (79, dispmidpointY - 39),
                                                       (79, dispmidpointY + 39)), WHITE) 
                
                '''
                pygame.gfxdraw.aapolygon(pausescreen, ((resX - 10, dispmidpointY), #Rightwards-pointing arrow
                                                  (resX - 80, dispmidpointY - 40),
                                                  (resX - 80, dispmidpointY + 40)), WHITE) 
                pygame.gfxdraw.filled_polygon(pausescreen, ((resX - 11, dispmidpointY),
                                                       (resX - 79, dispmidpointY - 39),
                                                       (resX - 79, dispmidpointY + 39)), WHITE) '''
                
                pausescreen.blit(pauselabel, pauserect.topleft)   
                arrowlabelrectlist[0].centerx = dispmidpointX #quit button
                arrowlabelrectlist[0].bottom = resY - 100
                pausescreen.blit(arrowlabellist[0], arrowlabelrectlist[0].topleft)
                
                arrowlabelrectlist[2].centerx = dispmidpointX #continue button
                arrowlabelrectlist[2].top = 100
                pausescreen.blit(arrowlabellist[2], arrowlabelrectlist[2].topleft)
                
                arrowlabelrectlist[1].left = 100 #retry button
                arrowlabelrectlist[1].centery = dispmidpointY
                pausescreen.blit(arrowlabellist[1], arrowlabelrectlist[1].topleft)
            elif state != "paused":
                pausecurtain.trigger()
                pausecurtain.done = False
                pausecurtain.backstep()
            if state == "gameover":
                #Pause Menu
                pygame.mixer.music.stop()
                gameoverscreen.fill(BLACK)
                gameovercurtain.trigger()
                gameovercurtain.done = False
                gameovercurtain.step()
                
                pygame.gfxdraw.aapolygon(gameoverscreen, ((resX - 10, dispmidpointY), #Rightwards-pointing arrow
                                                  (resX - 80, dispmidpointY - 40),
                                                  (resX - 80, dispmidpointY + 40)), WHITE) 
                pygame.gfxdraw.filled_polygon(gameoverscreen, ((resX - 11, dispmidpointY),
                                                       (resX - 79, dispmidpointY - 39),
                                                       (resX - 79, dispmidpointY + 39)), WHITE) 
                
                pygame.gfxdraw.aapolygon(gameoverscreen, ((10, dispmidpointY), #Leftwards-pointing arrow
                                                  (80, dispmidpointY - 40),
                                                  (80, dispmidpointY + 40)), WHITE) 
                pygame.gfxdraw.filled_polygon(gameoverscreen, ((11, dispmidpointY),
                                                       (79, dispmidpointY - 39),
                                                       (79, dispmidpointY + 39)), WHITE) 
                
                gameoverscreen.blit(gameoverlabel, gameoverrect.topleft)   
    
                arrowlabelrectlist[1].left = 100 #retry button
                arrowlabelrectlist[1].centery = dispmidpointY
                gameoverscreen.blit(arrowlabellist[1], arrowlabelrectlist[1].topleft)
                
                arrowlabelrectlist[2].right = resX - 100 #continue button
                arrowlabelrectlist[2].centery = dispmidpointY
                gameoverscreen.blit(arrowlabellist[2], arrowlabelrectlist[2].topleft)
                
                scorelabel = scorefont.render("score: " + str(score), 1, WHITE)
                scorerect = scorelabel.get_rect()
                scorerect.top = 400
                scorerect.centerx = dispmidpointX
                gameoverscreen.blit(scorelabel, scorerect.topleft)
                
                if score > highscore:
                    savefile = open('../savefile.txt', 'w')
                    savefile.write(str(score) + '\n')
                    savefile.close()
                    
                
    
        ##BEGIN PAUSE MENU CODE#################################################################################
        if state =="resetmenu":
            goalactionlist = []
            curtainsurf = pygame.Surface(cwcrect.size, depth = 32)#Color depth seems to be the main performance drag here. 32-bit works better sometimes, 24-bit others. Blame this if your game lags!
            for num in range(0,len(goallist)): #Adds animation to the onscreen buttons
                goalactionlist.append(pykeyframe.Action(-1, GOALHEIGHT, 7))
                goalactionlist[num].render()
            menuselect = 0
            state = "menustart"
        if state =="newgame":
            pygame.mixer.music.load('../assets/BounceBGM.ogg')
            pygame.mixer.music.play()
            paddlecolorfade = pykeyframe.Action(colorlist[0], colorlist[0], 15)
            paddlecolorfade.render()
            
            paddle_height = 13
            paddle_width = 90
            
            paddle_center = (dispmidpointX, resY  - (paddle_width + 100))
            
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
            
            launcherY = 75 #Launchers always start 75 pixels from top of screen
            launcherX = 0
            launchtime = None
            launchdir = False
            
            score = 0
            consecutive = 0 #How many balls in a row did the user hit?
            strikes = 0 #How many times did user miss?
            strikelist = [] #List of strike "icons" to display on scoreboard
            for num in range(maxstrikes):
                strikelist.append(pykeyframe.Action(GREEN, RED, 10))
                strikelist[num].render()
            scorefont = pygame.font.Font(None, 80)
            scorelabel = scorefont.render("9001", 1, WHITE)
            pygame.mixer.music.play(-1)
            state = "play"
            ballGroup = []
            current_theta = 0
            target_theta = 0
            d_theta = 0
            paddlecolor = 0
            
            gameovercurtain.rewind()
            pausecurtain.rewind()
        
        #Display various overlay screens
        if state == "paused":
            SCREEN.blit(pausescreen, (0, pausecurtain.position))
        if "sure" in state or state == "paused":
            SCREEN.blit(confirmscreen, (0, confcurtain.position))
        if state =="gameover":
            SCREEN.blit(gameoverscreen, (0, gameovercurtain.position))
    #EVENT HANDLER CODE########
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN:
                keys = pygame.key.get_pressed()
                if isaMac:
                    if keys[K_LMETA] or keys[K_RMETA]:
                        if keys[K_q] or keys[K_w]:
                            pygame.quit()
                            sys.exit()
                else:
                    if keys[K_LCTRL] or keys[K_RCTRL]:
                        if keys[K_q] or keys[K_w]:
                            pygame.quit()
                            sys.exit()
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
                            paddlecolorfade.forget()
                            paddlecolorfade.rewind()
                            paddlecolorfade.start = colorlist[paddlecolor]
                            paddlecolor -= 1
                            if paddlecolor < 0:
                                paddlecolor = 3
                            paddlecolorfade.end = colorlist[paddlecolor]
                            paddlecolorfade.render()
                            paddlecolorfade.trigger()
                        elif keys[K_DOWN] and not keys[K_UP]:
                            paddlecolorfade.forget()
                            paddlecolorfade.rewind()
                            paddlecolorfade.start = colorlist[paddlecolor]
                            paddlecolor += 1
                            if paddlecolor > 3:
                                paddlecolor = 0
                            paddlecolorfade.end = colorlist[paddlecolor]
                            paddlecolorfade.render()
                            paddlecolorfade.trigger()
                            
                    elif keys[K_s] or keys[K_w]:
                        if keys[K_w] and not keys[K_s]: 
                            paddlecolorfade.forget()
                            paddlecolorfade.rewind()
                            paddlecolorfade.start = colorlist[paddlecolor]
                            paddlecolor -= 1
                            if paddlecolor < 0:
                                paddlecolor = 3
                            paddlecolorfade.end = colorlist[paddlecolor]
                            paddlecolorfade.render()
                            paddlecolorfade.trigger()
                        elif keys[K_s] and not keys[K_w]:
                            paddlecolorfade.forget()
                            paddlecolorfade.rewind()
                            paddlecolorfade.start = colorlist[paddlecolor]
                            paddlecolor += 1
                            if paddlecolor > 3:
                                paddlecolor = 0
                            paddlecolorfade.end = colorlist[paddlecolor]
                            paddlecolorfade.render()
                            paddlecolorfade.trigger()
                    elif keys[K_ESCAPE]:
                        state = "paused"
                elif state == "keys":
                    if keys[K_SPACE] or keys[K_RETURN]:
                        state = "logo"
                elif state == "logo" or state == "logofadeout": #Easter egg!
                    if keys[K_s] and keys[K_a] and keys[K_m]:
                        easteregg = "sam"
                        okay.play()
                        
                elif state == "menu": #Menu controls
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
                    if (keys[K_SPACE] or keys[K_RETURN]):
                        state += menu_options[menuselect]
                elif state == "menuscores":
                    if keys[K_UP] or keys[K_w] or keys[K_ESCAPE] or keys[K_DOWN] or keys[K_s]:
                        state = "menu"
                elif state == "menuabout":
                    if keys[K_LEFT] or keys[K_RIGHT]: #Directional control defaults to look for arrows before WASD
                        if keys[K_RIGHT] and not keys[K_LEFT]:
                            credits.step()
                        elif keys[K_LEFT] or keys[K_RIGHT]:
                            credits.backstep()
                    elif keys[K_a] or keys[K_d]:
                        if keys[K_d] and not keys[K_a]:  
                            credits.step()   
                        if keys[K_a] and not keys[K_d]: 
                            credits.backstep() 
                    elif keys[K_UP] or keys[K_w] or keys[K_ESCAPE] or keys[K_DOWN] or keys[K_s]:
                        state = "menu"
                        
                elif state =="gameover":
                    if keys[K_LEFT] or keys[K_RIGHT]: #Directional control defaults to look for arrows before WASD
                        if keys[K_RIGHT] and not keys[K_LEFT]:
                            state = "resetmenu"
                        elif keys[K_LEFT] or keys[K_RIGHT]:
                            state = "newgame"
                    elif keys[K_a] or keys[K_d]:
                        if keys[K_d] and not keys[K_a]:  
                            state = "resetmenu"   
                        if keys[K_a] and not keys[K_d]: 
                            state = "newgame"  
                elif state == "paused":
                    if keys[K_LEFT] or keys[K_RIGHT]: #Directional control defaults to look for arrows before WASD
                        if keys[K_LEFT] and not keys[K_RIGHT]:
                            state = "retrysure"
                        #if keys[K_RIGHT] and not keys[K_LEFT]:
                            
                    elif keys[K_a] or keys[K_d]:
                        if keys[K_a] and not keys[K_d]: 
                            state = "retrysure"
                        #if keys[K_d] and not keys[K_a]:
    
                    
                    if keys[K_UP] or keys[K_DOWN]: #Directional control defaults to look for arrows before WASD
                        if keys[K_UP] and not keys[K_DOWN]:
                            state = "play"
                        elif keys[K_DOWN] and not keys[K_UP]:
                            state = "quitsure"
                    elif keys[K_s] or keys[K_w]:
                        if keys[K_w] and not keys[K_s]: 
                            state = "play"
                        elif keys[K_s] and not keys[K_w]:
                            state = "quitsure"
                    elif keys[K_ESCAPE]:
                        state = "play"
                elif "sure" in state:
                    if keys[K_UP] or keys[K_DOWN]: #Directional control defaults to look for arrows before WASD
                        if keys[K_UP] and not keys[K_DOWN]:
                            if state == "quitsure":
                                state = "resetmenu"
                            elif state == "retrysure":
                                state = "newgame"
                            elif state == "clearsure":
                                pass
                            elif state =="exitsure":
                                pygame.quit()
                                sys.exit()
                        elif keys[K_DOWN] and not keys[K_UP]:
                            if state == "exitsure":
                                state = "menustart"
                            else:
                                state = "paused"
                    elif keys[K_s] or keys[K_w]:
                        if keys[K_w] and not keys[K_s]: 
                            if state == "quitsure":
                                state = "resetmenu"
                            elif state == "retrysure":
                                state = "newgame"
                            elif state == "clearsure":
                                pass
                            elif state =="exitsure":
                                pygame.quit()
                                sys.exit()
                        elif keys[K_s] and not keys[K_w]:
                            if state == "exitsure":
                                state = "menustart"
                            else:
                                state = "paused"
                    elif keys[K_ESCAPE]:
                        if state == "exitsure":
                            state = "menustart"
                            a = 1/0
                        else:
                            state = "paused"
            elif event.type == KEYUP:
                keys = event.key
                if state == "play":
                    if keys == K_LEFT or keys == K_RIGHT or keys == K_a or keys == K_d:
                        d_theta = 0
        clock.tick(framerate)
        pygame.display.flip()
        

    except Exception: #Hopefully none of this ever has to get executed :)
        exc_type, exc_obj, exc_tb = sys.exc_info()
        fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
        oops.append((exc_type, fname, exc_tb.tb_lineno))
        for errors in oops:
            if oops.count(errors) > 10: #Watchdog timer--set limit for how many exceptions to pass before throwing an error.
                whoopsfont = pygame.font.Font(None, 250) #Displays "WHOOPS! :P" on screen when an error occurs.
                whoopslabel = whoopsfont.render("WHOOPS! :P", 1, WHITE)
                whoopsrect = whoopslabel.get_rect()
                whoopsrect.center = (dispmidpointX, dispmidpointY)
                exceptfont = pygame.font.Font(None, 36) #Displays actual error
                exceptlabel = exceptfont.render("EXCEPTION IN MODULE: " + str(errors[0]) + ", LINE " + str(errors[2]) + " " + str(errors[1]), 1, WHITE)
                SCREEN.fill(BLACK)
                SCREEN.blit(whoopslabel, whoopsrect.topleft)
                SCREEN.blit(exceptlabel, (100, resY - 150))
                exceptlabel = exceptfont.render("PYTHON HAS ENCOUNTERED A PROBLEM AND NEEDS TO CLOSE. PRESS [ESC] TO EXIT...", 1, WHITE)
                SCREEN.blit(exceptlabel, (100, resY - 200))
                pygame.display.update()
                while True:
                    for event in pygame.event.get():
                        if event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE):
                            pygame.quit()
                            sys.exit()
                            


'''
    Coded with Class by the {CWC} Community in Greenwood, Indiana, USA
    
    Directed by Jiawei Chen, {CWC} Group Coordinator (a.k.a "theComputerNerd")
    Sound Design by Sarah Bucker
    Project Manager: Emily Simon
    Project Organizer: Austin Freay
    Communications Coordinator: Thomas Benkert
    Programming Advisor and Keeper of Sanity: Joseph "Joey" Martz
    Menu Artwork: Nathan Duke
    
    Music:
        From Freesound.org:
        "Night - Soft Techno" (BounceBGM.ogg) by edtijo
        "untitled.wav" (BounceMenu.ogg) by -zin-
    
        
        Composed by CodersWithClass{} in Audacity and are licensed under the Creative Commons Attribution License:
        "Complete.ogg"
        "Fail.ogg"
        "BounceLeft.ogg"
        "BounceRight.ogg" 
    
    =========================== MIT License Statement ===============================
    : Permission is hereby granted, free of charge, to any person obtaining a copy  :
    : of this software and associated documentation files (the "Software"), to deal :
    : in the Software without restriction, including without limitation the rights  :
    : to use, copy, modify, merge, publish, distribute, sublicense, and/or sell     :
    : copies of the Software, and to permit persons to whom the Software is         :
    : furnished to do so, subject to the following conditions:                      :
    :                                                                               :
    : The above copyright notice and this permission notice shall be included in    :
    : all copies or substantial portions of the Software.                           :
    :                                                                               :
    : THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR    :
    : IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,      :
    : FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE   :
    : AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER        :
    : LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, :
    : OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN     :
    : THE SOFTWARE.                                                                 :
    =================================================================================
    
    "Python" and the Python logos are trademarks or registered trademarks of the 
    Python Software Foundation, used by CodersWithClass{} with permission from the Foundation.
    
'''


#    Stay classy, and may the code be with you. 
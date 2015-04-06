import pygame, sys
from pygame.locals import *
pygame.init()
resX = 800
resY = 800
clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((resX, resY))
pygame.display.set_caption('Caption Goes Here')
WHITE = (255, 255, 255)
myFont = pygame.font.Font(None, 75)
buttonrect = pygame.Rect(75, 75, 100, 100)
buttoncolor = (0, 128, 0)
pressstep = 0

leftlimit = 50
rightlimit = 750



firstclicked = True
while True:
    SCREEN.fill(WHITE)
    pygame.draw.rect(SCREEN, (255, 0, 0), (0, 0, leftlimit, resY), 0)
    pygame.draw.rect(SCREEN, (255, 0, 0), (rightlimit, 0, resX - rightlimit, resY), 0)
    mouse = pygame.mouse.get_pos()

    if pressstep == 3:
        print("CLICK")
        pressstep = 0

    
    if buttonrect.collidepoint(mouse): #Only if the mouse is directly over the button
        if pygame.mouse.get_pressed()[0] == 0 and pressstep == 0:
            pressstep = 1
        if pressstep == 1:
            if pygame.mouse.get_pressed()[0] == 1:
                pressstep = 2
    
       
    

    else:
        if pressstep == 1:
            pressstep = 0
        if pressstep == 2 and pygame.mouse.get_pressed()[0] == 0:
            pressstep = 1
    if pressstep != 2:
            buttoncolor = (0, 128, 0)
            firstclicked = True


    if pressstep == 2:
            buttoncolor = (0, 255, 0)
            if firstclicked:
                pygame.mouse.get_rel()
                firstclicked = False
            else:
                movement = pygame.mouse.get_rel()
                buttonrect.left += movement[0]
 #               buttonrect.top += movement[1]
                if abs(movement[0]) > 0:
                    print("moving")
                
            if pygame.mouse.get_pressed()[0] == 0:
                pressstep = 3


    if buttonrect.left <= leftlimit:
        buttonrect.left = leftlimit
    elif buttonrect.right >= rightlimit:
        buttonrect.right = rightlimit
        
    label = myFont.render(str(pressstep), 1, (0, 0, 0))
    labelrect = label.get_rect()
    labelrect.center = buttonrect.center


        
    pygame.draw.rect(SCREEN, buttoncolor, buttonrect, 0)
    SCREEN.blit(label, (labelrect.topleft))
    
    if pressstep >= 1:
            pygame.draw.rect(SCREEN, (200, 200, 200), buttonrect, 3)
            

                
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    clock.tick(60)
    pygame.display.update()

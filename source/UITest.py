import pygame, sys
from pygame.locals import *
import pykeyframe
import pygame.gfxdraw
pygame.init()
resX = 1366
resY = 768
clock = pygame.time.Clock()
SCREEN = pygame.display.set_mode((resX, resY))
BLACK = (0 , 0, 0)
WHITE = (255, 255, 255)
pygame.display.set_caption('Caption Goes Here')

####ARROW MENU SETUP CODE################################################
arrowchoicefont = pygame.font.Font(None, 50)
titlefont = pygame.font.Font(None, 175)
dispmidpointX = int(resX / 2)
dispmidpointY = int(resY / 2)
arrowchoicelist = ["quit", "retry", "continue", "yes", "no"] #Creates the choices that appear on the "arrow menu"
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

confirmscreen = pygame.surface.Surface((resX, resY))
pausescreen = pygame.surface.Surface((resX, resY))

confcurtain = pykeyframe.Action(-resY, 0, 20)
pausecurtain = pykeyframe.Action(-resY, 0, 20)
confcurtain.render()
confcurtain.trigger()
pausecurtain.render()
pausecurtain.trigger()
####END ARROW MENU SETUP CODE################################################    
state = "paused" 
while True:
    SCREEN.fill(BLACK) 

    

    if state =="play":
        print("PLAYING GAME") 
    elif state == "retrysure" or state == "quitsure" or state =="clearsure":
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
        
        arrowlabelrectlist[4].centerx = dispmidpointX #no button
        arrowlabelrectlist[4].bottom = resY - 100
        confirmscreen.blit(arrowlabellist[4], arrowlabelrectlist[4].topleft)
        
        arrowlabelrectlist[3].centerx = dispmidpointX #yes button
        arrowlabelrectlist[3].top = 100
        confirmscreen.blit(arrowlabellist[3], arrowlabelrectlist[3].topleft)
    if state != "retrysure" and state != "quitsure" and state !="clearsure":
        confcurtain.trigger()
        confcurtain.done = False
        confcurtain.backstep()
        
        if state == "paused":
            #Pause Menu
            print("PAUSE")
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
            
            
            pygame.gfxdraw.aapolygon(pausescreen, ((resX - 10, dispmidpointY), #Rightwards-pointing arrow
                                              (resX - 80, dispmidpointY - 40),
                                              (resX - 80, dispmidpointY + 40)), WHITE) 
            pygame.gfxdraw.filled_polygon(pausescreen, ((resX - 11, dispmidpointY),
                                                   (resX - 79, dispmidpointY - 39),
                                                   (resX - 79, dispmidpointY + 39)), WHITE) 
            
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

    SCREEN.blit(pausescreen, (0, pausecurtain.position))
    SCREEN.blit(confirmscreen, (0, confcurtain.position))
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            keys = pygame.key.get_pressed()
            if state == "blag":
                "placeholder"
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
            else:
                if keys[K_UP] or keys[K_DOWN]: #Directional control defaults to look for arrows before WASD
                    if keys[K_UP] and not keys[K_DOWN]:
                        if state == "quitsure":
                            pass
                        elif state == "retrysure":
                            pass
                        elif state == "clearsure":
                            pass
                    elif keys[K_DOWN] and not keys[K_UP]:
                        state = "paused"
                elif keys[K_s] or keys[K_w]:
                    if keys[K_w] and not keys[K_s]: 
                        if state == "quitsure":
                            pass
                        elif state == "retrysure":
                            pass
                        elif state == "clearsure":
                            pass
                    elif keys[K_s] and not keys[K_w]:
                        state = "paused"
                elif keys[K_ESCAPE]:
                    state = "paused"
                
    clock.tick(120)
    pygame.display.update()

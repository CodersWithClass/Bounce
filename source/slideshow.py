#Creates a photo slideshow in Pygame.
import pygame
class Slideshow:
    def __init__(self, surface, width, height, piclist, start = 0, centered = False, wrap = True):
        self.piclist = piclist
        self.surflist = []
        self.rectlist = []
        self.slide = start
        self.screen = surface
        self.wrap = wrap
        self.centered = centered
        self.surface = pygame.surface.Surface((width, height))
        for num in range(len(self.piclist)):
            self.surflist.append(pygame.image.load(self.piclist[num]).convert())
            self.rectlist.append(self.surflist[num].get_rect())

    def display(self, coords):
        if not self.centered:
            self.surface.blit(self.surflist[self.slide], (0, 0))
        self.screen.blit(self.surface, coords)
        
    def step(self):#Advances the slideshow by one picture
        self.slide += 1
        if self.slide >= len(self.surflist):
            if self.wrap:
                self.slide = 0
            else:
                self.slide -= 1
            
    def backstep(self):
        self.slide -= 1
        if self.slide < 0:
            if self.wrap:
                self.slide = len(self.surflist) - 1
            else:
                self.slide += 1
            
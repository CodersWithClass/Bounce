import pygame
class Logger:
    def __init__(self, surf, logfile=None, fontsize = 20, maxlines = 10):
        self.maxlines = maxlines #Maximum number of lines to display
        self.buffer = [] #List containing lines to be written to display
        self.fontsize = fontsize 
        self.myFont = pygame.font.Font(None, fontsize)
        self.charheight = self.myFont.size('A')[1] + 1 #Amount of spacing between lines
        self.surf = surf
        #if logfile != None:#open log file
           # self.log = open(logfile, "a")
        self.color = (0, 0, 0)
        
    def log(self, text):
        self.buffer.insert(0, text)
        while len(self.buffer) > self.maxlines:
            del(self.buffer[-1])
        ycoord = 0
        xcoord = 0
        for items in self.buffer:
            label = self.myFont.render(str(items), 1, self.color) 
            self.surf.blit(label, (xcoord, ycoord))
            ycoord += self.charheight
            
            

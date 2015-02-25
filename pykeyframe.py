class Action:
    END = -1
    BEGIN = 0
    def __init__(self, start, end, frames, mode=1):
        self.start = start
        self.end = end
        self.frames = frames
        self.mode = mode
        self.frame = 0 #What frame the animator is on currently
        
        self.framelist = [] 
        self.current_frame = 0
        done = False #Has the animation reached the end of 
        rendered = False
    def render(self): #Loads up frame buffer with values for each frame--"bakes" actions to buffer
        something.do() #Please fill this in with actual code sometime.
        
    def step(self): #Advances frame buffer by one 
        something.do_some_more()
    
    def backstep(self): #Steps one frame backward in frame buffer
        something.do_in_reverse()
    
    def forget(self): #Drops baked frames and un-renders action--frees up resources if that's necessary.
        something.do_no_more()
    
    def reverse(self): #Reverses frame buffer. Current frame buffer position also reversed to correspond with new frame position
        something.do_backwards()
    
    def jumpto(self, frame): #Directly sets frame pointer to value. Setting it to END or BEGIN sets to end or beginning, respectively.
        something.do_to_frame()
class Action:
    def __init__(self, start, end, frames, mode=1):
        self.start = start
        self.end = end
        self.frames = frames
        self.mode = mode
        
        self.framelist = [] 
        self.current_frame = 0
        done = True
        
        
    def render(self):
        something.do()
        
    def trigger(self):
        something.do()
    
    def step(self):
        something.do_some_more()
    
    def backstep(self):
        something.do_in_reverse()
        
    def reset(self):
        something.do_from_zero()
    
    def forget(self):
        something.do_no_more()
    
    def reverse(self):
        something.do_backwards()

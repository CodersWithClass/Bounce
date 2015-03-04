import sys
import math
class KeyframeMismatchError(Exception):
    def __str__(self):
        return repr("Start and end value types don't match.")
class KeyframeInvalidType(Exception):
    def __str(self):
        return repr("Provided values cannot be animated.")
class Action:
    END = -1
    BEGIN = 0
    def __init__(self, start, end, frames, mode=1):
        self.start = start
        self.end = end
        self.num_frames = frames
        self.mode = mode #Interpolation Mode--for now it's only linear, but some more types are coming!
        self.frame = 0 #What frame the animator is on currently
        
        self.framelist = [] 
        self.current_frame = 0
        self.value = None #Value associated with current frame
        self.done = False #Has the animation reached the end of 
        self.rendered = False
        self.triggered = False
        self.position = None #Keyframed value that corresponds to the frame's animation
    def render(self): #Loads up frame buffer with values for each frame--"bakes" actions to buffer
        
        #These are error handlers that prevent animating invalid data types
        if type(self.start) != type(self.end): 
            raise KeyframeMismatchError()
        if type(self.start) is str or type(self.end) is str:
            raise KeyframeInvalidType()
        #End error handler
        if self.mode == 1:
            if type(self.start) is not tuple and type(self.start) is not list:
                temp = self.start
                for num in range(0, self.num_frames):
                    self.framelist.append(int(round(temp, 0))) #Only rounds right when value is being stored--that way we don't introduce uncertainties into the actual calculations
                    temp += ((self.end - self.start)/ ((self.num_frames - 1) * 1.0))
                    
            else:
                temp = list(self.start) #Stores mathematical results
                temp2 = list(self.start) #Stores int-converted results since Pygame and many other graphics programs can't take longs or floats for values.
                for num in range(0, self.num_frames):
                    #Builds up current frame value by iterating through and animating 
                    #each element of list or tuple individually
                    self.framelist.append(list(temp2))
                    for i in range(0, len(temp)):
                        temp[i] += ((self.end[i] - self.start[i]) / 
                                         ((self.num_frames - 1) * 1.0))
                    for i in range(0, len(temp)):
                        temp2[i] = int(round(temp[i], 0))
                        
        self.position = self.framelist[0]
                    
        self.rendered = True
    def trigger(self): #Call this to initiate the animation
        self.triggered = True
        
    def step(self): #Advances frame buffer by one 
        if self.triggered and not self.done:
            
            if self.frame < self.num_frames - 1:
                self.frame += 1
                self.position = self.framelist[self.frame]
            else:
                self.done = True
                self.triggered = False
    def backstep(self): #Steps one frame backward in frame buffer
        if self.triggered and not self.done:
            
            if self.frame > 0:
                self.frame -= 1
                self.position = self.framelist[self.frame]
            else:
                self.done = True
                self.triggered = False
    
    def forget(self): #Drops baked frames and un-renders action--frees up resources if that's necessary.
        self.framelist = []
    
    def reverse(self): #Reverses frame buffer. Current frame buffer position also reversed to correspond with new frame position
        self.framelist.reverse()
        self.position = (len(self.framelist) - 1) - self.position
    
    def jumpto(self, frame): #Directly sets frame pointer to value. Setting it to END or BEGIN sets to end or beginning, respectively.
        self.position = frame
        
##Test code to spit out a keyframe list        
myAction = Action((25, 0, 25), (0, 25, 25), 50)
myAction.render()
myAction.trigger()
while not myAction.done:
    print(myAction.position)
    myAction.step()
print(len(myAction.framelist))
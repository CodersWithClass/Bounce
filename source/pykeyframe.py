##IMPORTANT! FRAME COUNTER STARTS AT ZERO!
import sys
import math
class KeyframeMismatchError(Exception):
    def __str__(self):
        return repr("Start and end value types don't match.")
class KeyframeInvalidType(Exception):
    def __str(self):
        return repr("Provided values cannot be animated.")
class ActionNotRendered(Exception):
    def __str(self):
        return repr("Action was not yet rendered.")
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
        self.position = start #Keyframed value that corresponds to the frame's animation
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
    def trigger(self): #Call this to initiate the animation. You can keep calling this forever; it's one-shot.
        if self.rendered:
            self.triggered = True
        else:
            raise ActionNotRendered()
        
    def step(self): #Advances frame buffer by one. Since animations require an event to be triggered, you can keep calling this function forever and nothing will happen unless you trigger it.
        if self.triggered and not self.done and self.rendered:
            
            if self.frame < self.num_frames - 1:
                self.frame += 1
                self.position = self.framelist[self.frame]
            else:
                self.done = True
                self.triggered = False
        elif not self.rendered:
            raise ActionNotRendered()
            
    def backstep(self): #Steps one frame backward in frame buffer
        if self.triggered and not self.done and self.rendered:
            
            if self.frame > 0:
                self.frame -= 1
                self.position = self.framelist[self.frame]
            else:
                self.done = True
                self.triggered = False
        elif not self.rendered:
            raise ActionNotRendered()
    
    def forget(self): #Drops baked frames and un-renders action--frees up resources if that's necessary.
        self.framelist = []
        self.rendered = False
        self.triggered = False
        self.done = False
    
    def reverse(self): #Reverses frame buffer. Current frame buffer position also reversed to correspond with new frame position
        if self.rendered:
            self.framelist.reverse()
            self.frame = (len(self.framelist) - 1) - self.frame
        else:
            raise ActionNotRendered()
    
    def jumpto(self, frame): #Directly sets frame pointer to value. Setting it to END or BEGIN sets to end or beginning, respectively.
        if self.rendered:
            self.frame = frame
        else:
            raise ActionNotRendered()
    def rewind(self): #Resets frame counter and un-triggers the animation
        self.frame = 0
        self.triggered = False
        self.done = False

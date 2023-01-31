import GenericPipe
import math
class SandFilter(GenericPipe):

    def __init__(self, id_num, inputs, outputs, length):
        if len(self.inputs) != 1 or len(self.outputs) == 2:
            print("Error: Bad Inputs / Outputs.")
            return 
        
        self.normalPipe = outputs[0]
        self.backwashPipe = outputs[1]
        self.output = self.normalPipe
        self.height = self.length
        self.sandHeight = self.height / 2 # arbitrary
        self.backwash = False 
        self.maxVolume = 100 # arbitrary
        self.valve = False 
        self.capacity = 0 
        self.radius = 5 # arbitrary
        self.time = 0 
        

    def waterVelocity(self):
        waterHeight = self.capacity / (math.pi * (self.radius ** 2))
        return math.sqrt(2 * 9.807 * waterHeight)

    def push(self, flowi_in, time: int):
        self.sandHeight += 1 # incrementing amount of particulate in system, should be based on level of particulate in water
        self.maxVolume -= math.pi * (self.radius ** 2)
        self.capacity += flowi_in

        if self.sandHeight > 10: # arbitrary boundary to start backwash
            backwash = True
            self.output = self.backwashPipe
            self.inputs[0].toggle_valve()

        flowOut = self.waterVelocity() * self.output.getArea() # get area will get crossectional area of the pipe (or it can be calculated this side)
        self.output.push(flowOut) # pushes flow out to the output pipe

        self.capacity -= flowOut
        # haven't messed with time yet, will ask Leo how he's doing time before trying it

    def snapshot(self, snap_dict):
        snap_dict[self.id_num] = (self.time, self.capacity, self.backwash, self.sandHeight)  # adds self to dictionary

        for child_pipe in self.outputs:
            child_pipe.snap(snap_dict)

        return snap_dict
        

        


        
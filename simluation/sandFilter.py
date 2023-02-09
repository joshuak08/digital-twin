import GenericPipe
import math
class SandFilter(GenericPipe):

    def __init__(self, id_num, inputs, outputs, length, tickLength):
    
        if len(self.inputs) != 1 or len(self.outputs) == 2:
            print("Error: Bad Inputs / Outputs.")
            return 
        
        self.input = inputs[0] # intake for the tank
        self.normalPipe = outputs[0] # default pipe for cleaned water
        self.backwashPipe = outputs[1] # pipe to output wash water
        self.output = self.normalPipe # current output of the tank
        self.height = length # height of the tank
        self.sandHeight = self.height / 2 # arbitrary, current height of sand in the tank
        self.backwash = False # whether or not the tank is currently backwashing
        self.maxVolume = 100 # max volume of the tank
        self.valve = False # whether or not the tank is shut
        self.capacity = 0 # current volume of liquid in the tank
        self.radius = 5 # arbitrary
        self.tickLength = tickLength # length of each round in seconds
        # will likely be pre-set, user just decides how often a snapshot is taken

        self.id = id_num # id of the component, used for snapshotting
        

    def waterVelocity(self):
        waterHeight = self.capacity / (math.pi * (self.radius ** 2))
        return math.sqrt(2 * 9.807 * waterHeight)

    def push(self, flowi_in):
        self.sandHeight += 1 # incrementing amount of particulate in system, should be based on level of particulate in water and flow in
        self.maxVolume -= math.pi * (self.radius ** 2)
        self.capacity += flowi_in

        if self.sandHeight > 10: # arbitrary boundary to start backwash
            self.backwash = True
            self.output = self.backwashPipe
            self.input.toggle_valve()

        flowOut = self.waterVelocity() * self.output.getArea() * self.tickLength # get area will get crossectional area of the pipe (or it can be calculated this side)
        self.output.push(flowOut) # pushes flow out to the output pipe

        self.capacity -= flowOut

    def snapshot(self, snap_dict):
        snap_dict[self.id_num] = (self.time, self.capacity, self.backwash, self.sandHeight)  # adds self to dictionary

        for child_pipe in self.outputs:
            child_pipe.snap(snap_dict)

        return snap_dict
        

        


        
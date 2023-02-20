import GenericPipe
import math
class SandFilter(GenericPipe.GenericPipe):

    def __init__(self, id_num, num_of_inputs, outputs, length, tick_length, radius):
    
        if num_of_inputs != 1 or len(outputs) != 2:
            print("Error: Bad Inputs / Outputs.")
            return 
        
        self.num_of_inputs = num_of_inputs # intake for the tank
        self.normal_pipe = outputs[0] # default pipe for cleaned water
        self.backwash_pipe = outputs[1] # pipe to output wash water
        self.output = self.normal_pipe # current output of the tank
        self.height = length # height of the tank
        self.particulate_mass = 0 # mass of particulate currently captured in the sand
        self.backwash = False # whether or not the tank is currently backwashing
        self.max_volume = 100 # max volume of the tank
        self.valve = False # whether or not the tank is shut
        self.capacity = 0 # current volume of liquid in the tank
        self.radius = radius # radius of the tank in metres
        self.tick_length = tick_length # length of each round in seconds
        self.radius = radius
        self.input = None 
        # will likely be pre-set, user just decides how often a snapshot is taken

        self.id = id_num # id of the component, used for snapshotting
        
        self.backwash_timer = 0
        # Numbers for a standard Sand Filter
        # Diameter = 3m
        # Height of tank area ~= 8m (ish)
        # Hydraulic Capacity = 71 m^3 / hr (71,000 litres)
        # Particulate (TSS) capacity = 2.33kg (average wastewater has 155 - 330mg /L, or 11 - 23 kg / hr)
        # Limiting factor will then be amount of TSS in the water

    def set_input(self, input_pipe):
        self.input = input_pipe

    def water_velocity(self):
        water_height = self.capacity / (math.pi * (self.radius ** 2))
        return math.sqrt(2 * 9.807 * water_height)

    def push(self, flow_in):
        
        self.particulate_mass += flow_in * 252 # incrementing amount of particulate in system, should be based on level of particulate in water and flow in
        self.max_volume -= math.pi * (self.radius ** 2)
        self.capacity += flow_in

        if self.particulate_mass > 500000: # arbitrary boundary to start backwash - 500g of particulate collected
            self.backwash = True
            self.output = self.backwash_pipe
            self.input.toggle_valve()
            self.backwash_timer = 180 / self.tick_length
        
        if self.backwash:
            self.backwash_timer -= 1
            self.normal_pipe.push(0)
            if self.backwash_timer == 0:
                self.backwash = False
                self.particulate_mass = 0
                self.input.toggle_valve()

        else:
            self.backwash_pipe.push(0)

        flow_out = self.water_velocity() * self.output.cs_area * self.tick_length # get area will get crossectional area of the pipe (or it can be calculated this side)
        self.output.push(flow_out) # pushes flow out to the output pipe

        self.capacity -= flow_out

        if not self.backwash:
            self.output = self.normal_pipe

    def snapshot(self, snap_dict, snap_num):
        snap_dict[self.id_num] = (snap_num, (self.capacity, self.backwash, self.sand_height))  # adds self to dictionary

        for child_pipe in self.outputs:
            child_pipe.snap(snap_dict)

        return snap_dict
        

        


        
import GenericPipe
import math

# class to represent a Sand Filter (based off of Nijhuis CSF 300)
class SandFilter(GenericPipe.GenericPipe):

    # initialisation for a sand filter is quite different to a regular pipe, so parents initialiser is not used
    def __init__(self, id_num, num_of_inputs, outputs, length, tick_length, radius):
        
        # sand filters have specific configuratiosn
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
        self.valve = False # whether or not the tank is shut
        self.capacity = 0 # current volume of liquid in the tank
        self.radius = radius # radius of the tank in metres
        self.tick_length = tick_length # length of each round in seconds
        self.radius = radius
        self.input = None 
        self.max_volume = self.height * (math.pi * (self.radius ** 2)) # max volume of the tank

        self.id = id_num # id of the component, used for snapshotting
        
        self.backwash_timer = 0

        # Numbers for a standard Sand Filter
        # Diameter = 3m
        # Height of tank area ~= 8m (ish)
        # Hydraulic Capacity = 71 m^3 / hr (71,000 litres)
        # Particulate (TSS) capacity = 2.33kg (average wastewater has 155 - 330mg /L, or 11 - 23 kg / hr)
        # Limiting factor will then be amount of TSS in the water

    # since inputs aren't necessarily defined when sand filter is defined, there's a method to add them
    def set_input(self, input_pipe):
        self.input = input_pipe

    # calculates the velocity of water leaving out the bottom of the tank, based on the amount of water currently 
    # in the tank
    # (a more realistic simulation would take into account the amount of particluate collected)
    def water_velocity(self):
        water_height = self.capacity / (math.pi * (self.radius ** 2))
        return math.sqrt(2 * 9.807 * water_height)

    # pushing for a sand filter
    def push(self, flow_in, flow_tss):
        
        # updates it's state based on the flow pushed into it
        self.particulate_mass += flow_in * flow_tss * 1000 # incrementing amount of particulate in system, should be based on level of particulate in water and flow in
        self.capacity += flow_in

        # if it's caught a certain amount of particulate it goes into backwash
        if self.particulate_mass > 500000: # arbitrary boundary to start backwash - 500g of particulate collected
            self.backwash = True
            self.output = self.backwash_pipe
            self.input.toggle_valve()
            self.backwash_timer = 180 / self.tick_length
        
        # if in a backwash, decrement backwash timer, and do an empty push to regular input 
        if self.backwash:
            self.backwash_timer -= 1
            self.normal_pipe.push(0, flow_tss)
            if self.backwash_timer == 0:
                self.backwash = False
                self.particulate_mass = 0
                self.input.toggle_valve()

        # if not in a regular backwash do an empty push to backwash pipe
        else:
            self.backwash_pipe.push(0, flow_tss)

        # push flow to current output based on water velocity and the size of the pipe being pushed to
        flow_out = self.water_velocity() * self.output.cs_area * self.tick_length 
        self.output.push(flow_out, flow_tss) # pushes flow out to the output pipe

        # update capacity accordingly
        self.capacity -= flow_out

        # if not in a backwash, then output is set to be normal_pipe (this is important just after a backwash has ended)
        if not self.backwash:
            self.output = self.normal_pipe

    def snapshot(self):
        data = (self.capacity, self.particulate_mass, self.backwash)
        

        


        

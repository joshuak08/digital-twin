import GenericPipe
import math

# Q = av where Q is the flow rate, a = cross-sectional area, v = velocity of water

# class for a basic pipe with any number of outputs or inputs
class SplitterPipe(GenericPipe.GenericPipe):

    # initialises the same as generic pipe, but has a few more things to keep track of 
    def __init__(self, id_num, num_of_inputs, outputs, length, tick_length, radius):
        
        super().__init__(id_num, num_of_inputs, outputs, length, tick_length, radius)

        # to handle having multiple inputs the pipe won't continue until it's been pushed to by all children
        self.pushes_in_current_round = 0
        self.flow_in_current_round = 0
        self.output_ratios = []
        self.type = "Splitter"
        
    
    # method to decide how much flow should be pushed to each output, based on the radius of each output
    # if an output is closed it is not brought into these calculations
    def get_output_ratios(self):
        total_radius = 0
        for i in self.outputs:
            if i.valve == False:
                total_radius += i.radius 
        if total_radius == 0:
            total_radius = 1
        for i in self.outputs:
            numerator = i.radius
            if i.valve == True:
                numerator = 0
            self.output_ratios.append(numerator / total_radius)


    # ======== override methods ======== #
    # pushing for a splitter 
    def push(self, flow_in, flow_tss):

        # waits to be pushed to by all inputs before pushing out
        self.pushes_in_current_round += 1
        self.flow_in_current_round += flow_in

        if self.pushes_in_current_round == self.num_of_inputs:

            # once pushed to by all inputs it pushes to all of it's ouputs based on output ratios
            self.get_output_ratios()
            flow_out = 0
            for i in range(0, len(self.outputs)):
                flow = self.flow_in_current_round * self.output_ratios[i]
                flow_out += flow
                self.outputs[i].push(flow, flow_tss)
            self.pushes_in_current_round = 0
            self.flow_in_current_round = 0

            self.capacity += (flow_in - flow_out)
        
        # if the pipe is not able to push out the flow pushed into it then bad things happen
        if self.capacity > self.max_volume:
            raise Exception("capacity is greater than max volume :(")
    # ================================== #

    # important information for a pipe is how much liquid it has in it and whehter or not it has been closed
    def snapshot(self):
        data = (self.capacity, self.valve)
        return data

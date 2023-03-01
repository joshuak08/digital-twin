import GenericPipe
import math

# Q = av where Q is the flow rate, a = cross-sectional area, v = velocity of water

class SplitterPipe(GenericPipe.GenericPipe):
    def __init__(self, id_num, num_of_inputs, outputs, length, tick_length, radius):
        super().__init__(id_num, num_of_inputs, outputs, length, tick_length, radius)
        self.pushes_in_current_round = 0
        self.flow_in_current_round = 0
        self.output_ratios = []
        
        
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
    def push(self, flow_in):

        #TODO add condition for valve closure to output rate as well
        self.pushes_in_current_round += 1
        self.flow_in_current_round += flow_in

        if self.pushes_in_current_round == self.num_of_inputs:
            self.get_output_ratios()
            flow_out = 0
            for i in range(0, len(self.outputs)):
                flow = self.flow_in_current_round * self.output_ratios[i]
                flow_out += flow
                self.outputs[i].push(flow)
            self.pushes_in_current_round = 0
            self.flow_in_current_round = 0

            self.capacity += (flow_in - flow_out)
        if self.capacity > self.max_volume:
            raise Exception("capacity is greater than max volume :(")
    # ================================== #

    def snapshot(self, snap_dict, snap_num):
        
        # returns a dictionary of pipe id's as keys with their value being a tuple of time and capacity
        snap_dict[self.id_num] = (snap_num, self.capacity)  # adds self to dictionary with time and capacity

        for child_pipe in self.outputs:
            child_pipe.snapshot(snap_dict, snap_num)

        return snap_dict
    # ================================== #

    def toggle_valve(self):
        #TODO
        pass
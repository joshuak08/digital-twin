from GenericPipe import GenericPipe


# Q = av where Q is the flow rate, a = cross-sectional area, v = velocity of water

class SplitterPipe(GenericPipe):
    def __init__(self, id_num, inputs, outputs, length, tickLength):
        super().__init__(id_num, inputs, outputs, length, tickLength)

    # ======== override methods ======== #
    def push(self, flow_in):

        #TODO add condition for valve closure to output rate as well
        self.capacity += (flow_in - self.outputRate*len(self.outputs))  # increase capacity difference of input and output

        if self.capacity > self.maxVolume:
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
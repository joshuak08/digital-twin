from GenericPipe import GenericPipe


# Q = av where Q is the flow rate, a = cross-sectional area, v = velocity of water

class SplitterPipe(GenericPipe):
    def __init__(self, id_num, inputs, outputs, length):
        super().__init__(id_num, inputs, outputs, length)

    # ======== override methods ======== #
    def push(self, flow_in, time):
        # TODO THIS IS JUST EXAMPLE CODE currently DOES NOT DO TIME PROPERLY, we need all components to keep track of
        #  the oldest time (perhaps by pointer) although time may not even matter

        self.time = max(time, self.time) + 1  # increases time by 1 after a push

        # TODO add condition for valve closure to output rate as well
        self.capacity += (
                    flow_in - self.outputRate * len(self.outputs))  # increase capacity difference of input and output

        if self.capacity > self.maxVolume:
            raise Exception("capacity is greater than max volume :(")

        for child_pipe in self.outputs:  # iterates through all output pipes
            self.time = max(self.time, child_pipe.push(self.outputRate,
                                                       self.time))  # updates current time with oldest time and pushes flow

    # ================================== #

    def snapshot(self, snap_dict):
        # TODO
        # currently incorrect, we want to take the largest time of any component after a push is done
        # returns a dictionary of pipe id's as keys with their value being a tuple of time and capacity
        snap_dict[self.id_num] = (self.time, self.capacity)  # adds self to dictionary with time and capacity

        for child_pipe in self.outputs:
            child_pipe.snap(snap_dict)

        return snap_dict

    # ================================== #

    def toggle_valve(self):
        # TODO
        pass

from GenericPipe import GenericPipe
import math


# Q = av where Q is the flow rate, a = cross-sectional area, v = velocity of water

class SplitterPipe(GenericPipe):
    def __init__(self, id_num, inputs, outputs, length):
        if len(self.inputs) == 0 or len(self.outputs) == 0:
            raise Exception("missing an input/output")
        else:
            super().__init__(id_num, inputs, outputs, length)
            self.radius = 1  # arbitrary

    # ================================== #
    def push(self, flow_in, time):
        # TODO THIS IS JUST EXAMPLE CODE currently DOES NOT DO TIME PROPERLY, we need all components to keep track of
        #  the oldest time (perhaps by pointer) although time may not even matter if we just pick the oldest time in
        #  c columns

        self.time = max(time, self.time) + 1  # increases time by 1 after a push

        self.maxVolume -= math.pi * (self.radius ** 2)
        self.capacity += flow_in  # increase capacity difference of input and output

        for child_pipe in self.outputs:
            if child_pipe.valve:  # if the valve isn't closed remove
                self.capacity -= child_pipe.outputRates

        if self.capacity > self.maxVolume or self.capacity < 0:
            raise Exception("capacity is out of bounds")

        for child_pipe in self.outputs:  # iterates through all output pipes
            if child_pipe.valve:
                child_pipe.push(self.outputRate, self.time)  # pushes flow down every child pipe

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
        self.valve = not self.valve

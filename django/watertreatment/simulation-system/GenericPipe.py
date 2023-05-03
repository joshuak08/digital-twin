from abc import ABC, abstractmethod
import math

# abstract class to define how pipes should behave in general


class GenericPipe(ABC):

    # all pipes will have the same parameters, so parameter assignment can be handled in parent method
    def __init__(self, id_num, num_of_inputs, outputs, length, tick_length, radius):
        self.id_num = id_num
        self.outputs = outputs  # outputs of pipe
        self.length = length    # length of pipe
        self.max_volume = 8   # maximum volume of pipe m^3
        self.capacity = 0       # current capacity of pipe
        self.valve = False
        self.tick_length = tick_length  # length of each round in seconds
        self.radius = radius  # diameter of the pipe
        self.num_of_inputs = num_of_inputs
        self.cs_area = math.pi * (self.radius ** 2)
        self.type = "GenericPipe"

    # method to push flow into a pipe - takes the amount of flow in m^3, and tss of the water in mg/m^3
    # each type of pipe will handle pushing differently, so this is implemented by children
    @abstractmethod
    def push(self, flow_in, flow_tss):  # pushes water down pipe on a single tick
        pass

    # snapshotting method to save information about the simulation
    # each child should implement this to return the important information about that component in a tuple
    @abstractmethod
    def snapshot(self, snap_num):  # takes snapshot of pipe and stores it in a db
        pass

    # method to simulate turning a valve on a pipe
    # behaviour here is universal, so is defined by parent
    def toggle_valve(self):
        self.valve = not self.valve

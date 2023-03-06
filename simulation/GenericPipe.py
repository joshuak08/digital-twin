from abc import ABC, abstractmethod
import math

class GenericPipe(ABC):
    def __init__(self, id_num, num_of_inputs, outputs, length, tick_length, radius):
        self.id_num = id_num
        self.outputs = outputs  # outputs of pipe
        self.length = length    # length of pipe
        self.max_volume = 8   # maximum volume of pipe m^3
        self.capacity = 0       # current capacity of pipe
        self.valve = False
        self.tick_length = tick_length # length of each round in seconds
        self.radius = radius # diameter of the pipe
        self.num_of_inputs = num_of_inputs
        self.cs_area = math.pi * (self.radius ** 2)
        self.type = "GenericPipe"

    @abstractmethod
    def push(self, flow_in) -> int:  # pushes water down pipe on a single tick
        pass

    @abstractmethod
    def snapshot(self, snap_dict: dict, snap_num: int) -> dict:  # takes snapshot of pipe and stores it in a db
        pass

    def toggle_valve(self):
        self.valve = not self.valve



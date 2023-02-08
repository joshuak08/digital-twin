from abc import ABC, abstractmethod


class GenericPipe(ABC):
    def __init__(self, id_num, inputs, outputs, length, tickLength):
        self.id_num = id_num
        self.inputs = inputs  # inputs of pipe
        self.outputs = outputs  # outputs of pipe
        self.length = length    # length of pipe
        self.outputRate = sum(inputX.outputRate for inputX in inputs) / outputs  # sum of all input rates divided by outputs
        self.maxVolume = 8   # maximum volume of pipe m^3
        self.capacity = 0       # current capacity of pipe
        self.valve = False
        self.tickLength = tickLength # length of each round in seconds

    @abstractmethod
    def push(self, flowi_in) -> int:  # pushes water down pipe on a single tick
        pass

    @abstractmethod
    def snapshot(self, snap_dict: dict, snap_num: int) -> dict:  # takes snapshot of pipe and stores it in a db
        pass

    def toggle_valve(self):
        self.valve = not self.valve



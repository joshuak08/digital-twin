from abc import ABC, abstractmethod


class genericPipe(ABC):
    def __init__(self, inputs, outputs, length):
        self.inputs = inputs  # inputs of pipe
        self.outputs = outputs  # outputs of pipe
        self.length = length    # length of pipe
        self.maxVolume = None   # maximum volume of pipe
        self.capacity = 0       # current capacity of pipe

    @abstractmethod
    def push(self):  # pushes water down pipe on a single tick
        pass

    @abstractmethod
    def snapshot(self):  # takes snapshot of pipe and stores it in a db
        pass



import abc 

import SplitterPipe
import SandFilter
import Sink
import Source

class SimulationSystem(abc.ABC):

    @abc.abstractclassmethod
    def __init__(self, tick_length, average_flow, average_tss, snapshotter, total_rounds, snapshot_frequency, take_snapshots):

        self.tick_length = tick_length
        self.average_flow = average_flow
        self.average_tss = average_tss
        self.snapshotter = snapshotter
        self.total_rounds = total_rounds
        self.snapshot_frequency = snapshot_frequency
        self.take_snapshots = take_snapshots

        self.round = 0
        self.source = None 
        self.sink = None 
        self.finished = False
        self.components = []

    def simulate(self):
        for i in range(self.total_rounds):
            
            if self.round % self.snapshot_frequency == 0 and self.take_snapshots:
                self.snapshotter.snapshot(self.source)
            
            self.take_round()


    @abc.abstractclassmethod
    def take_round(self):

        if self.round % self.snapshot_frequency == 0 and self.take_snapshots:
            self.snapshotter.snapshot(self.source)

        self.round += 1

        if self.round > self.total_rounds:
            self.finished = True 
    
    def add_component(self, num_of_inputs, outputs, length, tick_length, radius, type):

        id_num = len(self.components)
        if type == "pipe":
            component = SplitterPipe.SplitterPipe(id_num, num_of_inputs, outputs, length, tick_length, radius)
        if type == "filter":
            component = SandFilter.SandFilter(id_num, num_of_inputs, outputs, length, tick_length, radius)
        if type == "sink":
            component = Sink.Sink(id_num, num_of_inputs, outputs, length, tick_length, radius, self)
        if type == "source":
            component = Source.Source(id_num, num_of_inputs, outputs, length, tick_length, radius)

        self.components.append(component)

        return component




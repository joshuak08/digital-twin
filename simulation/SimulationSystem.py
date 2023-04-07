import abc 

import SplitterPipe
import SandFilter
import Sink
import Source

# generic class for a simulation system - gives the framework for other systems to build off of
class SimulationSystem(abc.ABC):

    # abstract initialisier covers the assignment of simulation parameters, but not the setup of system components
    # children can extend this method to set up specific systems
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

    # simulation on a system consists of taking a number of rounds specified in system parameters
    # system specific behaviour is handled by take_round
    def simulate(self):
        for i in range(self.total_rounds):

            if self.round % self.snapshot_frequency == 0 and self.take_snapshots:
                self.snapshotter.snapshot(self)
            
            self.take_round()

    # abstract method for processing of each round - each system may do different things on each rounds, 
    # so will implement this method themselves
    @abc.abstractclassmethod
    def take_round(self):
        pass
    
    # method to add a component to a system - keeps a track of component ids so they will all be unique
    # returns the new component so that the caller can use it
    # pass the parameters for the new component (excluding id_num), and the type of component (i.e. class)
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




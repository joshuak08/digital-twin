import abc 

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

    @abc.abstractclassmethod
    def take_round(self):

        if self.round % self.snapshot_frequency == 0 and self.take_snapshots:
            self.snapshotter.snapshot(self.source)

        self.round += 1

        if self.round > self.total_rounds:
            self.finished = True 
         




import SimulationSystem
import Sink
import SplitterPipe

class FilterSystem(SimulationSystem.SimulationSystem):

    def __init__(self, tick_length, average_flow, average_tss, snapshotter, total_rounds, snapshot_frequency, take_snapshots):
        super.__init__(self, tick_length, average_flow, average_tss, snapshotter, total_rounds, snapshot_frequency, take_snapshots)
        self.sink = Sink.Sink(0, 8, [], 1, self.tick_length, 1, self)
        self.add_component(self.sink)

        out_1 = SplitterPipe.SplitterPipe(0, 1, [self.sink], 0.5, self.tick_length, 0.1)
        self.add_component(out_1)
        out_2 = SplitterPipe.SplitterPipe(0, 1, [self.sink], 0.5, self.tick_length, 0.1)
        self.add_component(out_2)
        out_3 = SplitterPipe.SplitterPipe(0, 1, [self.sink], 0.5, self.tick_length, 0.1)
        self.add_component(out_3)
        out_4 = SplitterPipe.SplitterPipe(0, 1, [self.sink], 0.5, self.tick_length, 0.1)
        self.add_component(out_4)

        back_1 = SplitterPipe.SplitterPipe(0, 1, [self.sink], 0.5, self.tick_length, 0.1)
        self.add_component(back_1)
        back_2 = SplitterPipe.SplitterPipe(0, 1, [self.sink], 0.5, self.tick_length, 0.1)
        self.add_component(back_2)
        back_3 = SplitterPipe.SplitterPipe(0, 1, [self.sink], 0.5, self.tick_length, 0.1)
        self.add_component(back_3)
        back_4 = SplitterPipe.SplitterPipe(0, 1, [self.sink], 0.5, self.tick_length, 0.1)
        self.add_component(back_4)


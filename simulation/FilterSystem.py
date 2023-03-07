import SimulationSystem
import Sink
import SplitterPipe

class FilterSystem(SimulationSystem.SimulationSystem):

    def __init__(self, tick_length, average_flow, average_tss, snapshotter, total_rounds, snapshot_frequency, take_snapshots):
        super.__init__(self, tick_length, average_flow, average_tss, snapshotter, total_rounds, snapshot_frequency, take_snapshots)

        self.sink = self.add_component(8, [], 1, self.tick_length, 1, "sink")

        out_1 = self.add_component(1, [self.sink], 0.5, self.tick_length, 0.1, "pipe")
        out_2 = self.add_component(1, [self.sink], 0.5, self.tick_length, 0.1, "pipe")
        out_3 = self.add_component(1, [self.sink], 0.5, self.tick_length, 0.1, "pipe")
        out_4 = self.add_component(1, [self.sink], 0.5, self.tick_length, 0.1, "pipe")

        back_1 = self.add_component(1, [self.sink], 0.5, self.tick_length, 0.1, "pipe")
        back_2 = self.add_component(1, [self.sink], 0.5, self.tick_length, 0.1, "pipe")
        back_3 = self.add_component(1, [self.sink], 0.5, self.tick_length, 0.1, "pipe")
        back_4 = self.add_component(1, [self.sink], 0.5, self.tick_length, 0.1, "pipe")

        filter_1 = self.add_component(1, [out_1, back_1], 8, self.tick_length, 1.5, "filter")
        filter_2 = self.add_component(1, [out_2, back_2], 8, self.tick_length, 1.5, "filter")
        filter_3 = self.add_component(1, [out_3, back_3], 8, self.tick_length, 1.5, "filter")
        filter_4 = self.add_component(1, [out_4, back_4], 8, self.tick_length, 1.5, "filter")

        in_1 = self.add_component(1, [filter_1], 0.5, self.tick_length, 0.1, "pipe")
        in_2 = self.add_component(1, [filter_2], 0.5, self.tick_length, 0.1, "pipe")
        in_3 = self.add_component(1, [filter_3], 0.5, self.tick_length, 0.1, "pipe")
        in_4 = self.add_component(1, [filter_4], 0.5, self.tick_length, 0.1, "pipe")

        left_end = self.add_component(1, [in_1], 3, self.tick_length, 0.1, "pipe")
        left_start = self.add_component(1, [left_end, in_2], 3, self.tick_length, 0.1, "pipe")

        right_end = self.add_component(1, [in_4], 3, self.tick_length, 0.1, "pipe")
        right_start = self.add_component(1, [right_end, in_3], 3, self.tick_length, 0.1, "pipe")

        main_in = self.add_component(1, [left_start, right_start], 3, self.tick_length, 0.1, "pipe")

        self.source = self.add_component(1, [main_in], 1, self.tick_length, 1, "source")


    def take_round(self):
        self.source.push(self.average_flow, self.average_tss)
        

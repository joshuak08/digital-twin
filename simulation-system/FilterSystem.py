import SimulationSystem


# implementation of a simulation system specific to our 4-tank system


class FilterSystem(SimulationSystem.SimulationSystem):

    # initialisation does basic system setup, then sets up the system specific components
    def __init__(self, tick_length, average_flow, average_tss, snapshotter, total_rounds, snapshot_frequency, take_snapshots):
        super().__init__(tick_length, average_flow, average_tss,
                         snapshotter, total_rounds, snapshot_frequency, take_snapshots)

        # initialising sink
        self.sink = self.add_component(8, [], 1, self.tick_length, 1, "sink")

        # initialising sand filter outputs
        out_1 = self.add_component(
            1, [self.sink], 0.5, self.tick_length, 0.1, "pipe")
        out_2 = self.add_component(
            1, [self.sink], 0.5, self.tick_length, 0.1, "pipe")
        out_3 = self.add_component(
            1, [self.sink], 0.5, self.tick_length, 0.1, "pipe")
        out_4 = self.add_component(
            1, [self.sink], 0.5, self.tick_length, 0.1, "pipe")

        # inititalising sand filter backwash pipes
        back_1 = self.add_component(
            1, [self.sink], 0.5, self.tick_length, 0.1, "pipe")
        back_2 = self.add_component(
            1, [self.sink], 0.5, self.tick_length, 0.1, "pipe")
        back_3 = self.add_component(
            1, [self.sink], 0.5, self.tick_length, 0.1, "pipe")
        back_4 = self.add_component(
            1, [self.sink], 0.5, self.tick_length, 0.1, "pipe")

        # initialising sand filters
        filter_1 = self.add_component(
            1, [out_1, back_1], 8, self.tick_length, 1.5, "filter")
        filter_2 = self.add_component(
            1, [out_2, back_2], 8, self.tick_length, 1.5, "filter")
        filter_3 = self.add_component(
            1, [out_3, back_3], 8, self.tick_length, 1.5, "filter")
        filter_4 = self.add_component(
            1, [out_4, back_4], 8, self.tick_length, 1.5, "filter")

        # initialising sand filter inputs
        in_1 = self.add_component(
            1, [filter_1], 0.5, self.tick_length, 0.1, "pipe")
        in_2 = self.add_component(
            1, [filter_2], 0.5, self.tick_length, 0.1, "pipe")
        in_3 = self.add_component(
            1, [filter_3], 0.5, self.tick_length, 0.1, "pipe")
        in_4 = self.add_component(
            1, [filter_4], 0.5, self.tick_length, 0.1, "pipe")

        filter_1.set_input(in_1)
        filter_2.set_input(in_2)
        filter_3.set_input(in_3)
        filter_4.set_input(in_4)

        main_in = self.add_component(
            1, [in_1, in_2, in_3, in_4], 3, self.tick_length, 0.1, "pipe")

        # initialising source for the system
        self.source = self.add_component(
            1, [main_in], 1, self.tick_length, 1, "source")

    def take_round(self):

        # in each round simply push the predefined flow rate into the source
        self.source.push(self.average_flow, self.average_tss)

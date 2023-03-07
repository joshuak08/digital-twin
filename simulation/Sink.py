import GenericPipe

# special type of pipe, sink, used to mark the end of a system
class Sink(GenericPipe.GenericPipe):

    # as well as regular pipe stuff sinks keep track of stats for the whole system
    def __init__(self, id_num, num_of_inputs, outputs, length, tick_length, radius):
        super().__init__(id_num, num_of_inputs, outputs, length, tick_length, radius)
        self.pushes_in_round = 0
        self.flow_in_round = 0
        self.total_flow = 0
        self.total_particulate = 0
        self.type = "Sink"

    # push for a sink - doesn't push anywhere else, just updates its own values, resets for each round once it's been
    # pushed to by all inputs
    def push(self, flow_in, flow_tss):
        self.pushes_in_round += 1
        self.flow_in_round += flow_in 
        self.total_flow += flow_in 
        self.total_particulate += flow_tss * flow_in
        if self.pushes_in_round == self.num_of_inputs:
            self.pushes_in_round = 0
            self.flow_in_round = 0

    #TODO update - maybe keep track of sink info
    def snapshot(self, snap_dict: dict, snap_num: int) -> dict:
        return snap_dict
    
import GenericPipe


class Sink(GenericPipe.GenericPipe):

    def __init__(self, id_num, num_of_inputs, outputs, length, tick_length, radius):
        super().__init__(id_num, num_of_inputs, outputs, length, tick_length, radius)
        self.pushes_in_round = 0
        self.flow_in_round = 0
        self.total_flow = 0
        self.total_particulate = 0
        self.type = "Sink"

    def push(self, flow_in, flow_tss):
        self.pushes_in_round += 1
        self.flow_in_round += flow_in 
        self.total_flow += flow_in 
        self.total_particulate += flow_tss * flow_in
        if self.pushes_in_round == self.num_of_inputs:
            self.pushes_in_round = 0
            self.flow_in_round = 0

    def snapshot(self, snap_dict: dict, snap_num: int) -> dict:
        return snap_dict
    
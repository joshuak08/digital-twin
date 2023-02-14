import GenericPipe


class Sink(GenericPipe.GenericPipe):
    def __init__(self, num_of_inputs, simulation_system):
        self.num_of_inputs = num_of_inputs
        self.pushes_in_round = 0
        self.flow_in_round = 0
        self.total_flow = 0
        self.system = simulation_system
        pass

    def push(self, flow_in):
        self.pushes_in_round += 1
        self.flow_in_round += flow_in 
        self.total_flow += flow_in 
        if self.pushes_in_round == self.num_of_inputs:
            self.pushes_in_round = 0
            self.flow_in_round = 0
            self.system.take_round() # this doesn't exist yet, but would be the method in our system to take another round, might also pass information from sink

    def snapshot(self, snap_dict: dict, snap_num: int) -> dict:
        return snap_dict
    
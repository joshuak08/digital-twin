import SplitterPipe


class Source(SplitterPipe.SplitterPipe):
    def __init__(self, id_num, outputs, length, tick_length, radius):
        super().__init__(id_num, 1, outputs, length, tick_length, radius)
        self.total_flow = 0

    def push(self, flow_in):
        super().push(flow_in)
        self.total_flow += flow_in

    def snapshot(self, snap_dict, snap_num):

        for child_pipe in self.outputs:
            child_pipe.snapshot(snap_dict, snap_num)

        return snap_dict

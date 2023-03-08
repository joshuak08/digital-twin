import SplitterPipe


class Source(SplitterPipe.SplitterPipe):
    def __init__(self, id_num, outputs, length, tick_length, radius):
        super().__init__(id_num, 1, outputs, length, tick_length, radius)
        self.total_flow = 0
        self.type = "Source"

    def push(self, flow_in, flow_tss):
        super().push(flow_in, flow_tss)
        self.total_flow += flow_in
    
    def snapshot(self):
        data = (self.total_flow)
        return data
       
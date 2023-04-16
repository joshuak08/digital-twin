import SplitterPipe

# class to represent the source for a system i.e. where water is coming from
# functions as a multi output pipe, so inherits from splitter pipe
class Source(SplitterPipe.SplitterPipe):

    # as well as usual stuff source tracks total flow pushed into it
    def __init__(self, id_num, outputs, length, tick_length, radius):
        super().__init__(id_num, 1, outputs, length, tick_length, radius)
        self.total_flow = 0
        self.type = "Source"

    # uses inherited push method from splitter pipes, but also adds to total_flow for each push
    def push(self, flow_in, flow_tss):
        super().push(flow_in, flow_tss)
        self.total_flow += flow_in
    
    # snapshot just gives back total_flow, as this is the important information for the source
    def snapshot(self, snap_num):
        data = (self.id_num, snap_num, self.total_flow)
        return data
       
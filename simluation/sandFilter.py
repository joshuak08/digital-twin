import genericPipe

class sandFilter(genericPipe):

    def __init__(self, inputs, outputs, length):
        genericPipe.__init__(inputs, outputs, length)
        if len(self.inputs) != 1 or len(self.outputs) == 2:
            print("Error: Bad Inputs / Outputs.")
            return 
        self.outputNormal = outputs[0]
        self.outputBackwash = outputs[1]
        self.height = self.length
        self.sandHeight = self.height / 2
        self.backwash = False 

    def push(self, flow):
        self.sandHeight += 1 # incrementing amount of particulate in system - should be based on flow

        if self.sandHeight > 10: # arbitrary boundary to start backwash
            backwash = True
        if backwash:
            self.outputBackwash.push(flow) # should be based on how full the unit is
        else:
            self.outputNormal.push(flow) # ''
        


        

class Snapshotter:
    
    def __init__(self):
        self.system_data = {}
    
    def setup(self, system):
        
        self.system_data = {}
        for i in system.components:
            self.system_data[i.id_num] = (i.type, [])

    def snapshot(self, system):

        for i in system.components:
            self.system_data[i.id_num][1].append(i.snapshot())

    
    

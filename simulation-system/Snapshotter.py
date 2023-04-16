
class Snapshotter:
    
    # initially just has empty dictionary for data, and a variable to keep track of snapshots
    # also has system and is_setup to track whether or not it is safe to snapshot
    def __init__(self):
        self.system_data = {}
        self.snap_num = 0
        self.system = None
        self.is_setup = False
    
    # needs to be initialised with a particular system so the schema of the dictionary matches the components of the system
    def setup(self, system):
        
        # sets variables to track system state, and then make an entry in the dictionary for each component in the system
        self.is_setup = True
        self.system = system
        self.system_data = {}
        for i in system.components:
            self.system_data[i.id_num] = (i.type, [])

    # save the current state of the passed system
    # uses components own methods to handle gathering data, so what data is saved from a component is covered in that component's code
    def snapshot(self, system):
        
        # if either not setup at all, or setup with a different system, setup the snapshotter
        if not self.is_setup or self.system != system:
            self.setup(system)

        # for each component call it's snapshot function, and add that to it's entry in the dictionary
        # snapshot number isn't used to directly index anything here, but is necessary to retreive data later
        for i in system.components:
            self.system_data[i.id_num][1].append(i.snapshot(self.snap_num))
        
        # increment snapshot number
        self.snap_num += 1

    
    

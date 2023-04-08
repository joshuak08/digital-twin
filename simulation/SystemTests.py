#TODO Things to Test:
#   - Adding things to the system 
#       - Make sure that IDs are unique DONE
#       - Make sure that the list contains the right number of items DONE
#       - Make sure elements have the right type DONE
#   - Generic running of a simulation
#       - Correct number of rounds are taken DONE
#       - Correct number of snapshots are taken DONE
#   - Test Filter System
#       - Make sure it's constructed correctly
#       - Make sure pushes behave as expected (flow makes it to the sink etc.)
#       - Check state of filters
#   - Test Snapshotters
#       - Check the right amount of data is recorded
#       - Check the right data is recorded
#   - Test database
#       - Make sure correct stuff is written to database
import unittest

import SimulationSystem
import Snapshotter

class DummySimulation(SimulationSystem.SimulationSystem):
    
    def __init__(self, tick_length, average_flow, average_tss, snapshotter, total_rounds, snapshot_frequency, take_snapshots):
        super().__init__(tick_length, average_flow, average_tss, snapshotter, total_rounds, snapshot_frequency, take_snapshots)
        self.turns_taken = 0
    
    def take_round(self):
        self.turns_taken += 1

class DummySnapshotter(Snapshotter.Snapshotter):

    def __init__(self):
        super().__init__()
        self.snapshots_taken = 0
    
    def snapshot(self, system):
        self.snapshots_taken = 0
    

class TestSystemCreation(unittest.TestCase):

    def test_ids_unique(self):
        system = SimulationSystem.SimulationSystem(1, 0, 0, None, 0, 1, False)
        for i in range(100):
            system.add_component(0, [], 0, system.tick_length, 1, "pipe")

        component_ids = []
        for i in system.components:
            self.assertFalse(i.id_num in component_ids)
            component_ids.append(i.id_num)

    def test_all_components_added(self):
        system = SimulationSystem.SimulationSystem(1, 0, 0, None, 0, 1, False)

        for i in range(100):
            system.add_component(0, [], 0, system.tick_length, 1, "pipe")
        
        self.assertEqual(len(system.components), 100)

    def test_correct_types(self):
        system = SimulationSystem.SimulationSystem(1, 0, 0, None, 0, 1, False)

        system.add_component(0, [], 0, system.tick_length, 1, "pipe")
        system.add_component(1, [None, None], 0, system.tick_length, 1, "filter")
        system.add_component(0, [], 0, system.tick_length, 1, "sink")
        system.add_component(0, [], 0, system.tick_length, 1, "source")

        components = system.components
        self.assertEqual(components[0].type, "Splitter")
        self.assertEqual(components[1].type, "Filter")
        self.assertEqual(components[2].type, "Sink")
        self.assertEqual(components[3].type, "Source")

class TestSimulationRunning(unittest.TestCase):

    def test_correct_rounds(self):
        system = DummySimulation(1, 0, 0, None, 100, 1, False)
        system.simulate()
        self.assertEqual(system.turns_taken, 100)
    
    def test_correct_snapshots(self):
        snapshotter = DummySnapshotter()
        system = DummySimulation(1, 0, 0, snapshotter, 100, 5, False)
        system.simulate()
        self.assertEqual(snapshotter.snapshots_taken, 20)
    


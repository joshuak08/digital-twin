#TODO Things to Test:
#   - Adding things to the system 
#       - Make sure that IDs are unique DONE
#       - Make sure that the list contains the right number of items DONE
#       - Make sure elements have the right type DONE
#   - Generic running of a simulation
#       - Correct number of rounds are taken
#       - Correct number of snapshots are taken
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


class TestSystemCreation(unittest.TestCase):

    def test_ids_unique(self):
        system = SimulationSystem.SimulationSystem(1, 0, 0, 1, 1, False)

        for i in range(100):
            system.add_component(0, [], 0, system.tick_length, 1, "pipe")

        component_ids = []
        for i in system.components:
            self.assertFalse(i.id_num in component_ids)
            component_ids.append(i.id_num)

    def test_all_components_added(self):
        system = SimulationSystem.SimulationSystem(1, 0, 0, 1, 1, False)

        for i in range(100):
            system.add_component(0, [], 0, system.tick_length, 1, "pipe")
        
        self.assertEqual(len(system.components), 100)

    def test_correct_types(self):
        system = SimulationSystem.SimulationSystem(1, 0, 0, 1, 1, False)

        system.add_component(0, [], 0, system.tick_length, 1, "pipe")
        system.add_component(1, [None, None], 0, system.tick_length, 1, "filter")
        system.add_component(0, [], 0, system.tick_length, 1, "sink")
        system.add_component(0, [], 0, system.tick_length, 1, "source")

        components = system.components
        self.assertEqual(components[0].type, "Splitter")
        self.assertEqual(components[1].type, "Filter")
        self.assertEqual(components[2].type, "Sink")
        self.assertEqual(components[3].type, "Source")

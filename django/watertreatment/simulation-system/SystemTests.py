# TODO Things to Test:
#   - Adding things to the system DONE
#       - Make sure that IDs are unique DONE
#       - Make sure that the list contains the right number of items DONE
#       - Make sure elements have the right type DONE
#   - Generic running of a simulation DONE
#       - Correct number of rounds are taken DONE
#       - Correct number of snapshots are taken DONE
#   - Test Filter System DONE
#       - Make sure it's constructed correctly DONE
#       - Make sure pushes behave as expected (flow makes it to the sink etc.) DONE
#   - Test Snapshotters DONE
#       - Check Snapshotter setup works DONE
#       - Check right amount of data is recorded DONE
#       - Check the right data is recorded DONE
#   - Test database
#       - Make sure correct stuff is written to database
import unittest
import sqlite3
import os

import SimulationSystem
import Snapshotter
import FilterSystem
import FilterSnapshotter


class DummySimulation(SimulationSystem.SimulationSystem):

    def __init__(self, tick_length, average_flow, average_tss, snapshotter, total_rounds, snapshot_frequency, take_snapshots):
        super().__init__(tick_length, average_flow, average_tss,
                         snapshotter, total_rounds, snapshot_frequency, take_snapshots)
        self.turns_taken = 0

    def take_round(self):
        self.turns_taken += 1


class DummySnapshotSimulation(SimulationSystem.SimulationSystem):

    def take_round(self):
        for i in self.components:
            i.capacity += 1


class DummySnapshotter(Snapshotter.Snapshotter):

    def __init__(self):
        super().__init__()
        self.snapshots_taken = 0

    def snapshot(self, system):
        self.snapshots_taken += 1


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
        system.add_component(1, [None, None], 0,
                             system.tick_length, 1, "filter")
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
        system = DummySimulation(1, 0, 0, snapshotter, 100, 5, True)
        system.simulate()
        self.assertEqual(snapshotter.snapshots_taken, 20)


class TestFilterSystem(unittest.TestCase):

    def test_system_construction(self):
        component_dict = {"Splitter": 0, "Filter": 0, "Sink": 0, "Source": 0}
        system = FilterSystem.FilterSystem(1, 0, 0, None, 0, 1, False)

        for i in system.components:
            component_dict[i.type] = component_dict[i.type] + 1

        self.assertEqual(component_dict["Splitter"], 17)
        self.assertEqual(component_dict["Filter"], 4)
        self.assertEqual(component_dict["Sink"], 1)
        self.assertEqual(component_dict["Source"], 1)

    def test_simulation_one_round(self):
        system = FilterSystem.FilterSystem(1, 0.3, 243, None, 1, 1, False)
        system.simulate()

        self.assertGreater(system.sink.total_flow, 0)

        filters = [i for i in system.components if i.type == "Filter"]

        first_capacity = filters[0].capacity
        for i in filters:
            self.assertEqual(i.capacity, first_capacity)

    def test_simulation_multi_round(self):
        system = FilterSystem.FilterSystem(1, 0.3, 243, None, 10, 1, False)
        system.simulate()

        self.assertGreater(system.sink.total_flow, 0)

        filters = [i for i in system.components if i.type == "Filter"]

        first_capacity = filters[0].capacity
        for i in filters:
            self.assertEqual(i.capacity, first_capacity)


class TestSnapshotter(unittest.TestCase):

    def test_snapshotter_setup(self):
        system = SimulationSystem.SimulationSystem(1, 0, 0, None, 0, 1, False)
        snapshotter = Snapshotter.Snapshotter()

        system.add_component(0, [], 0, system.tick_length, 1, "pipe")
        system.add_component(1, [None, None], 0,
                             system.tick_length, 1, "filter")
        system.add_component(0, [], 0, system.tick_length, 1, "sink")
        system.add_component(0, [], 0, system.tick_length, 1, "source")

        snapshotter.setup(system)

        self.assertEqual(snapshotter.system_data[0][0], "Splitter")
        self.assertEqual(snapshotter.system_data[1][0], "Filter")
        self.assertEqual(snapshotter.system_data[2][0], "Sink")
        self.assertEqual(snapshotter.system_data[3][0], "Source")
        self.assertEqual(snapshotter.system_data[0][1], [])
        self.assertEqual(snapshotter.system_data[1][1], [])
        self.assertEqual(snapshotter.system_data[2][1], [])
        self.assertEqual(snapshotter.system_data[3][1], [])

    def test_snapshot_amount(self):
        snapshotter = Snapshotter.Snapshotter()
        system = DummySimulation(1, 0, 0, snapshotter, 5, 1, True)

        system.add_component(0, [], 0, system.tick_length, 1, "pipe")
        system.add_component(1, [None, None], 0,
                             system.tick_length, 1, "filter")
        system.add_component(0, [], 0, system.tick_length, 1, "sink")
        system.add_component(0, [], 0, system.tick_length, 1, "source")

        snapshotter.setup(system)

        system.simulate()

        for i in snapshotter.system_data:
            self.assertEqual(len(snapshotter.system_data[i][1]), 5)

    def test_snapshot_content(self):
        snapshotter = Snapshotter.Snapshotter()
        system = DummySnapshotSimulation(1, 0, 0, snapshotter, 5, 1, True)

        system.add_component(0, [], 0, system.tick_length, 1, "pipe")
        system.add_component(1, [None, None], 0,
                             system.tick_length, 1, "filter")
        system.add_component(0, [], 0, system.tick_length, 1, "sink")
        system.add_component(0, [], 0, system.tick_length, 1, "source")

        snapshotter.setup(system)

        system.simulate()

        for i in range(5):
            self.assertEqual(snapshotter.system_data[0][1][i][2], i)
            self.assertEqual(snapshotter.system_data[1][1][i][2], i)


class TestFilterSnapshotter(unittest.TestCase):

    def test_correct_contents(self):

        snapshotter = FilterSnapshotter.FilterSnapshotter(True)
        system = DummySnapshotSimulation(1, 0, 0, snapshotter, 5, 1, True)

        system.add_component(0, [], 0, system.tick_length, 1, "pipe")
        system.add_component(1, [None, None], 0,
                             system.tick_length, 1, "filter")
        system.add_component(0, [], 0, system.tick_length, 1, "sink")
        system.add_component(0, [], 0, system.tick_length, 1, "source")

        snapshotter.setup(system)

        system.simulate()

        table_name = snapshotter.to_database()

        connection = sqlite3.connect(os.getcwd() + "\db.sqlite3")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM " + table_name)
        data = cursor.fetchall()

        self.assertEqual(len(data), 5)
        for i in data:
            self.assertEqual(len(i), 5)
            self.assertEqual(i[1], i[2])

        connection.close()
        os.remove(os.getcwd() + "\db.sqlite3")

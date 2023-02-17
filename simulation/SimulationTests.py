import unittest 
import math

import GenericPipe
import SplitterPipe
import SandFilter
import Sink
import Source

class TestSystem:
    def __init__ (self, name):
        self.name = name 
        self.rounds_taken = 0
    
    def take_round(self):
        self.rounds_taken += 1

class TestPipe:
    def __init__ (self, name):
        self.name = name 
        self.valve = False 
    
    def toggle_valve(self):
        self.valve = not self.valve



class TestSinkBehaviour(unittest.TestCase):

    def test_sink_one_round_one_input(self):
        system = TestSystem("Dummy System")
        sink = Sink.Sink(0, 1, [], 1, 1, 1, system)
        sink.push(100)
        self.assertEqual(100, sink.total_flow)
        self.assertEqual(0, sink.flow_in_round)
        self.assertEqual(0, sink.pushes_in_round)
        self.assertEqual(1, system.rounds_taken)
    
    def test_sink_multi_round_one_input(self):
        system = TestSystem("Dummy System")
        sink = Sink.Sink(0, 1, [], 1, 1, 1, system)
        for i in range(5):
            sink.push(100)
        self.assertEqual(500, sink.total_flow)
        self.assertEqual(0, sink.flow_in_round)
        self.assertEqual(0, sink.pushes_in_round)
        self.assertEqual(5, system.rounds_taken)
    
    def test_sink_partial_round_multi_input(self):
        system = TestSystem("Dummy System")
        sink = Sink.Sink(0, 3, [], 1, 1, 1, system)
        sink.push(100)
        sink.push(100)
        self.assertEqual(200, sink.total_flow)
        self.assertEqual(200, sink.flow_in_round)
        self.assertEqual(2, sink.pushes_in_round)
        self.assertEqual(0, system.rounds_taken)
    
    def test_sink_one_round_multi_input(self):
        system = TestSystem("Dummy System")
        sink = Sink.Sink(0, 3, [], 1, 1, 1, system)
        sink.push(100)
        sink.push(100)
        sink.push(100)
        self.assertEqual(300, sink.total_flow)
        self.assertEqual(0, sink.flow_in_round)
        self.assertEqual(0, sink.pushes_in_round)
        self.assertEqual(1, system.rounds_taken)
    
    def test_sink_multi_round_multi_input(self):
        system = TestSystem("Dummy System")
        sink = Sink.Sink(0, 3, [], 1, 1, 1, system)
        for i in range(5):
            sink.push(100)
            sink.push(100)
            sink.push(100)
        self.assertEqual(1500, sink.total_flow)
        self.assertEqual(0, sink.flow_in_round)
        self.assertEqual(0, sink.pushes_in_round)
        self.assertEqual(5, system.rounds_taken)


class TestSplitterBehaviour(unittest.TestCase):

    def test_single_pipe(self):
        system = TestSystem("Dummy System")
        sink = Sink.Sink(0, 1, [], 1, 1, 1, system)
        pipe = SplitterPipe.SplitterPipe(1, 1, [sink], 1, 1, 1)
        pipe.push(100)
        self.assertEqual(100, sink.total_flow)
        self.assertEqual(0, pipe.capacity)
    
    def test_pipe_chain(self):
        system = TestSystem("Dummy System")
        sink = Sink.Sink(0, 1, [], 1, 1, 1, system)
        pipe1 = SplitterPipe.SplitterPipe(1, 1, [sink], 1, 1, 1)
        pipe2 = SplitterPipe.SplitterPipe(2, 1, [pipe1], 1, 1, 1)
        pipe2.push(100)
        self.assertEqual(100, sink.total_flow)
        self.assertEqual(0, pipe1.capacity)
        self.assertEqual(0, pipe2.capacity)
    
    def test_basic_split(self):
        system = TestSystem("Dummy System")
        sink1 = Sink.Sink(0, 1, [], 1, 1, 1, system)
        sink2 = Sink.Sink(1, 1, [], 1, 1, 1, system)
        pipe = SplitterPipe.SplitterPipe(2, 1, [sink1, sink2])
        pipe.push(100) 
        self.assertEqual(50, sink1.total_flow)
        self.assertEqual(50, sink2.total_flow)
        self.assertEqual(0, pipe.capacity)
    
    def test_split_one_closed(self):
        system = TestSystem("Dummy System")
        sink1 = Sink.Sink(0, 1, [], 1, 1, 1, system)
        sink2 = Sink.Sink(1, 1, [], 1, 1, 1, system)
        pipe = SplitterPipe.SplitterPipe(2, 1, [sink1, sink2])
        sink1.toggle_valve()
        pipe.push(100) 
        self.assertEqual(0, sink1.total_flow)
        self.assertEqual(100, sink2.total_flow)
        self.assertEqual(0, pipe.capacity)

    def test_split_both_closed(self):
        system = TestSystem("Dummy System")
        sink1 = Sink.Sink(0, 1, [], 1, 1, 1, system)
        sink2 = Sink.Sink(1, 1, [], 1, 1, 1, system)
        pipe = SplitterPipe.SplitterPipe(2, 1, [sink1, sink2])
        sink1.toggle_valve()
        sink2.toggle_valve()
        pipe.push(100) 
        self.assertEqual(0, sink1.total_flow)
        self.assertEqual(0, sink2.total_flow)
        self.assertEqual(100, pipe.capacity)

    def test_fractional_split(self):
        system = TestSystem("Dummy System")
        sink1 = Sink.Sink(0, 1, [], 1, 1, 1, system)
        sink2 = Sink.Sink(1, 1, [], 1, 1, 1, system)
        pipe = SplitterPipe.SplitterPipe(2, 1, [sink1, sink2])
        pipe.push(45) 
        self.assertEqual(22.5, sink1.total_flow)
        self.assertEqual(22.5, sink2.total_flow)
        self.assertEqual(0, pipe.capacity)

    def test_unequal_radius_split(self):
        system = TestSystem("Dummy System")
        sink1 = Sink.Sink(0, 1, [], 1, 1, 3, system)
        sink2 = Sink.Sink(1, 1, [], 1, 1, 1, system)
        pipe = SplitterPipe.SplitterPipe(2, 1, [sink1, sink2])
        pipe.push(45)
        self.assertEqual(75, sink1.total_flow)
        self.assertEqual(25, sink2.total_flow)
        self.assertEqual(0, pipe.capacity)

class TestSourceBehaviour(unittest.TestCase):

    def test_single_output(self):
        system = TestSystem("Dummy System")
        sink = Sink.Sink(0, 1, [], 1, 1, 1, system)
        source = Source.Source(1, [sink], 1, 1, 1)
        source.push(100)
        self.assertEqual(100, sink.total_flow)
        self.assertEqual(100, source.total_flow)

    # All other behaviour is inherited from splitter pipes so those tests should cover sources


class TestSandFilterBehaviour(unittest.TestCase):

    def test_basic_push(self):
        system = TestSystem("Dummy System")
        sink1 = Sink.Sink(0, 1, [], 1, 1, 0.1, system)
        sink2 = Sink.Sink(1, 1, [], 1, 1, 0.1, system)
        filter = SandFilter.SandFilter(2, 1, [sink1, sink2], 8, 1, 1.5)
        filter.push(10)
        expected_water_height = 10 / math.pi * (1.5 ** 2)
        expected_velocity = math.sqrt(2 * 9.807 * expected_water_height)
        expected_flow_out = expected_velocity * sink1.cs_area
        self.assertEqual(expected_flow_out, sink1.total_flow)
        self.assertEqual(0, sink2.total_flow)
        self.assertEqual(10 - expected_flow_out, filter.capacity)

    def test_start_and_end_backwash(self):
        system = TestSystem("Dummy System")
        sink1 = Sink.Sink(0, 1, [], 1, 1, 0.1, system)
        sink2 = Sink.Sink(1, 1, [], 1, 1, 0.1, system)
        filter = SandFilter.SandFilter(2, 1, [sink1, sink2], 8, 1, 1.5)
        filter.particulate_mass = 499999
        self.assertFalse(filter.backwash)
        filter.push(10)
        self.assertTrue(filter.backwash)
        self.assertEqual(filter.output, sink2)
        self.assertGreater(sink2.total_flow, 0)
        self.assertEqual(0, sink1.total_flow)
        filter.backwash_timer = 1
        filter.push(10)
        self.assertFalse(filter.backwash)
        self.assertEqual(filter.output, sink1)
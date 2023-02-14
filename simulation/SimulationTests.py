import unittest 

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
    
    def test_pipe_chain(self):
        system = TestSystem("Dummy System")
        sink = Sink.Sink(0, 1, [], 1, 1, 1, system)
        pipe1 = SplitterPipe.SplitterPipe(1, 1, [sink], 1, 1, 1)
        pipe2 = SplitterPipe.SplitterPipe(2, 1, [pipe1], 1, 1, 1)
        pipe2.push(100)
        self.assertEqual(100, sink.total_flow)
    
    def test_basic_split(self):
        system = TestSystem("Dummy System")
        sink1 = Sink.Sink(0, 1, [], 1, 1, 1, system)
        sink2 = Sink.Sink(1, 1, [], 1, 1, 1, system)
        pipe = SplitterPipe.SplitterPipe(2, 1, [sink1, sink2])
        # test work paused to add area attribute to Splitters
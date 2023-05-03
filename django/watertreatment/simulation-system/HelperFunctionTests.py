import unittest
import os
import sqlite3

import HelperFunctions


class BasicHelperTests(unittest.TestCase):

    def test_can_run(self):
        HelperFunctions.basic_simulation(0.3, 252, 10, True)


class VariableParticluateTests(unittest.TestCase):

    def test_can_run(self):
        HelperFunctions.initial_particulate_simulation(
            0.3, 252, 10, [0, 0, 0, 0], True)

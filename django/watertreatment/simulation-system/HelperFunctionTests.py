import unittest
import os
import sqlite3

import HelperFunctions


class BasicHelperTests(unittest.TestCase):

    def test_can_run(self):
        HelperFunctions.basic_simulation(0.3, 252, 10, True)
        os.remove(os.getcwd() + "\db.sqlite3")


class VariableParticluateTests(unittest.TestCase):

    def test_can_run(self):
        HelperFunctions.initial_particulate_simulation(
            0.3, 252, 10, [0, 0, 0, 0], True)
        os.remove(os.getcwd() + "\db.sqlite3")

    def test_proper_particulate(self):

        table_name = HelperFunctions.initial_particulate_simulation(
            0.3, 0, 1, [0, 1, 2, 3], True)

        connection = sqlite3.connect(os.getcwd() + "\db.sqlite3")
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM " + table_name)
        data = cursor.fetchall()

        pariculate_amounts = [0, 1, 2, 3]

        for i in data:
            self.assertTrue(i[3] in pariculate_amounts)
            pariculate_amounts.remove(i[3])

        connection.close()

        os.remove(os.getcwd() + "\db.sqlite3")

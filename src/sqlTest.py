import unittest

import sqliteRevitIpy
import DocumentInterfaceTest
import DocumentInterface
import os
import json


class testSqliteRevitDB(unittest.TestCase):

    @classmethod
    def setUpClass(cls):  # sets up the data baser class with a test document
        test_doc = DocumentInterfaceTest.generic_3_cat_document("cat1", "cat2", "cat3")  # document for testing
        test_doc_interface = DocumentInterface.DocumentInterface(test_doc, DocumentInterfaceTest.TestCollector(
            test_doc.elementList), [])  # document interface for testing
        data_baser = sqliteRevitIpy.DataBaser(test_doc_interface, "test")  # creates database
        data_baser.access_table()  # creates table / accesses table if it doesn't exist
        data_baser.store_elems()
        data_baser.cursor.row_factory = lambda cursor, row: row[0]

        cls.data_baser = data_baser
        cls.cursor = data_baser.cursor
        print("setting up class done")

    def test_1_check_columns(self):  # checks the names of columns
        self.cursor.execute("""SELECT * FROM components_document""")
        self.cursor.fetchone()
        names = list(map(lambda x: x[0], self.cursor.description))
        self.assertEqual(["elemID", "name", "params"], names)

    def test_2_correct_row_Count(self):  # checks the correct number of rows are in the table
        self.cursor.execute("""SELECT * FROM components_document""")
        self.assertEqual(len(self.cursor.fetchall()), 6)

    def test_3_validate_JSON_storage(self):  # checks if the parameters are stored as JSON correctly
        try:
            for param in self.cursor.execute("""SELECT params FROM components_document"""):
                json.loads(param)
        except ValueError:
            self.fail("test_validate_JSON_storage has failed: ValueError")

    def test_4_closing_conn(self):  # checks if closing the connection to the data base is successful
        try:
            self.data_baser.close_connection()
        except:
            self.fail("failure in attempting to close connection to testdb.sqlite3")

    @classmethod
    def tearDownClass(cls):
        os.remove(os.path.dirname(os.path.realpath(__file__)) + "\\testdb.sqlite3")


if __name__ == '__main__':
    unittest.main()

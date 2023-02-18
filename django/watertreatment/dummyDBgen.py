import sqlite3
import os


class DataBaser:  # class to hold info about database
    def __init__(self, test=""):
        path = os.path.dirname(os.path.realpath(__file__)) + '\\' + test + "db.sqlite3"
        print("path:" + path)
        self.dbConn = sqlite3.connect(path)  # represents connection to db (creates db if non existent)
        self.cursor = self.dbConn.cursor()  # database cursor

    # creates a table for elements if it doesn't already exist`
    def drop_table(self):
        self.cursor.execute("""DROP TABLE IF EXISTS components_simdatatable""")
        self.dbConn.commit()

    def access_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS components_simdatatable (
                                components text, 
                                snapshots integer,
                                waterLevel integer,
                                sanddisp integer
                                )""")
        self.dbConn.commit()  # Commit changes to database

    # stores all elements listed in documentInterface into database
    def store_elems(self, components, snapshots, waterlevel, sanddisp):
        for i in range(0, len(components)):
            print("storing row: ", waterlevel[i])
            self.cursor.execute("INSERT INTO components_simdatatable VALUES (?, ?, ?, ?)", (components[i],
                                                                          snapshots[i],
                                                                          waterlevel[i],
                                                                          sanddisp[i]))
        self.dbConn.commit()  # commits changes to database

    def close_connection(self):
        self.dbConn.close()


dummyDB = DataBaser()
dummyDB.drop_table()
dummyDB.access_table()
dummyDB.store_elems(["tank0","tank0","tank1","tank1","tank2","tank2","tank3","tank3"], [0, 1, 0, 1, 0, 1, 0, 1], [152, 20, 20, 125, 0, 100, 40, 80], [5, 5, 5, 5, 5, 5, 5, 5])
dummyDB.close_connection()

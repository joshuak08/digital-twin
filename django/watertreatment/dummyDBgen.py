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

    # (id integer, snap_num integer, water_vol integer, particulate integer, backwash boolean)
    def access_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS components_simdatatable (
                                id integer, 
                                snap_num integer,
                                water_vol integer,
                                particulate integer,
                                backwash boolean
                                )""")
        self.dbConn.commit()  # Commit changes to database

    # stores all elements listed in documentInterface into database
    def store_elems(self, components, snap_num, water_vol, particulate, backwash):
        for i in range(0, len(components)):
            print("storing row: ", water_vol[i])
            self.cursor.execute("INSERT INTO components_simdatatable VALUES (?, ?, ?, ?, ?)", (components[i],
                                                                                               snap_num[i],
                                                                                               water_vol[i],
                                                                                               particulate[i],
                                                                                               backwash[i]))
        self.dbConn.commit()  # commits changes to database

    def close_connection(self):
        self.dbConn.close()


dummyDB = DataBaser()
dummyDB.drop_table()
dummyDB.access_table()
# ["tank0","tank0","tank1","tank1","tank2","tank2","tank3","tank3"], [0, 1, 0, 1, 0, 1, 0, 1], [152, 20, 20, 125, 0, 100, 40, 80], [5, 5, 5, 5, 5, 5, 5, 5]
dummyDB.store_elems([9, 9, 9, 9, 10, 10, 10, 10, 11, 11, 11, 11, 12, 12, 12, 12],  # component id
                    [0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3, 0, 1, 2, 3],  # snap_num
                    [0, 56, 56, 25, 0, 50, 0, 50, 32, 5, 30, 56, 0, 10, 30, 0],  # water_vol
                    # [92800, 23921, 293083, 308351, 83458, 341822, 485693, 114396, 92800, 23921, 293083, 308351],  # particulate
                    [0, 500000, 0, 250000, 0, 500000, 0, 250000, 0, 500000, 0, 250000, 0, 500000, 0, 250000],  # particulate
                    [False, True, True, False, False, True, True, False, False, True, True, False, False, True, True, False])  # backwash
dummyDB.close_connection()

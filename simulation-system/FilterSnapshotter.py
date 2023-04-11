import sqlite3
import os
import datetime

import Snapshotter

def filter_for_filters(pair):
    key, value = pair 
    return value[0] == "Filter" 

class FilterSnapshotter(Snapshotter.Snapshotter):

    def __init__(self, testing):
        super().__init__()
        self.testing = testing

    # TODO implement this - should write to a database the information about all the filters in the system
    def to_database(self):
        
        if not self.testing:
            path = os.getcwd()
            parent = os.path.abspath(os.path.join(path, os.pardir))
            db_path = parent + "\django\watertreatment\db.sqlite3"
        else:
            db_path = os.getcwd() + "\db.sqlite3"

        time_tag = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
        table_name = "filters_" + time_tag

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE " + table_name + "(id integer, snap_num integer, water_vol integer, particulate integer, backwash boolean)")

        filtered_components = dict(filter(filter_for_filters, self.system_data.items()))
        data = []

        for i in filtered_components:
            data = data + filtered_components[i][1]

        cursor.executemany("INSERT INTO " + table_name + " VALUES(?, ?, ?, ?, ?)", data)
        connection.commit()
        connection.close()

        return table_name
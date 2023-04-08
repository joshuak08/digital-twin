import sqlite3
import os
import datetime

import Snapshotter

def filter_for_filters(pair):
    key, value = pair 
    return value[0] == "Filter" 

class FilterSnapshotter(Snapshotter.Snapshotter):

    # TODO implement this - should write to a database the information about all the filters in the system
    def to_database(self):

        path = os.getcwd()
        parent = os.path.abspath(os.path.join(path, os.pardir))
        db_path = parent + "\django\watertreatment\db.sqlite3"

        time_tag = datetime.datetime.now().strftime("%d/%m/%Y_%H:%M:%S")
        table_name = "filters_" + time_tag

        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE " + table_name + "(id integer, snap_num integer, water_vol integer, particulate integer, backwash boolean)")

        filtered_components = dict(filter(filter_for_filters, self.system_data.items))
        
        data = []

        for k, v in filtered_components:
            data.append(v[1])

        cursor.executemany("INSERT INTO " + table_name + " VALUES(?, ?, ?, ?, ?)", data)
        connection.commit()
        connection.close()

        return table_name
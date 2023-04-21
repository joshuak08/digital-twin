import sqlite3
import os
import datetime

import Snapshotter

# helper function to make filtering out unused elements easier


def filter_for_filters(pair):
    key, value = pair
    return value[0] == "Filter"

# extension of snapshotter that specifically saves only information about filters


class FilterSnapshotter(Snapshotter.Snapshotter):

    # initialise with a variable to indicate whether you are running tests or not
    def __init__(self, testing):
        super().__init__()
        self.testing = testing

    # function to write data contained in snapshotter to a database, returns name of the table the data is written to
    def to_database(self):

        # if not testing mode, use path of the database being used by django
        if not self.testing:
            path = os.getcwd()
            parent = os.path.abspath(os.path.join(path, os.pardir))
            db_path = parent + "\watertreatment\db.sqlite3"

        # otherwise make new database in local directory
        else:
            db_path = os.getcwd() + "\db.sqlite3"

        # name the table based on the current time, so different tables are uniquely identifiable
        time_tag = datetime.datetime.now().strftime("%d%m%Y_%H%M%S")
        table_name = "filters_" + time_tag

        # open connection to database
        connection = sqlite3.connect(db_path)
        cursor = connection.cursor()

        # create a table, with a unique name, that stores the information of filters, and has primary key of the id of the fitler, and the snap_num
        # (as each filter should have only one entry for each snapshot)
        cursor.execute("CREATE TABLE " + table_name +
                       "(id integer, snap_num integer, water_vol integer, particulate integer, backwash boolean, PRIMARY KEY (id, snap_num))")

        # remove anything that isn't a sand filter from the dictionary
        filtered_components = dict(
            filter(filter_for_filters, self.system_data.items()))
        data = []

        # then take the tuples of data from all of them and add them to one list
        for i in filtered_components:
            data = data + filtered_components[i][1]

        # then write all of these tuples into our table, and, close our connection
        cursor.executemany("INSERT INTO " + table_name +
                           " VALUES(?, ?, ?, ?, ?)", data)
        connection.commit()
        connection.close()

        # then return the name of the table so it can be used by other code to access this data
        return table_name

import sqlite3
import os

class DataBaser:  # class to hold info about database
    def __init__(self, document_interface, test=""):
        self.document = document_interface  # assigns document to a variable
        print(self.document)

        path = os.path.dirname(os.path.realpath(__file__)) + '\\' + test + "db.sqlite3"
        print("path:" + path)
        self.dbConn = sqlite3.connect(path)  # represents connection to db (creates db if non existent)
        self.cursor = self.dbConn.cursor()  # database cursor

    # creates a table for elements if it doesn't already exist`
    def access_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS components_document (
                                elemID integer PRIMARY KEY, 
                                name text,
                                params blob 
                                )""")
        self.dbConn.commit()  # Commit changes to database

    # stores all elements listed in documentInterface into database
    def store_elems(self):
        for elementList in self.document.elementDict.values():  # names  = keys , values = list of elements
            for element in elementList:
                parameters = element.parameters
                param_string = "{"
                for name, parameter in parameters.items():
                    newString = '"' + name + '" : ' + '"(' + parameter.stringValue + ', ' + str(parameter.numericalValue) + ')"'
                    param_string += newString + ','
                param_string = param_string.rstrip(',')
                param_string += '}'

                self.cursor.execute("INSERT INTO components_document VALUES (?, ?, ?)", (element.elementID,
                                                                                         element.name,
                                                                                         param_string))
        self.dbConn.commit()  # commits changes to database

    def close_connection(self):
        self.dbConn.close()


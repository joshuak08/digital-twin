import sqlite3
import os

# import json
# import DocumentInterface
# import DocumentInterfaceTest
import DocumentInterfaceTest
import DocumentInterface


class DataBaser:  # class to hold info about database
    def __init__(self, document_interface, test=""):
        self.document = document_interface  # assigns document to a variable
        print(self.document)

        # for elements in self.document.elementDict.values():
        #     for i in elements:
        #         print(i.elementID)

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
                param_string.rstrip(',')
                param_string += '}'

                self.cursor.execute("INSERT INTO components_document VALUES (?, ?, ?)", (element.elementID,
                                                                                         element.name,
                                                                                         param_string))
        self.dbConn.commit()  # commits changes

    # returns entire table in json format
    # def return_elems(self):
    #     table = self.cursor.execute("SELECT * FROM components_document")
    #     dict_arr = [
    #         dict((self.cursor.description[i][0], row[i] if i != 2 else json.loads(row[i]))  # array of dictionaries
    #              for i, value in enumerate(row))  # late binding, enumerate row tuple
    #         for row in self.cursor.fetchall()  # fetchall returns rows as a list of tuples (1 row = 1 tuple)
    #         ]
    #     json_out = json.dumps(dict_arr)
    #     return json_out

    def close_connection(self):
        self.dbConn.close()


# testDoc = DocumentInterfaceTest.generic_3_cat_document("cat1", "cat2", "cat3")
# document = DocumentInterface.DocumentInterface(testDoc, DocumentInterfaceTest.TestCollector(testDoc.elementList), [])
#
# database = DataBaser(document)  # creates databaser class with the document passed in
# database.access_table()  # creates a table with element columns as parameters if one doesn't exist
# # #
# database.store_elems()  # queries the database and prints all rows
# # #
# database.cursor.execute("DELETE FROM components_document")  # empties the database
# database.dbConn.commit()  # commits changes
# database.dbConn.close()  # closes connection to database

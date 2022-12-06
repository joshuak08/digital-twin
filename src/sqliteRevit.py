import sqlTest
import sqlite3
import array
import json


class DataBaser:  # class to hold info about database
    def __init__(self, document_interface):
        self.document = document_interface  # assigns document to a variable
        self.dbConn = sqlite3.connect("document.db")  # represents connection to db
        self.cursor = self.dbConn.cursor()  # database cursor

    # creates a table for elements if it doesn't already exist
    def access_table(self):
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS document (
                                elemID integer, 
                                name text, 
                                category blob, 
                                params text /*should be json*/
                                )""")
        self.dbConn.commit()  # Commit changes to database

    # stores all elements listed in documentInterface into database
    def store_elems(self):
        for element in self.document.elementList:  # iterates through elements in document and adds them to db
            parameters = element.Parameters
            param_string = "{name:" + parameters.Definition.Name + ",stringVal:" + parameters.stringVal \
                           + ",doubleVal:" + str(parameters.doubleVal) + ",HasVal:" + str(parameters.HasValue) + "}"

            self.cursor.execute("INSERT INTO document VALUES (?, ?, ?, ?)", (element.Id,
                                                                             element.Name,
                                                                             element.category,
                                                                             param_string))
        self.dbConn.commit()  # commits changes

    # returns entire table in json format
    def return_elems(self):
        table = self.cursor.execute("SELECT * FROM document")
        dict_arr = [dict((self.cursor.description[i][0], row[i])  # array of dictionaries
                         for i, value in enumerate(row))  # late binding, enumerate allows rows to be iterable
                    for row in self.cursor.fetchall()  # fetchall returns rows as a list of tuples (1 row = 1 tuple)
                    ]
        json_out = json.dumps(dict_arr)
        return json_out


# params = sqlTest.TestParameter("param", "string", 0.1)  # initialises params
# elem1 = sqlTest.element_type_element(0, params)  # initialises an element
# # elem2 = sqlTest.element_type_element(1, params)  # initialises an element
# document = sqlTest.TestDocument([elem1])  # initialises a document
#
# database = DataBaser(document)  # creates databaser class with the document passed in
# database.access_table()  # creates a table with element columns as parameters if one doesn't exist
# #
# database.store_elems()
# print(database.return_elems())  # queries the database and prints all rows
# #
# database.cursor.execute("DELETE FROM document WHERE elemID=1")  # deletes the element with elemID = 1
# database.dbConn.commit()  # this commits changes to the database
# #
# database.cursor.execute("DELETE FROM document")  # empties the database
# database.dbConn.commit()  # commits changes
# database.dbConn.close()  # closes connection to database

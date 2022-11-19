import SqlTest
import sqlite3
import array


class DataBaser:  # class to hold info about database
    def __init__(self, DocumentInterface):
        self.document = DocumentInterface   # assigns document to a variable
        self.dbConn = sqlite3.connect("document.db")  # represents connection to db
        self.cursor = self.dbConn.cursor()  # database cursor

    def create_elem_table(self):  # creates a table for elements if it doesn't already exist
        self.cursor.execute("""CREATE TABLE IF NOT EXISTS document (
                                elemID integer, 
                                name text, 
                                category blob, 
                                params text
                                )""")
        self.dbConn.commit()  # Commit changes to database

    def store_elems(self):
        for element in self.document.elementList:  # iterates through elements in document and adds them to db
            param_string = element.Parameters.convert_to_string()
            self.cursor.execute("INSERT INTO document VALUES (?, ?, ?, ?)", (element.Id,
                                                                             element.Name,
                                                                             element.category,
                                                                             param_string))
        self.dbConn.commit()  # commits changes


params = SqlTest.TestParameter("param", "string", 0.1)  # initialises params
elem1 = SqlTest.element_type_element(0, params)  # initialises an element
elem2 = SqlTest.element_type_element(1, params)  # initialises an element
document = SqlTest.TestDocument([elem1, elem2])  # initialises a document

database = DataBaser(document)  # creates databaser class with the document passed in
database.create_elem_table()  # creates a table with element columns as parameters if one doesn't exist

database.store_elems()
print(database.cursor.execute("SELECT * FROM document").fetchall())  # queries the database and prints all rows

database.cursor.execute("DELETE FROM document WHERE elemID=1")  # deletes the element with elemID = 1
database.dbConn.commit()    # this commits changes to the database

print(database.cursor.execute("SELECT * FROM document").fetchall())  # queries database for all rows and columns and prints them

database.cursor.execute("DELETE FROM document")  # empties the database
database.dbConn.commit()  # commits changes
database.dbConn.close()  # closes connection to database


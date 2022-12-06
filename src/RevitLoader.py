import Autodesk.Revit.DB as DB
from revitutils import doc
import DocumentInterface
import sqliteRevit

collector = DB.FilteredElementCollector(doc)

categories = []
# Construct categories - user input / hardcode / something else

docI = DocumentInterface.DocumentInterface(doc, collector, categories)
# Next needs to pass this into something to construct the database, and that should be it

dataBaser = sqliteRevit.DataBaser(docI)
dataBaser.access_table()
dataBaser.store_elems()


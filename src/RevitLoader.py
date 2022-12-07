import DocumentInterface
import sqliteRevitIpy
import Autodesk.Revit.DB as DB

doc = __revit__.ActiveUIDocument.Document
collector = DB.FilteredElementCollector(doc)
#categories = [DB.BuiltInCategory.OST_MechanicalEquipment, DB.BuiltInCategory.OST_PipingSystem, DB.BuiltInCategory.OST_PipeFitting, DB.BuiltInCategory.OST_PipeAccessory]
document = DocumentInterface.DocumentInterface(doc, collector, [DB.BuiltInCategory.OST_MechanicalEquipment])
for elements in document.elementDict.values():
    for i in elements:
        print(i.elementID)
    


dataBaser = sqliteRevitIpy.DataBaser(document)

dataBaser.access_table()
dataBaser.store_elems()
dataBaser.close_connection()

print("Done making DB")

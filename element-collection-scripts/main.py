import Autodesk.Revit.DB as DB


class DocumentInterface:
    elementDict = {}

    def __init__(self, collector):

        newcollector = collector.WhereElementIsNotElementType()
        mechequip = newcollector.OfCategory(DB.BuiltInCategory.OST_MechanicalEquipment)
        pipes = newcollector.OfCategory(DB.BuiltInCategory.OST_PipeSegments)
        connections = newcollector.OfCategory(DB.BuiltInCategory.OST_PipeConnections)
        fittings = newcollector.OfCategory(DB.BuiltInCategory.OST_PipeFitting)
        fullelements = mechequip.UnionWith(pipes).UnionWith(connections).UnionWith(fittings)

        for i in fullelements:
            if self.elementDict.has_key(i.Name):
                self.elementDict[i.Name].append(i)
            else:
                self.elementDict[i.Name] = [i]

    def get_element_names(self):
        return self.elementDict.keys()

    def get_elements_of_name(self, name):
        return self.elementDict[name]

class ElementInterface:


    def __init__(self):

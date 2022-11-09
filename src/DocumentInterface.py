import Autodesk.Revit.DB as DB


class DocumentInterface:
    elementDict = {}
    underlyingDocument = None

    def __init__(self, collector, categories, document):
        self.underlyingDocument = document

        newcollector = collector.WhereElementIsNotElementType()
        elements = None
        if len(categories) != 0:
            for i in categories:
                if elements is None:
                    elements = newcollector.OfCategory(i)
                else:
                    elements = elements.UnionWith(newcollector.OfCategory(i))

        for i in elements:
            if i.Name in self.elementDict:
                self.elementDict[i.Name].append(ElementInterface(i))
            else:
                self.elementDict[i.Name] = [ElementInterface(i)]

    def get_element_names(self):
        return self.elementDict.keys()

    def get_elements_of_name(self, name):
        return self.elementDict[name]


class ElementInterface:
    name = ""
    elementID = None
    underlyingElement = None
    parameters = {}

    def __init__(self, element):
        self.name = element.Name
        self.elementID = element.Id
        self.underlyingElement = element
        for i in element.Parameters:
            if i.HasValue:
                self.parameters[i.Definition.Name] = ParameterInterface(i)

    def has_parameter(self, parametername):
        return parametername in self.parameters

    def get_parameter(self, parametername):
        if self.has_parameter(parametername):
            return self.parameters[parametername]
        else:
            return "No such parameter"


class ParameterInterface:
    name = ""
    underlyingParameter = None
    stringValue = None
    numericalValue = 0.0

    def __init__(self, parameter):
        self.name = parameter.Definition.Name
        self.underlyingParameter = parameter
        self.stringValue = parameter.AsValueString()
        self.numericalValue = parameter.AsDouble()

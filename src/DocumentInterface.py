#import Autodesk.Revit.DB as DB

"""
Set of classes for interfacing with a Revit document

Way to use this is to create a new DocumentInterface, you need to pass this:
- The Document you are working with
- A base FilteredElementCollector on the Document you are working with
- A list of categories of Elements that you are interested in working with (and empty list will lead
to the collection of Elements from all categories)

This will generate a DocumentInterface for you with all the relevant information from the document, including:
- A dictionary of element type names to lists of ElementInterfaces
- ElementInterface-s that contain the useful information from an element (including a dictionary of parameters)
- ParameterInterface-s provide easy access to a certain parameter of a certain element

Each interface has some basic getting commands at the moment, but can be expanded as needed.
Each Interface stores it's underlying Revit object for the sake of direct document access for modifying the
document or making another query.
"""


class DocumentInterface:

    def __init__(self, document, collector, categories):
        self.underlyingDocument = document
        self.elementDict = {}
        newcollector = collector.WhereElementIsNotElementType()

        elements = None
        if len(categories) != 0:
            for i in categories:
                if elements is None:
                    elements = newcollector.OfCategory(i)
                else:
                    elements = elements.UnionWith(newcollector.OfCategory(i))
        else:
            elements = newcollector
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

    def __init__(self, element):
        self.name = element.Name
        self.elementID = element.Id
        self.underlyingElement = element
        self.parameters = {}
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

    def __init__(self, parameter):
        self.name = parameter.Definition.Name
        self.underlyingParameter = parameter
        self.stringValue = parameter.AsValueString()
        self.numericalValue = parameter.AsDouble()

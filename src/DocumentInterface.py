# import Autodesk.Revit.DB as DB

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
    # DocumentInterface initilisation, takes in a document, collector, and list of categories
    def __init__(self, document, collector, categories):
        self.underlyingDocument = document  # saves the actual revit document in the object
        self.elementDict = {}  # initialises the dictionary to store elements
        newcollector = collector.WhereElementIsNotElementType()  # removes element types from the collector (I don't think we'll ever need to work with these, can be changed)

        elements = None
        # If categories have been specified, union together all elements from specified categories
        if len(categories) != 0:
            for i in categories:
                if elements is None:
                    elements = newcollector.OfCategory(i)
                else:
                    elements = elements.UnionWith(newcollector.OfCategory(i))
        # If not then the collector is unmodified (all elements passed through)
        else:
            elements = newcollector
        # At this point the collector should contain all elements belonging to specified categories
        # if categories are specified, otherwise should have all elements
        # Then goes through all of these elements, and adds them to the dictionary
        for i in elements:
            # If the name of the element is already a key in the dictionary - add it to the list of elements with that
            # name (before being added, the elements are converted into ElementInterfaces
            if i.Name in self.elementDict:
                self.elementDict[i.Name].append(ElementInterface(i))
            # Otherwise make a new list to store elements of this name
            else:
                self.elementDict[i.Name] = [ElementInterface(i)]

    # Method to get all names of elements that have been put into the interface
    def get_element_names(self):
        return self.elementDict.keys()

    # Method to get a list of all elements of a certain name
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

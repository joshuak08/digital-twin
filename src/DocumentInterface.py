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
Each Interface stores its underlying Revit object for the sake of direct document access for modifying the
document or making another query.
"""


class DocumentInterface:
    # DocumentInterface initilisation, takes in a document, collector, and list of categories
    def __init__(self, document, collector, categories, testing):
        self.underlyingDocument = document  # saves the actual revit document in the object
        self.elementDict = {}  # initialises the dictionary to store elements
        newcollector = collector.WhereElementIsNotElementType()  # removes element types from the collector
        elements = []
        # If categories have been specified, union together all elements from specified categories
        if len(categories) != 0:
            for i in categories:
                if testing:
                    categoryElements = newcollector.OfCategory(i)
                else:
                    categoryElements = DB.FilteredElementCollector(document).WhereElementIsNotElementType().OfCategory(i)
                elements.append(categoryElements)
        # If not then the collector is unmodified (all elements passed through)
        else:
            elements = [newcollector]
        # At this point the collector should contain all elements belonging to specified categories
        # if categories are specified, otherwise should have all elements
        # Then goes through all of these elements, and adds them to the dictionary
        for category in elements:
            # If the name of the element is already a key in the dictionary - add it to the list of elements with that
            # name (before being added, the elements are converted into ElementInterfaces
            for i in category:
                if not (i is None):
                    try:
                        name = i.Category.Name.replace(" ", "_")
                    except:
                        name = "unnamed"
                    if name in self.elementDict:
                        self.elementDict[name].append(ElementInterface(i, name))
                    # Otherwise make a new list to store elements of this name
                    else:
                        self.elementDict[name] = [ElementInterface(i, name)]

    # Method to get all names of elements that have been put into the interface
    def get_element_names(self):
        return self.elementDict.keys()

    # Method to get a list of all elements of a certain name
    def get_elements_of_name(self, name):
        return self.elementDict[name]


# Interface for dealing with individual elements from a Revit document
class ElementInterface:
    # Initialisation - takes in a revit element, produces an Interface
    def __init__(self, element, name):
        # Basically just copying info from the element (can be expanded on if there's anything extra we want)
        self.name = name
        self.elementID = element.Id.IntegerValue
        self.underlyingElement = element
        self.parameters = {}
        # Dealing with parameters - formatting them into a dictionary
        for i in element.Parameters:
            # Excludes parameters that don't have values, this can be removed if needed
            if i.HasValue:
                if not (i is None):
                    try:
                        name = i.Definition.Name
                    except:
                        name = "unnamed"
                    self.parameters[name] = ParameterInterface(i)

    # Whether the element has a parameter of a certain name
    def has_parameter(self, parametername):
        return parametername in self.parameters

    # Retrieving a parameter of a certain name
    def get_parameter(self, parametername):
        if self.has_parameter(parametername):
            return self.parameters[parametername]
        else:
            return "No such parameter"


# Interface for storing parameters, strips away a bunch of the extra unused data
class ParameterInterface:

    # To create a ParameterInterface you pass in a revit parameter
    def __init__(self, parameter):
        # Mostly just copying data from the revit parameter
        # Metadata about a parameter is mostly stored in it's .Definition
        try:
            name = parameter.Definition.Name
        except:
            name = "unnamed"
        self.name = name
        self.underlyingParameter = parameter
        # Revit parameters have 4 possible data types - Ints, Doubles, Strings, ValueStrings
        # It seems that all parameters have either a Double value or ValueString defined, so storing the others isn't
        # necessary, can be changed if needed
        try:
            self.stringValue = parameter.AsValueString()
            self.stringValue = self.stringValue.replace('"', ' inches')
        except:
            self.stringValue = ""
        try:
            self.numericalValue = parameter.AsDouble()
        except:
            self.numericalValue = 0


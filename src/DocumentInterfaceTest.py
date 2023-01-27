import unittest
import DocumentInterface


# Dummy class to simulate a Revit document - initialised with a list of elements (which are assumed to be TestElements)
class TestDocument:

    def __init__(self, elements):
        self.elementList = []
        for i in elements:
            self.elementList.append(i)


# Dummy class to simulate a Revit FilteredElementCollector - initialised with a list of elements (which are assumed
# to be TestElements)
class TestCollector:
    def __init__(self, elements):
        self.filteredElements = []
        for i in elements:
            self.filteredElements.append(i)

    # Iteration method to allow iteration through the collector - in the same way you could iterate through a Revit
    # collector
    def __iter__(self):
        return TestCollectorIterator(self)

    # Next 3 methods are intended to simulate the methods of the same name in FilteredElementCollectors
    # Returns a new collector with ElementType elements removed
    def WhereElementIsNotElementType(self):
        newElements = []
        for i in self.filteredElements:
            if not i.isElementType:
                newElements.append(i)
        return TestCollector(newElements)

    # Filters out elements not of the specified category, returns collector with these elements removed
    def OfCategory(self, category):
        newElements = []
        for i in self.filteredElements:
            if i.Category.Name == category:
                newElements.append(i)
        return TestCollector(newElements)

    # Unions the elements of two collectors together into a new collector
    def UnionWith(self, collector):
        newElements = []
        for i in self.filteredElements:
            if i not in newElements:
                newElements.append(i)
        for i in collector.filteredElements:
            if i not in newElements:
                newElements.append(i)

        return TestCollector(newElements)


# Iterator class for TestCollectors
class TestCollectorIterator:
    def __init__(self, collector):
        self.collector = collector
        self.index = 0

    def next(self):
        if self.index < len(self.collector.filteredElements):
            result = self.collector.filteredElements[self.index]
            self.index += 1
            return result
        raise StopIteration


# Simulates a revit element - only contains the attributes needed for testing - not the full range of behavoiour that
# revit elements have
# Initialised with whether the element is an ElementType, its category, its id, its parameters (as a list), and its name
class TestElement:

    def __init__(self, iselementtype, category, elementid, parameters, name):
        self.isElementType = iselementtype
        self.Category = TestCategory(category)
        self.Id = TestId(elementid)
        self.Parameters = parameters
        self.Name = name


class TestId:

    def __init__(self, elementid):
        self.IntegerValue = elementid


class TestCategory:

    def __init__(self, category):
        self.Name = category


# Simulates revit parameters, initialised with its name, its string value, and its numerical value
class TestParameter:

    def __init__(self, name, string, double):
        self.Definition = TestDefinition(name)
        self.stringVal = string
        self.doubleVal = double
        self.HasValue = True

    # Next two methods are just there so the parameter behaves the same as a Revit parameter - basically just getters
    def AsValueString(self):
        return self.stringVal

    def AsDouble(self):
        return self.doubleVal


# Basic Definition class to simulate a revit definition - initialised with a name - other functionality is not needed
# for testing
class TestDefinition:

    def __init__(self, name):
        self.Name = name


# The next few functions are for make writing tests a bit easier
# Returns an element type with a given ID
def element_type_element(elementId):
    return TestElement(True, "Generic", elementId, [], "Generic")


# Returns a TestElement of a given category and ID
def element_of_category(category, elementId):
    return TestElement(False, category, elementId, [], category)


# Returns a TestDocument with a combination of documents of various names and types. Needs to be passed 3 category names
def generic_3_cat_document(cat1, cat2, cat3):
    currentId = 0
    elements = []
    for i in range(3):
        elements.append(element_of_category(cat1, currentId))
        currentId += 1
    for i in range(2):
        elements.append((element_of_category(cat2, currentId)))
        currentId += 1
    elements.append(element_of_category(cat3, currentId))
    return TestDocument(elements)


# Main test class
class DocumentInterfaceTests(unittest.TestCase):

    # Tests to ensure that element types are removed from a document when an interface is created
    def test_no_element_types(self):
        element = element_type_element(0)
        document = TestDocument([element])
        collector = TestCollector(document.elementList)
        interface = DocumentInterface.DocumentInterface(document, collector, [], True)
        self.assertEqual(len(interface.elementDict), 0)

    # Tests to ensure category filtering works in a generic case
    def test_category_filter(self):
        cat1 = "Category1"
        cat2 = "Category2"
        cat3 = "Category3"
        document = generic_3_cat_document(cat1, cat2, cat3)
        collector = TestCollector(document.elementList)
        interface = DocumentInterface.DocumentInterface(document, collector, [cat1, cat2], True)
        self.assertEqual(len(interface.elementDict), 2)
        self.assertEqual(len(interface.get_elements_of_name(cat1)), 3)
        self.assertEqual(len(interface.get_elements_of_name(cat2)), 2)

    # Tests to make sure that an empty category list means all elements are kept in the interface
    def test_empty_categories(self):
        cat1 = "Category1"
        cat2 = "Category2"
        cat3 = "Category3"
        document = generic_3_cat_document(cat1, cat2, cat3)
        collector = TestCollector(document.elementList)
        interface = DocumentInterface.DocumentInterface(document, collector, [], True)
        self.assertEqual(len(interface.elementDict), 3)

    # Tests that if an element is created with a parameter that this is reflected through has parameter
    def test_has_parameter(self):
        element = TestElement(False, "Generic", 0, [TestParameter("Height", None, 10)], "generic")
        interface = DocumentInterface.ElementInterface(element, "Generic")
        self.assertTrue(interface.has_parameter("Height"))

    # Tests that created parameters return the expected values when put into an interface
    def test_parameter_has_right_value(self):
        element = TestElement(False, "Generic", 0,
                              [TestParameter("Height", None, 10), TestParameter("Material", "Steel", None)], "generic")
        interface = DocumentInterface.ElementInterface(element, "Generic")
        parameter1 = interface.get_parameter("Height")
        parameter2 = interface.get_parameter("Material")
        self.assertEqual(parameter1.numericalValue, 10.0)
        self.assertEqual(parameter2.stringValue, "Steel")


if __name__ == '__main__':
    unittest.main()

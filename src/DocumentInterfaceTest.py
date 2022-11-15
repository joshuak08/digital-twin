import unittest
import DocumentInterface


class TestDocument:
    elementList = []

    def __init__(self, elements):
        for i in elements:
            self.elementList.append(i)


class TestCollector:
    filteredElements = []

    def __init__(self, elements):
        for i in elements:
            self.filteredElements.append(i)

    def WhereElementIsNotElementType(self):
        newElements = []
        for i in self.filteredElements:
            if not i.isElementType:
                newElements.append(i)

        return TestCollector(newElements)

    def OfCategory(self, category):
        newElements = []
        for i in self.filteredElements:
            if i.category == category:
                newElements.append(i)

        return TestCollector(newElements)

    def UnionWith(self, collector):
        newElements = []
        newElements.extend(self.filteredElements)
        newElements.extend(collector.filteredElements)
        return TestCollector(newElements)


class TestElement:
    isElementType = None
    category = None
    Id = None
    Parameters = []

    def __init__(self, iselementtype, category, elementid, parameters):
        self.isElementType = iselementtype
        self.category = category
        self.Id = elementid
        self.Parameters = parameters


class TestParameter:
    Definition = None
    stringVal = None
    doubleVal = None

    def __init__(self, name, string, double):
        self.Definition = TestDefinition(name)
        self.stringVal = string
        self.doubleVal = double

    def AsValueString(self):
        return self.stringVal

    def AsDouble(self):
        return self.doubleVal


class TestDefinition:
    Name = None

    def __init__(self, name):
        self.Name = name


def element_type_element(elementId):
    return TestElement(True, "Generic", elementId, [])


def element_of_category(category, elementId):
    return TestElement(False, category, elementId, [])


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


class DocumentInterfaceTests(unittest.TestCase):

    def test_no_element_types(self):
        element = element_type_element(0)
        document = TestDocument([element])
        collector = TestCollector(document.elementList)
        interface = DocumentInterface.DocumentInterface(document, collector, [])
        self.assertEqual(len(interface.elementDict), 0)

    def test_category_filter(self):
        cat1 = "Category1"
        cat2 = "Category2"
        cat3 = "Category3"
        document = generic_3_cat_document(cat1, cat2, cat3)
        collector = TestCollector(document.elementList)
        interface = DocumentInterface.DocumentInterface(document, collector, [cat1, cat2])
        self.assertEqual(len(interface.elementDict), 2)
        self.assertEqual(len(interface.get_elements_of_name(cat1)), 3)
        self.assertEqual(len(interface.get_elements_of_name(cat2)), 2)

    def test_empty_categories(self):
        cat1 = "Category1"
        cat2 = "Category2"
        cat3 = "Category3"
        document = generic_3_cat_document(cat1, cat2, cat3)
        collector = TestCollector(document.elementList)
        interface = DocumentInterface.DocumentInterface(document, collector, [])
        self.assertEqual(len(interface.elementDict), 3)

    def test_has_parameter(self):
        element = TestElement(False, "Generic", 0, [TestParameter("Height", None, 10)])
        interface = DocumentInterface.ElementInterface(element)
        self.assertTrue(interface.has_parameter("Height"))

    def test_parameter_has_right_value(self):
        element = TestElement(False, "Generic", 0, [TestParameter("Height", None, 10), TestParameter("Material", "Steel", None)])
        interface = DocumentInterface.ElementInterface(element)
        parameter1 = interface.get_parameter("Height")
        parameter2 = interface.get_parameter("Material")
        self.assertEqual(parameter1.numericalValue, 10.0)
        self.assertEqual(parameter2.stringValue, "Steel")


if __name__ == '__main__':
    unittest.main()

import unittest


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


if __name__ == '__main__':
    unittest.main()

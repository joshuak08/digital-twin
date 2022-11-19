class TestDocument:
    def __init__(self, elements):
        self.elementList = []
        for i in elements:
            self.elementList.append(i)


class TestElement:
    def __init__(self, iselementtype, category, elementid, parameters, name):
        self.isElementType = iselementtype
        self.category = category
        self.Id = elementid
        self.Parameters = parameters
        self.Name = name


class TestDefinition:
    def __init__(self, name):
        self.Name = name


class TestParameter:
    def __init__(self, name, string, double):
        self.Definition = TestDefinition(name)
        self.stringVal = string
        self.doubleVal = double
        self.HasValue = True

    def convert_to_string(self):
        string = self.Definition.Name + ',' + self.stringVal + ',' + str(self.doubleVal) + ',' + str(self.HasValue)
        return string

    def as_value_string(self):
        return self.stringVal

    def as_double(self):
        return self.doubleVal


def element_type_element(elementId, params):
    return TestElement(True, "Generic", elementId, params, "Generic")
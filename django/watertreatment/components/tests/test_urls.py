from django.test import TestCase
from django.urls import resolve, reverse
from components.views import revitModel, simulation, carousel

class TestUrls(TestCase):
    def testHome(self):
        url = '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def testRevitModel(self):
        url = '/revit-model/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def testRevitModelResolve(self):
        url = reverse('components-revit-model')
        response = resolve(url)
        self.assertEqual(response.func, revitModel)

    # Need to figure out how to open database to run tests for pages that need to access tables and database
    # def testSimulation(self):
    #     url = reverse('components-simulation')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)


    # Will test when forms merged into dev
    # def testForms(self):
    #     url = reverse('components-test-form')
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)

    """
    Or write tests like this, both works
    def testRevitModel(self):
        url = reverse('components-revit-model')
        response = resolve(url)
        self.assertEqual(response.func, revitModel)
    """
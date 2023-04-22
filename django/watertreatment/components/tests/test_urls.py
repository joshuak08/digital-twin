from django.test import TestCase, Client
from django.urls import resolve, reverse
from components.views import *
from components.models import *

class TestUrls(TestCase):
    def setUp(self):
        self.client = Client()

    def testHome_at_correct_location(self):
        url = '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def testHome_url_available_by_name(self):
        url = reverse('components-home')
        response = resolve(url)
        self.assertEqual(response.func, home)
        self.assertEqual(self.client.get(url).status_code, 200)

    def testRevitModel_at_correct_location(self):
        url = '/revit-model/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def testRevitModel_url_available_by_name(self):
        url = reverse('components-revit-model')
        response = resolve(url)
        self.assertEqual(response.func, revitModel)
        self.assertEqual(self.client.get(url).status_code, 200)

    def testTypes_at_correct_location(self):
        url = '/types/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/types.html')

    def testTypes_url_available_by_name(self):
        url = reverse('components-types')
        response = resolve(url)
        self.assertEqual(response.func, types)
        self.assertEqual(self.client.get(url).status_code, 200)

    # Need to figure out how to test each element type page
    # def testElementsOfTypes_at_correct_location(self):
    #     elements = Document.objects.all()
    #     url = '/types/'
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'components/types.html')
    #
    # def testElementsOfTypes_url_available_by_name(self):
    #     url = reverse('components-types')
    #     response = resolve(url)
    #     self.assertEqual(response.func, types)
    #     self.assertEqual(self.client.get(url).status_code, 200)
    #
    # def testElements_at_correct_location(self):
    #     url = '/types/'
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'components/types.html')
    #
    # def testElements_url_available_by_name(self):
    #     url = reverse('components-types')
    #     response = resolve(url)
    #     self.assertEqual(response.func, types)
    #     self.assertEqual(self.client.get(url).status_code, 200)

    def testSimulation_at_correct_location(self):
        url = '/simulation/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/simulation.html')

    def testSimulation_url_available_by_name(self):
        url = reverse('components-simulation')
        response = resolve(url)
        self.assertEqual(response.func, simulation)
        self.assertEqual(self.client.get(url).status_code, 200)


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
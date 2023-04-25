from django.test import TestCase, Client, utils
from django.urls import resolve, reverse
from components.views import *
from components.models import *


# Integration testing
class TestUrls(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.data = Document.objects.create(elemID=12345, name='testing',
                                           params='{"Testing 1" : "1", "Testing 2" : "2"}')

    def testHome_at_correct_location(self):
        url = '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/new-base.html')

    def testHome_url_available_by_name(self):
        url = reverse('components-home')
        resolved = resolve(url)
        response = self.client.get(url)
        self.assertEqual(resolved.func, home)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/home.html')
        self.assertTemplateUsed(response, 'components/new-base.html')

    def testRevitModel_at_correct_location(self):
        url = '/revit-model/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/new-base.html')
        self.assertTemplateUsed(response, 'components/revit-model.html')

    def testRevitModel_url_available_by_name(self):
        url = reverse('components-revit-model')
        resolved = resolve(url)
        response = self.client.get(url)
        self.assertEqual(resolved.func, revitModel)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/new-base.html')
        self.assertTemplateUsed(response, 'components/revit-model.html')

    def testTypes_at_correct_location(self):
        url = '/types/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/types.html')
        self.assertTemplateUsed(response, 'components/new-base.html')

    def testTypes_url_available_by_name(self):
        url = reverse('components-types')
        resolved = resolve(url)
        response = self.client.get(url)
        self.assertEqual(resolved.func, types)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/new-base.html')
        self.assertTemplateUsed(response, 'components/types.html')

    def testElementsOfTypes_url_available_by_name(self):
        url = reverse('components-elements-of-type', args=[self.data])
        resolved = resolve(url)
        response = self.client.get(url)
        self.assertEqual(resolved.func, elementsOfType)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/elements-of-type.html')
        self.assertTemplateUsed(response, 'components/new-base.html')

    def testElementsOfTypes_at_correct_location(self):
        url = '/types/' + self.data.name + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/elements-of-type.html')
        self.assertTemplateUsed(response, 'components/new-base.html')

    def testElements_at_correct_location(self):
        url = '/types/' + self.data.name + '/' + str(self.data.elemID) + '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/element.html')
        self.assertTemplateUsed(response, 'components/new-base.html')

    def testElements_url_available_by_name(self):
        url = reverse('components-elements', args=[self.data.name, self.data.elemID])
        resolved = resolve(url)
        response = self.client.get(url)
        self.assertEqual(resolved.func, elements)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/new-base.html')
        self.assertTemplateUsed(response, 'components/element.html')

    def testSimulation_at_correct_location(self):
        url = '/simulation/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/simulation.html')
        self.assertTemplateUsed(response, 'components/new-base.html')

    def testSimulation_url_available_by_name(self):
        url = reverse('components-simulation')
        resolved = resolve(url)
        response = self.client.get(url)
        self.assertEqual(resolved.func, simulation)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/new-base.html')
        self.assertTemplateUsed(response, 'components/simulation.html')

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

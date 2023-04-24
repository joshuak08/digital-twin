from django.test import TestCase, Client
from django.urls import resolve, reverse
from components.views import *
from components.models import *
from parameterized import parameterized, parameterized_class


class TestUrls(TestCase):
    def setUp(self):
        self.client = Client()
        # elements = Document.objects.all()
        # types = []
        # for i in elements:
        #     if i.name not in types:
        #         types.append(str(i.name))
        #     else:
        #         continue
        # self.types = types
        # self.elements = elements

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

    # def createNewDB(self):

    # def testTypes_at_correct_location(self):
    #     url = '/types/'
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'components/types.html')
    #     self.assertTemplateUsed(response, 'components/new-base.html')

    # def testTypes_url_available_by_name(self):
    #     url = reverse('components-types')
    #     resolved = resolve(url)
    #     response = self.client.get(url)
    #     self.assertEqual(resolved.func, types)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'components/new-base.html')
    #     self.assertTemplateUsed(response, 'components/types.html')

    # def testSomething(self):
    #

    # Need to figure out how to test each element type page
    # def testElementsOfTypes_url_available_by_name(self):
    #     for t in self.types:
    #         url = reverse('components-elements-of-type', args=[t])
    #         resolved = resolve(url)
    #         response = self.client.get(url)
    #         self.assertEqual(resolved.func, elementsOfType)
    #         self.assertEqual(response.status_code, 200)
    #         self.assertTemplateUsed(response, 'components/elements-of-type.html')
    #         self.assertTemplateUsed(response, 'components/new-base.html')
    #
    # def testElementsOfTypes_at_correct_location(self):
    #     url = '/types/'
    #     for t in self.types:
    #         finalUrl = url + t + '/'
    #         response = self.client.get(finalUrl)
    #         self.assertEqual(response.status_code, 200)
    #         self.assertTemplateUsed(response, 'components/elements-of-type.html')
    #         self.assertTemplateUsed(response, 'components/new-base.html')
    # #
    #
    # # Tests not working
    # def testElements_at_correct_location(self):
    #     url = '/types/'
    #     for t in self.types:
    #         elements = Document.objects.filter(name=type)
    #         for i in elements:
    #             finalUrl = url + t + '/' + str(i.elemID) + '/'
    #             response = self.client.get(finalUrl)
    #             self.assertEqual(response.status_code, 200)
    #             self.assertTemplateUsed(response, 'components/elements.html')
    #             self.assertTemplateUsed(response, 'components/new-base.html')
    #
    # # Tests not working
    # def testElements_url_available_by_name(self):
    #     for t in self.types:
    #         elements = Document.objects.filter(name=type)
    #         for i in elements:
    #             print('test')
    #             url = reverse('components-elements', args=[t, str(i.elemID)])
    #             resolved = resolve(url)
    #             response = self.client.get(url)
    #             print(resolved.func)
    #             assert 1 == 2
    #             self.assertEqual(resolved.func, elements)
    #             self.assertEqual(response.status_code, 200)
    #             self.assertTemplateUsed(response, 'components/new-base.html')
    #             self.assertTemplateUsed(response, 'components/elements.html')

    # def testSimulation_at_correct_location(self):
    #     url = '/simulation/'
    #     response = self.client.get(url)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'components/simulation.html')
    #     self.assertTemplateUsed(response, 'components/new-base.html')
    #
    # def testSimulation_url_available_by_name(self):
    #     url = reverse('components-simulation')
    #     resolved = resolve(url)
    #     response = self.client.get(url)
    #     self.assertEqual(resolved.func, simulation)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, 'components/new-base.html')
    #     self.assertTemplateUsed(response, 'components/simulation.html')

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

    # @parameterized([i for i in self.elements])
    # def TestElements(TestCase):
    #     def setUp(self):
    #         self.client = Client()
    #         elements = Document.objects.all()
    #         types = []
    #         for i in elements:
    #             if i.name not in types:
    #                 types.append(str(i.name))
    #             else:
    #                 continue
    #         self.types = types
    #         self.elements = elements


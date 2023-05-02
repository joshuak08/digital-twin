from django.test import TestCase
from django.urls import reverse
from components.views import *

# Tests for views methods
class TestViews(TestCase):
    def test_home_GET(self):
        response = self.client.get(reverse('components-home'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/new-base.html')
        self.assertTemplateUsed(response, 'components/home.html')

    def test_revitModel_GET(self):
        response = self.client.get(reverse('components-revit-model'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'components/new-base.html')
        self.assertTemplateUsed(response, 'components/revit-model.html')

    def testFormDataManipulation(self):
        form = SimInputForm(
            data={'csrfmiddlewaretoken': 'asdfjkl', 'tank0': 1, 'tank1': 1, 'tank2': 1, 'tank3': 1, 'average_flow': 0.2,
                  'average_tss': 252, 'sim_length': 20})
        formData = form.__dict__['data']
        self.assertTrue('csrfmiddlewaretoken' in formData)
        formData, initial_particulate = formDataManipulation(formData)
        self.assertFalse('csrfmiddlewaretoken' in formData)
        self.assertTrue('testing' in formData)
        self.assertEqual(formData['testing'], False)

        testingForm = SimInputForm(
            data={'csrfmiddlewaretoken': 'asdfjkl', 'tank0': 1, 'tank1': 1, 'tank2': 1, 'tank3': 1, 'average_flow': 0.2,
                  'average_tss': 252, 'sim_length': 20, 'testing': 'on'}
        )
        testingFormData = testingForm.__dict__['data']
        self.assertTrue('csrfmiddlewaretoken' in testingFormData)
        testingFormData, initial_particulate = formDataManipulation(testingFormData)
        self.assertFalse('csrfmiddlewaretoken' in testingFormData)
        self.assertTrue('testing' in testingFormData)
        self.assertEqual(testingFormData['testing'], True)

from django.test import TestCase, Client
from django.urls import reverse
from components.views import *
import json

class TestViews(TestCase):

    def setUp(self):
        self.client = Client()

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
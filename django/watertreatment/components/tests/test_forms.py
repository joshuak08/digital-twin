from django.test import TestCase, Client
from django.urls import reverse
from components.views import form
from components.models import SimInput
from components.forms import SimInputForm


class TestForms(TestCase):
    def testSimInputForm_valid_data(self):
        form = SimInputForm(data={
            'tank0': 1,
            'tank1': 1,
            'tank2': 1,
            'tank3': 1,
            'average_flow': 0.2,
            'average_tss': 252,
            'sim_length': 20,
            'testing': False
        })

        self.assertTrue(form.is_valid())

    def testSimInputForm_not_valid(self):
        form = SimInputForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)


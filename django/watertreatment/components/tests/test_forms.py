from django.test import TestCase, Client
from django.urls import reverse
from components.views import form
from components.models import SimInput
from components.forms import SimInputForm


class TestForms(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.form = SimInputForm(data={
            'csrfmiddlewaretoken': 'asdfjkl',
            'tank0': 1,
            'tank1': 1,
            'tank2': 1,
            'tank3': 1,
            'average_flow': 0.2,
            'average_tss': 252,
            'sim_length': 20,
        })

    def testSimInputForm_valid_data(self):
        self.assertTrue(self.form.is_valid())

    def testSimInputForm_not_valid(self):
        form = SimInputForm(data={})

        self.assertFalse(form.is_valid())
        self.assertEqual(len(form.errors), 3)

    def test_empty_form(self):
        form = SimInputForm(data={})
        self.assertIn("tank0", form.fields)
        self.assertIn("tank1", form.fields)
        self.assertIn("tank2", form.fields)
        self.assertIn("tank3", form.fields)
        self.assertIn("average_flow", form.fields)
        self.assertIn("average_tss", form.fields)
        self.assertIn("sim_length", form.fields)
        self.assertIn("testing", form.fields)

    def testFormRedirect(self):
        response = self.client.post('/input-form/', self.form.data)
        self.assertEqual(response.status_code, 302)

# TODO: Figure out what more tests needed for forms and whole application
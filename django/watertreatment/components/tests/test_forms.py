from django.test import TestCase
from components.forms import SimInputForm

# Tests for input forms
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
        self.assertEqual(len(form.errors), 7)

    def test_empty_form(self):
        form = SimInputForm(data={})
        self.assertIn("tank0", form.fields)
        self.assertIn("tank1", form.fields)
        self.assertIn("tank2", form.fields)
        self.assertIn("tank3", form.fields)
        self.assertIn("average_flow", form.fields)
        self.assertIn("average_tss", form.fields)
        self.assertIn("sim_length", form.fields)

    def testFormRedirect(self):
        response = self.client.post('/input-form/', self.form.data)
        self.assertEqual(response.status_code, 302)

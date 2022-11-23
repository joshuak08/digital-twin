from django.test import TestCase


# Create your tests here.

class TestView(TestCase):

    def testHome(self):
        url = '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

       
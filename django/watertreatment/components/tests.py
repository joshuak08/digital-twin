from django.test import TestCase
from .models import Post
from django.urls import reverse


# Create your tests here.

class TestPosts(TestCase):

    def test_same_post(self):
        name = "TestName"
        postID = 123
        content = "TestContent"
        params = {'TestParam': 456}
        post1 = Post(name, postID, content, params)
        post2 = Post(name, postID, content, params)
        self.assertEqual(post1, post2)

    def test_post_id_integer(self):
        int_id = 1
        post_int_id = Post(None, int_id, None, None)
        self.assertTrue(post_int_id, isinstance(post_int_id.elementID, int))

    def test_client(self):
        # post = Post(None, None, None, None)
        response = self.client.get(reverse('components-home'))
        print(response.status_code)


class TestView(TestCase):

    def testHome(self):
        url = '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

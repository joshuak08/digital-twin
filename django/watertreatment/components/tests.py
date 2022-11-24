from django.test import TestCase
from .models import Post


# Create your tests here.

class TestPosts(TestCase):

    def testCreatePost(self):
        name = "TestName"
        postID = 123
        content = "TestContent"
        params = {'TestParam': 456}
        post1 = Post(name, postID, content, params)
        post2 = Post(name, postID, content, params)
        self.assertEqual(post1, post2)


class TestView(TestCase):

    def testHome(self):
        url = '/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

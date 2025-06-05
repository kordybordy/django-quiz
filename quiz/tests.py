from django.test import TestCase
from django.urls import reverse

class QuizViewsTest(TestCase):
    def test_index_redirects_to_check_cookie(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse('check_cookie'))


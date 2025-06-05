from django.test import TestCase
from django.urls import reverse


class QuizRoutingTests(TestCase):
    def test_root_redirects_to_quiz(self):
        response = self.client.get('/')
        self.assertRedirects(response, reverse('quiz'))

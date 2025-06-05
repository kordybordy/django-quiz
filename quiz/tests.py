from django.test import TestCase, Client
from django.urls import reverse


class QuizRoutingTests(TestCase):
    def test_root_redirects_to_quiz(self):
        response = self.client.get('/')
        self.assertRedirects(response, reverse('quiz'))


class SkipQuestionTests(TestCase):
    def setUp(self):
        self.client.get('/')

    def test_skipping_moves_question_to_end(self):
        session = self.client.session
        first_question = session['quiz']['questions'][0]
        response = self.client.post(reverse('quiz'), {'action': 'skip'})
        self.assertRedirects(response, reverse('quiz'))
        session = self.client.session
        self.assertEqual(session['quiz']['current'], 0)
        self.assertEqual(session['quiz']['questions'][-1], first_question)


class CookiesRequiredTests(TestCase):
    def test_first_get_without_cookies_redirects_to_index(self):
        response = self.client.get('/quiz/')
        self.assertRedirects(
            response, reverse('index'), fetch_redirect_response=False
        )

    def test_missing_cookies_after_index_redirects_to_warning(self):
        self.client.get('/')
        new_client = Client()
        response = new_client.get('/quiz/')
        self.assertRedirects(
            response, reverse('cookies_required'), fetch_redirect_response=False
        )

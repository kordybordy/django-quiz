from django.test import TestCase
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

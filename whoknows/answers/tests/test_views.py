from django.test import TestCase
from tests.mixins import BaseTestMixins
from answers.forms import AnswerForm
from django.urls import reverse
from questions.models import Question
from answers.models import Answer
from django.contrib.auth import get_user_model


class AnswerTest(BaseTestMixins, TestCase):

    credentials = {'username': 'john', 'password': 'p@ssw0rd'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_test_data()

    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.first()

    def test_invalid_form_returns_error(self):
        self.client.post(reverse('account:login'), self.credentials)
        form = AnswerForm(data={'user': '', 'content': '', 'question': ''})
        response = self.client.post(reverse('answers:create_answer'),
                                    data={'answer_form': form})
        self.assertEqual(response.status_code, 400)
        response_message = response.json()['response']
        self.assertEqual(response_message, 'Invalid Answer')

    def test_invalid_question_returns_error(self):
        self.client.post(reverse('account:login'), self.credentials)
        response = self.client.post(reverse('answers:create_answer'),
                                    data={'user': self.user.id,
                                          'question': '500',
                                          'content': 'test answer'})
        self.assertEqual(response.status_code, 400)
        response_message = response.json()['response']
        self.assertEqual(response_message, 'Invalid Answer')

    def test_user_must_login_to_answer(self):
        question = Question.objects.first()
        response = self.client.post(reverse('answers:create_answer'),
                                    data={'user': self.user.id,
                                          'content': 'test answer',
                                          'question': question.id})
        response_message = response.json()['response']
        self.assertIn('login required', response_message)

    def test_successful_answer(self):
        self.client.post(reverse('account:login'), self.credentials)
        question = Question.objects.last()
        num_answers = Answer.objects.count()
        response = self.client.post(reverse('answers:create_answer'),
                                    data={'answer-user': self.user.id,
                                          'answer-content': 'test answer',
                                          'answer-question': question.id})
        self.assertEqual(response.status_code, 200)
        response_message = response.json()['response']
        self.assertEqual(response_message, 'Answer created')
        self.assertEqual(Answer.objects.count(), num_answers + 1)

    def test_user_can_only_answer_question_once(self):
        self.client.post(reverse('account:login'), self.credentials)
        question = Question.objects.first()
        self.client.post(reverse('answers:create_answer'),
                         data={'answer-user': self.user.id,
                               'answer-content': 'test answer',
                               'answer-question': question.id})
        self.assertEqual(Answer.objects.count(), 1)
        response = self.client.post(reverse('answers:create_answer'),
                                    data={'answer-user': self.user.id,
                                          'answer-content': 'test second answer',
                                          'answer-question': question.id})
        self.assertEqual(response.status_code, 400)
        response_message = response.json()['response']
        self.assertEqual(response_message, 'You have already answered this question')
        self.assertEqual(Answer.objects.count(), 1)

from django.test import TestCase
from tests.mixins import BaseTestMixins
from answers.forms import AnswerForm
from django.urls import reverse
from questions.models import Question
from answers.models import Answer
from django.contrib.auth import get_user_model


class AnswerTest(BaseTestMixins, TestCase):

    credentials = {'username': 'john', 'password': 'p@ssw0rd'}
    second_user_credentials = {'username': 'sally', 'password': 'p@ssw0rd'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_test_data()
        cls.create_second_user()

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
        self.assertEqual(response.status_code, 400)
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

    def test_user_must_login_to_accept_answer(self):
        response = self.client.post(reverse('answers:toggle_accept'), data={'answer_id': 1})
        response_message = response.json()['response']
        self.assertEqual(response.status_code, 400)
        self.assertIn('login required', response_message)
        answer = Answer.objects.first()
        self.assertEqual(answer.accepted, False)

    def test_accept_invalid_answer_returns_error(self):
        self.client.post(reverse('account:login'), self.credentials)
        response = self.client.post(reverse('answers:toggle_accept'), data={'answer_id': 500})
        response_message = response.json()['response']
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid answer', response_message)

    def test_only_question_initiator_can_accept_answer(self):
        self.client.post(reverse('account:login'), self.second_user_credentials)
        answer = Answer.objects.first()
        response = self.client.post(reverse('answers:toggle_accept'), data={'answer_id': answer.id})
        response_message = response.json()['response']
        self.assertEqual(response.status_code, 400)
        self.assertIn('Invalid user', response_message)
        answer.refresh_from_db()
        self.assertEqual(answer.accepted, False)

    def test_accept_answer(self):
        self.client.post(reverse('account:login'), self.credentials)
        answer = Answer.objects.first()
        response = self.client.post(reverse('answers:toggle_accept'), data={'answer_id': answer.id})
        response_message = response.json()['response']
        self.assertEqual(response.status_code, 200)
        self.assertIn('Accepted answer toggled', response_message)
        answer.refresh_from_db()
        self.assertEqual(answer.accepted, True)

    def test_cannot_accept_multiple_answers(self):
        # first question already contains one answer from create_test_data.
        # Add another answer from a different user
        question = Question.objects.first()
        second_user = get_user_model().objects.get(username=self.second_user_credentials['username'])
        Answer.objects.create(user=second_user, question=question, content='test second answer')

        # login with first user and accept first answer
        self.client.post(reverse('account:login'), self.credentials)
        first_answer = question.answer_set.first()
        self.client.post(reverse('answers:toggle_accept'), data={'answer_id': first_answer.id})
        first_answer.refresh_from_db()
        self.assertEqual(first_answer.accepted, True)

        # accept the second answer and confirm that only one answer in total is accepted
        second_answer = question.answer_set.last()
        self.client.post(reverse('answers:toggle_accept'), data={'answer_id': second_answer.id})
        second_answer.refresh_from_db()
        self.assertEqual(second_answer.accepted, True)
        num_accepted_answers = Answer.objects.filter(question=question, accepted=True).count()
        self.assertEqual(num_accepted_answers, 1)

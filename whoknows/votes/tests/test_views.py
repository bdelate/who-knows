from django.test import TestCase
from tests.mixins import BaseTestMixins
from votes.forms import VoteForm
from django.urls import reverse
from questions.models import Question


class UpVoteQuestionTest(BaseTestMixins, TestCase):

    credentials = {'username': 'john', 'password': 'p@ssw0rd'}
    second_user_credentials = {'username': 'sally', 'password': 'p@ssw0rd'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_test_data()
        cls.create_second_user()

    def test_invalid_form_returns_error(self):
        form = VoteForm(data={'object_id': '', 'vote_type': ''})
        response = self.client.post(reverse('votes:up_vote'), data={'vote_form': form})
        response_message = response.json()['response']
        self.assertEqual(response_message, 'Invalid Vote')

    def test_invalid_question_returns_error(self):
        response = self.client.post(reverse('votes:up_vote'), data={'object_id': '500', 'vote_type': 'question'})
        response_message = response.json()['response']
        self.assertEqual(response_message, 'Invalid Question')

    def test_user_must_login_to_vote(self):
        question = Question.objects.first()
        response = self.client.post(reverse('votes:up_vote'), data={'object_id': question.id, 'vote_type': 'question'})
        response_message = response.json()['response']
        self.assertIn('You have to be logged in to vote', response_message)

    def test_user_cannot_vote_for_own_question(self):
        self.client.post(reverse('account:login'), self.credentials)
        question = Question.objects.first()
        response = self.client.post(reverse('votes:up_vote'), data={'object_id': question.id, 'vote_type': 'question'})
        response_message = response.json()['response']
        self.assertEqual(response_message, 'You cannot vote for your own question')

    def test_user_can_only_vote_for_question_once(self):
        self.client.post(reverse('account:login'), self.second_user_credentials)
        question = Question.objects.first()
        self.client.post(reverse('votes:up_vote'), data={'object_id': question.id, 'vote_type': 'question'})
        response = self.client.post(reverse('votes:up_vote'), data={'object_id': question.id, 'vote_type': 'question'})
        response_message = response.json()['response']
        self.assertEqual(response_message, 'You have already voted for this question')

    def test_successful_vote(self):
        self.client.post(reverse('account:login'), self.second_user_credentials)
        question = Question.objects.first()
        response = self.client.post(reverse('votes:up_vote'), data={'object_id': question.id, 'vote_type': 'question'})
        response_message = response.json()['response']
        self.assertEqual(response_message, 'Thanks for your vote')

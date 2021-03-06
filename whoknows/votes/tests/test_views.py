from django.contrib.auth import get_user_model
from django.test import TestCase
from tests.mixins import BaseTestMixins
from votes.forms import VoteForm
from django.urls import reverse
from questions.models import Question
from comments.models import Comment
from answers.models import Answer
from django.db import transaction


class GenericVoteTests:
    """View tests that are common to up voting and removing votes"""

    def test_invalid_form_returns_error(self, url):
        form = VoteForm(data={'object_id': '', 'vote_type': ''})
        response = self.client.post(reverse(url), data={'vote_form': form})
        self.assertEqual(response.status_code, 400)
        response_message = response.json()['response']
        self.assertEqual(response_message, 'Invalid Vote')

    def test_invalid_object_returns_error(self, url, vote_type):
        response = self.client.post(reverse(url),
                                    data={'object_id': 500,
                                          'vote_type': vote_type})
        self.assertEqual(response.status_code, 400)
        response_message = response.json()['response']
        self.assertEqual(response_message, 'Invalid {}'.format(vote_type))


class UpVoteTest(BaseTestMixins, GenericVoteTests, TestCase):

    credentials = {'username': 'john', 'password': 'p@ssw0rd'}
    second_user_credentials = {'username': 'sally', 'password': 'p@ssw0rd'}

    @classmethod
    def setUpTestData(cls):
        cls.create_test_data()
        cls.create_second_user()

    def test_invalid_form_returns_error(self):
        super().test_invalid_form_returns_error(url='votes:up_vote')

    def test_invalid_object_returns_error(self):
        super().test_invalid_object_returns_error(url='votes:up_vote',
                                                  vote_type='question')
        super().test_invalid_object_returns_error(url='votes:up_vote',
                                                  vote_type='comment')
        super().test_invalid_object_returns_error(url='votes:up_vote',
                                                  vote_type='answer')

    def test_user_must_login_to_vote(self):
        self.user_must_login_to_vote(obj=Question.objects.first(),
                                     vote_type='question')
        self.user_must_login_to_vote(obj=Comment.objects.first(),
                                     vote_type='comment')
        self.user_must_login_to_vote(obj=Answer.objects.first(),
                                     vote_type='answer')

    def user_must_login_to_vote(self, obj, vote_type):
        response = self.client.post(reverse('votes:up_vote'),
                                    data={'object_id': obj.id,
                                          'vote_type': vote_type})
        response_message = response.json()['response']
        self.assertIn('Please login or signup before doing this.',
                      response_message)

    def test_user_cannot_vote_for_own_object(self):
        self.user_cannot_vote_for_own_object(obj=Question.objects.first(),
                                             vote_type='question')
        self.user_cannot_vote_for_own_object(obj=Comment.objects.first(),
                                             vote_type='comment')
        self.user_cannot_vote_for_own_object(obj=Answer.objects.first(),
                                             vote_type='answer')

    def user_cannot_vote_for_own_object(self, obj, vote_type):
        self.client.post(reverse('account:login'), self.credentials)
        response = self.client.post(reverse('votes:up_vote'),
                                    data={'object_id': obj.id,
                                          'vote_type': vote_type})
        self.assertEqual(response.status_code, 400)
        response_message = response.json()['response']
        self.assertEqual(response_message,
                         'You cannot vote for your own {}'.format(vote_type))

    def test_user_can_only_vote_for_object_once(self):
        with transaction.atomic():
            obj = Question.objects.first()
            self.user_can_only_vote_for_object_once(obj=obj,
                                                    vote_type='question')
        with transaction.atomic():
            obj = Comment.objects.first()
            self.user_can_only_vote_for_object_once(obj=obj,
                                                    vote_type='comment')
        with transaction.atomic():
            obj = Answer.objects.first()
            self.user_can_only_vote_for_object_once(obj=obj,
                                                    vote_type='answer')

    def user_can_only_vote_for_object_once(self, obj, vote_type):
        self.client.post(reverse('account:login'),
                         self.second_user_credentials)
        self.client.post(reverse('votes:up_vote'),
                         data={'object_id': obj.id,
                               'vote_type': vote_type})
        response = self.client.post(reverse('votes:up_vote'),
                                    data={'object_id': obj.id,
                                          'vote_type': vote_type})
        self.assertEqual(response.status_code, 400)
        response_message = response.json()['response']
        message = 'You have already voted for this {}'.format(vote_type)
        self.assertEqual(response_message, message)

    def test_successful_vote(self):
        self.successful_vote(obj=Question.objects.first(),
                             vote_type='question')
        self.successful_vote(obj=Comment.objects.first(),
                             vote_type='comment')
        self.successful_vote(obj=Answer.objects.first(),
                             vote_type='answer')

    def successful_vote(self, obj, vote_type):
        self.client.post(reverse('account:login'),
                         self.second_user_credentials)
        response = self.client.post(reverse('votes:up_vote'),
                                    data={'object_id': obj.id,
                                          'vote_type': vote_type})
        response_message = response.json()['response']
        self.assertEqual(response_message, 'Thanks for your vote')


class RemoveVoteTest(BaseTestMixins, GenericVoteTests, TestCase):

    second_user_credentials = {'username': 'sally', 'password': 'p@ssw0rd'}

    @classmethod
    def setUpTestData(cls):
        cls.create_test_data()
        cls.create_second_user()

    def test_invalid_form_returns_error(self):
        super().test_invalid_form_returns_error(url='votes:remove_vote')

    def test_invalid_object_returns_error(self):
        super().test_invalid_object_returns_error(url='votes:remove_vote',
                                                  vote_type='question')
        super().test_invalid_object_returns_error(url='votes:remove_vote',
                                                  vote_type='comment')
        super().test_invalid_object_returns_error(url='votes:remove_vote',
                                                  vote_type='answer')

    def test_non_existant_vote_returns_error(self):
        self.client.post(reverse('account:login'),
                         self.second_user_credentials)
        question = Question.objects.first()
        self.non_existant_vote_returns_error(obj=question,
                                             vote_type='question')
        comment = question.comments.first()
        self.non_existant_vote_returns_error(obj=comment, vote_type='comment')
        answer = Answer.objects.get(question=question)
        self.non_existant_vote_returns_error(obj=answer, vote_type='answer')

    def non_existant_vote_returns_error(self, obj, vote_type):
        response = self.client.post(reverse('votes:remove_vote'),
                                    data={'object_id': obj.id,
                                          'vote_type': vote_type})
        self.assertEqual(response.status_code, 400)
        response_message = response.json()['response']
        self.assertEqual(response_message, 'Invalid Vote')

    def test_successful_vote_removal(self):
        username = self.second_user_credentials['username']
        user = get_user_model().objects.get(username=username)
        self.successful_vote_removal(obj=Question,
                                     vote_type='question',
                                     user=user)
        self.successful_vote_removal(obj=Comment,
                                     vote_type='comment',
                                     user=user)
        self.successful_vote_removal(obj=Answer,
                                     vote_type='answer',
                                     user=user)

    def successful_vote_removal(self, obj, vote_type, user):
        obj_instance = obj.objects.first()
        obj_instance.votes.create(voter=user)
        self.client.post(reverse('account:login'),
                         self.second_user_credentials)
        response = self.client.post(reverse('votes:remove_vote'),
                                    data={'object_id': obj_instance.id,
                                          'vote_type': vote_type})
        response_message = response.json()['response']
        self.assertEqual(response_message, 'Your vote has been removed')

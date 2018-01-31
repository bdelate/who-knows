from django.test import TestCase
from tests.mixins import BaseTestMixins
from comments.forms import CommentForm
from django.urls import reverse
from questions.models import Question


class UpVoteQuestionTest(BaseTestMixins, TestCase):

    credentials = {'username': 'john', 'password': 'p@ssw0rd'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_test_data()

    def test_invalid_form_returns_error(self):
        form = CommentForm(data={'object_id': '', 'comment_type': '', 'content': ''})
        response = self.client.post(reverse('comments:create_comment'), data={'comment_form': form})
        self.assertEqual(response.status_code, 400)
        response_message = response.json()['response']
        self.assertEqual(response_message, 'Invalid Comment')

    def test_invalid_question_returns_error(self):
        response = self.client.post(reverse('comments:create_comment'),
                                    data={'object_id': '500', 'comment_type': 'question', 'content': 'test comment'})
        self.assertEqual(response.status_code, 400)
        response_message = response.json()['response']
        self.assertEqual(response_message, 'Invalid Question')

    def test_user_must_login_to_comment(self):
        question = Question.objects.first()
        response = self.client.post(reverse('comments:create_comment'),
                                    data={'object_id': question.id, 'comment_type': 'question', 'content': 'test comment'})
        response_message = response.json()['response']
        self.assertIn('You have to be logged in to comment', response_message)

    def test_successful_comment(self):
        self.client.post(reverse('account:login'), self.credentials)
        question = Question.objects.first()
        response = self.client.post(reverse('comments:create_comment'),
                                    data={'object_id': question.id, 'comment_type': 'question', 'content': 'test comment'})
        response_message = response.json()['response']
        self.assertEqual(response_message, 'Comment created')

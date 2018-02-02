from django.test import TestCase
from tests.mixins import BaseTestMixins
from comments.models import Comment
from questions.models import Question
from django.contrib.auth import get_user_model


class CommentTest(BaseTestMixins, TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_test_data()

    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.first()

    def test_save_and_retrieve(self):
        question = Question.objects.first()
        num_comments = Comment.objects.count()
        question.comments.create(commenter=self.user, content='test comment')
        self.assertEqual(Comment.objects.count(), num_comments + 1)
        comment = Comment.objects.last()
        self.assertEqual(comment.commenter, self.user)
        self.assertEqual(comment.content, 'test comment')

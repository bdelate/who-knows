from django.test import TestCase
from tests.mixins import BaseTestMixins
from comments.models import Comment
from questions.models import Question
from answers.models import Answer
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
        self.save_and_retrieve(obj=question)
        answer = Answer.objects.first()
        self.save_and_retrieve(obj=answer)

    def save_and_retrieve(self, obj):
        num_comments = Comment.objects.count()
        obj.comments.create(commenter=self.user, content='test comment')
        self.assertEqual(Comment.objects.count(), num_comments + 1)
        comment = Comment.objects.last()
        self.assertEqual(comment.commenter, self.user)
        self.assertEqual(comment.content, 'test comment')

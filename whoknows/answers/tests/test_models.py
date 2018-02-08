from django.test import TestCase
from tests.mixins import BaseTestMixins
from answers.models import Answer
from questions.models import Question
from django.contrib.auth import get_user_model


class AnswerTest(BaseTestMixins, TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_test_data()

    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.first()

    def test_save_and_retrieve(self):
        question = Question.objects.first()
        answer = Answer.objects.create(user=self.user,
                                       question=question,
                                       content='test answer')
        self.assertEqual(Answer.objects.count(), 1)
        self.assertEqual(answer.user, self.user)
        self.assertEqual(answer.question, question)
        self.assertEqual(answer.content, 'test answer')

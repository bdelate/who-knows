from django.test import TestCase
from tests.mixins import BaseTestMixins
from answers.models import Answer
from questions.models import Question
from django.contrib.auth import get_user_model


class AnswerTest(BaseTestMixins, TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.create_test_data()

    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.first()

    def test_save_and_retrieve(self):
        question = Question.objects.first()
        num_answers = Answer.objects.count()
        answer = Answer.objects.create(user=self.user,
                                       question=question,
                                       content='test answer')
        self.assertEqual(Answer.objects.count(), num_answers + 1)
        self.assertEqual(answer.user, self.user)
        self.assertEqual(answer.question, question)
        self.assertEqual(answer.content, 'test answer')

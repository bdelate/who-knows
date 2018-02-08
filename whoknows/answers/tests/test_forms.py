from django.test import TestCase
from answers.forms import AnswerForm
from django.contrib.auth import get_user_model
from questions.models import Question
from tests.mixins import BaseTestMixins


class AnswerTest(BaseTestMixins, TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_test_data()

    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.first()

    def test_valid_form(self):
        question = Question.objects.first()
        form = AnswerForm(data={'user': self.user.id, 'content': 'test answer', 'question': question.id})
        self.assertTrue(form.is_valid())

    def test_all_fields_required(self):
        form = AnswerForm(data={'user': '', 'content': '', 'question': ''})
        self.assertFalse(form.is_valid())
        user_error = str(form.errors['user'].as_data()[0].message)
        self.assertEqual(user_error, 'This field is required.')
        content_error = str(form.errors['content'].as_data()[0].message)
        self.assertEqual(content_error, 'This field is required.')
        question_error = str(form.errors['question'].as_data()[0].message)
        self.assertEqual(question_error, 'This field is required.')

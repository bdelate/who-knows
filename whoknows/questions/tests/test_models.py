from django.contrib.auth import get_user_model
from django.test import TransactionTestCase
from questions.models import Question
from django.db.utils import IntegrityError
from django.core.exceptions import ValidationError


class QuestionTest(TransactionTestCase):

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create(username='john')

    def test_save_and_retrieve(self):
        Question.objects.create(user=self.user, title='test title', content='test content')
        question = Question.objects.first()
        self.assertEqual(question.user, self.user)
        self.assertEqual(question.title, 'test title')
        self.assertEqual(question.content, 'test content')

    def test_question_must_have_user(self):
        invalid_question = Question(title='test title', content='test content')
        with self.assertRaises(IntegrityError):
            invalid_question.save()

    def test_question_must_have_title_and_content(self):
        invalid_question = Question(user=self.user)
        with self.assertRaises(ValidationError):
            invalid_question.save()
            invalid_question.full_clean()

    def test_cannot_create_duplicate_titles(self):
        Question.objects.create(user=self.user, title='test title', content='test content')
        with self.assertRaises(IntegrityError):
            Question.objects.create(user=self.user, title='test title', content='test content')

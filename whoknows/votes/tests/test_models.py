from django.test import TestCase
from tests.mixins import BaseTestMixins
from votes.models import Vote
from questions.models import Question
from django.contrib.auth import get_user_model
from django.db.utils import IntegrityError
from django.db import transaction


class VoteTest(BaseTestMixins, TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_test_data()

    def setUp(self):
        user_model = get_user_model()
        self.user = user_model.objects.first()

    def test_save_and_retrieve(self):
        question = Question.objects.first()
        question.votes.create(voter=self.user)
        self.assertEqual(Vote.objects.count(), 1)
        vote = Vote.objects.first()
        self.assertEqual(vote.voter, self.user)

    def test_user_can_only_vote_for_question_once(self):
        question = Question.objects.first()
        question.votes.create(voter=self.user)
        try:
            with transaction.atomic():
                question.votes.create(voter=self.user)
        except IntegrityError:
            pass
        self.assertEqual(Vote.objects.all().count(), 1)

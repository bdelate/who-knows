from django.test import TestCase
from tests.mixins import BaseTestMixins
from votes.models import Vote
from questions.models import Question
from comments.models import Comment
from answers.models import Answer
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

    def test_save_and_retrieve_question_vote(self):
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

    def test_save_and_retrieve_comment_vote(self):
        """
        Test that votes can be created both for question comments
        and answer comments
        """
        objects = [Question.objects.first(),
                   Answer.objects.first()]
        for obj in objects:
            num_votes = Vote.objects.count()
            comment = obj.comments.create(commenter=self.user,
                                          content='test comment')
            comment.votes.create(voter=self.user)
            self.assertEqual(Vote.objects.count(), num_votes + 1)
            vote = Vote.objects.last()
            self.assertEqual(vote.voter, self.user)

    def test_user_can_only_vote_for_comment_once(self):
        question = Question.objects.first()
        question.comments.create(commenter=self.user, content='test comment')
        comment = Comment.objects.first()
        comment.votes.create(voter=self.user)
        try:
            with transaction.atomic():
                comment.votes.create(voter=self.user)
        except IntegrityError:
            pass
        self.assertEqual(Vote.objects.all().count(), 1)

    def test_save_and_retrieve_answer_vote(self):
        answer = Answer.objects.first()
        answer.votes.create(voter=self.user)
        self.assertEqual(Vote.objects.count(), 1)
        vote = Vote.objects.first()
        self.assertEqual(vote.voter, self.user)

    def test_user_can_only_vote_for_answer_once(self):
        answer = Answer.objects.first()
        answer.votes.create(voter=self.user)
        try:
            with transaction.atomic():
                answer.votes.create(voter=self.user)
        except IntegrityError:
            pass
        self.assertEqual(Vote.objects.all().count(), 1)

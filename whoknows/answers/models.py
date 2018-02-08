from django.db import models
from django.conf import settings
from django.contrib.contenttypes.fields import GenericRelation
from votes.models import Vote
from comments.models import Comment
from questions.models import Question


class Answer(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    content = models.TextField()
    accepted = models.BooleanField(default=False)
    votes = GenericRelation(Vote, related_query_name='answers')
    comments = GenericRelation(Comment, related_query_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)

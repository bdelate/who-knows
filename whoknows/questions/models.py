from django.db import models
from django.conf import settings


class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, unique=True)
    content = models.TextField()
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.title

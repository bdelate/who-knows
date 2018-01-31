from django.db import models
from django.conf import settings
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.contenttypes.fields import GenericRelation
from votes.models import Vote
from comments.models import Comment


class Tag(models.Model):

    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class Question(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=256, unique=True)
    slug = models.SlugField(max_length=256)
    content = models.TextField()
    votes = GenericRelation(Vote, related_query_name='questions')
    comments = GenericRelation(Comment, related_query_name='questions')
    created_at = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('questions:detail', args=[self.slug])

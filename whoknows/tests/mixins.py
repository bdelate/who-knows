from django.contrib.auth import get_user_model
from questions.models import Question, Tag


class BaseTestMixins:

    def create_test_data():
        User = get_user_model()
        credentials = {'username': 'john', 'password': 'p@ssw0rd'}
        user = User.objects.create_user(**credentials)
        tag1 = Tag.objects.create(name='tag1')
        tag2 = Tag.objects.create(name='tag2')
        question1 = Question.objects.create(user=user, title='first question', content='content for first question')
        question1.tags.add(tag1)
        question1.comments.create(commenter=user, content='comment for first question')
        question2 = Question.objects.create(user=user, title='second question', content='content for second question')
        question2.tags.add(tag1)
        question2.tags.add(tag2)
        question2.comments.create(commenter=user, content='comment for second question')

    def create_second_user():
        User = get_user_model()
        credentials = {'username': 'sally', 'password': 'p@ssw0rd'}
        User.objects.create_user(**credentials)

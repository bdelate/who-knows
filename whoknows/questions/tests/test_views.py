from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import auth
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
        question2 = Question.objects.create(user=user, title='second question', content='content for second question')
        question2.tags.add(tag1)
        question2.tags.add(tag2)


class QuestionCreateAndDetailTest(TestCase, BaseTestMixins):

    credentials = {'username': 'john', 'password': 'p@ssw0rd'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_test_data()

    def test_logged_out_user_cannot_ask_question(self):
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)
        response = self.client.get(reverse('questions:create'), follow=True)
        login_url = reverse('account:login') + '?next=/question/'
        self.assertRedirects(response, login_url, status_code=302)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_create_question_redirects_to_detail(self):
        self.client.post(reverse('account:login'), self.credentials)
        tag = Tag.objects.first()
        response = self.client.post(reverse('questions:create'),
                                    data={'title': 'test title', 'content': 'test content', 'tags': tag.slug},
                                    follow=True)
        self.assertRedirects(response, reverse('questions:detail', args=['test-title']), status_code=302)
        self.assertTemplateUsed(response, 'questions/detail.html')

    def test_logged_out_user_can_access_question_detail(self):
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)
        response = self.client.get(reverse('questions:detail', args=['first-question']))
        self.assertEqual(response.status_code, 200)

    def test_invalid_question_detail_displays_404(self):
        response = self.client.get(reverse('questions:detail', args=['this-question-does-not-exist']))
        self.assertEqual(response.status_code, 404)

    def test_cannot_create_duplicate_title(self):
        self.client.post(reverse('account:login'), self.credentials)
        tag = Tag.objects.first()
        response = self.client.post(reverse('questions:create'),
                                    data={'title': 'first question', 'content': 'test content', 'tags': tag.slug},
                                    follow=True)
        self.assertContains(response, 'Question with this Title already exists.')

    def test_create_question_with_multiple_tags(self):
        self.client.post(reverse('account:login'), self.credentials)
        tags = Tag.objects.all()
        response = self.client.post(reverse('questions:create'),
                                    data={'title': 'test title', 'content': 'test content', 'tags': [tags[0].slug, tags[1].slug]},
                                    follow=True)
        self.assertContains(response, 'tag1')
        self.assertContains(response, 'tag2')

    def test_question_must_have_a_tag(self):
        self.client.post(reverse('account:login'), self.credentials)
        response = self.client.post(reverse('questions:create'),
                                    data={'title': 'test title', 'content': 'test content'},
                                    follow=True)
        self.assertContains(response, 'This field is required')


class QuestionHomePageTest(TestCase, BaseTestMixins):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_test_data()

    def test_question_list(self):
        response = self.client.get(reverse('questions:home'))
        self.assertContains(response, 'first question')
        self.assertContains(response, 'second question')


class TagTest(TestCase, BaseTestMixins):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_test_data()

    def test_list_tags(self):
        response = self.client.get(reverse('questions:tags_list'))
        self.assertContains(response, 'tag1')
        self.assertContains(response, 'tag2')

    def test_list_questions_for_specific_tag(self):
        response = self.client.get(reverse('questions:tagged_questions', args=['tag2']))
        self.assertNotContains(response, 'first question')
        self.assertContains(response, 'second question')

    def test_invalid_tag_displays_404(self):
        response = self.client.get(reverse('questions:tagged_questions', args=['invalid tag']))
        self.assertEqual(response.status_code, 404)

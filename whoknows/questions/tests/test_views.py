from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.contrib import auth
from questions.models import Question


class QuestionCreateAndDetailTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.credentials = {'username': 'john', 'password': 'p@ssw0rd'}
        self.user = User.objects.create_user(**self.credentials)

    def test_logged_out_user_cannot_ask_question(self):
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)
        response = self.client.get(reverse('questions:create'), follow=True)
        login_url = reverse('account:login') + '?next=/question/'
        self.assertRedirects(response, login_url, status_code=302)
        self.assertTemplateUsed(response, 'account/login.html')

    def test_create_question_redirects_to_detail(self):
        self.client.post(reverse('account:login'), self.credentials)
        response = self.client.post(reverse('questions:create'), data={'title': 'test title', 'content': 'test content'}, follow=True)
        self.assertRedirects(response, reverse('questions:detail', args=['test-title']), status_code=302)
        self.assertTemplateUsed(response, 'questions/detail.html')

    def test_logged_out_user_can_access_question_detail(self):
        self.client.post(reverse('account:login'), self.credentials)
        self.client.post(reverse('questions:create'), data={'title': 'test title', 'content': 'test content'})
        self.client.get(reverse('account:logout'))
        user = auth.get_user(self.client)
        self.assertEqual(user.is_authenticated, False)
        response = self.client.get(reverse('questions:detail', args=['test-title']))
        self.assertEqual(response.status_code, 200)

    def test_invalid_question_detail_displays_404(self):
        response = self.client.get(reverse('questions:detail', args=['this-question-does-not-exist']))
        self.assertEqual(response.status_code, 404)

    def test_cannot_create_duplicate_title(self):
        self.client.post(reverse('account:login'), self.credentials)
        self.client.post(reverse('questions:create'), data={'title': 'test title', 'content': 'test content'})
        response = self.client.post(reverse('questions:create'), data={'title': 'test title', 'content': 'test content'})
        self.assertContains(response, 'Question with this Title already exists.')


class QuestionHomePageTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.credentials = {'username': 'john', 'password': 'p@ssw0rd'}
        self.user = User.objects.create_user(**self.credentials)

    def test_no_questions(self):
        response = self.client.get(reverse('questions:home'))
        self.assertContains(response, 'No Questions yet. Ask a question')

    def test_question_list(self):
        Question.objects.create(user=self.user, title='test title1', content='test content1')
        Question.objects.create(user=self.user, title='test title2', content='test content2')
        response = self.client.get(reverse('questions:home'))
        self.assertContains(response, 'test title1')
        self.assertContains(response, 'test title2')

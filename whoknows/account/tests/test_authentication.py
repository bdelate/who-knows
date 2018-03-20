from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model


class UserAuthFlowTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.credentials = {'username': 'john', 'password': 'p@ssw0rd'}
        self.user = User.objects.create_user(**self.credentials)

    def test_create_user_redirects_to_profile(self):
        response = self.client.post(reverse('account:create'), data={'username': 'tammy', 'password1': 'p@ssword', 'password2': 'p@ssword'})
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account:profile'))

    def test_login_redirects_to_profile(self):
        response = self.client.post(reverse('account:login'), self.credentials, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, reverse('account:profile'))
        self.assertTrue(response.context['user'].is_authenticated)

    def test_logout_redirects_to_home(self):
        self.client.post(reverse('account:login'), self.credentials, follow=True)
        response = self.client.post(reverse('account:logout'))
        self.assertEqual(response.status_code, 302)
        self.assertIsNone(response.context)
        self.assertRedirects(response, reverse('questions:home'))

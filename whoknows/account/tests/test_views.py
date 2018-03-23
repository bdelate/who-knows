from django.test import TestCase
from django.urls import reverse
from account.models import Profile
from tests.mixins import BaseTestMixins


class ProfileTest(BaseTestMixins, TestCase):

    credentials = {'username': 'john', 'password': 'p@ssw0rd'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_test_data()

    def test_unauth_profile_redirects_to_login(self):
        response = self.client.get(reverse('account:profile'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('account:login'))

    def test_unauth_user_can_view_public_profile(self):
        response = self.client.get(reverse('account:profile', kwargs={'username': 'john'}))
        self.assertFalse(response.context['user'].is_authenticated)
        self.assertEquals(response.status_code, 200)
        self.assertContains(response, 'first question')
        self.assertTrue('submit' not in response)  # ensure the submit button is not present

    def test_update_profile(self):
        response = self.client.post(reverse('account:login'), self.credentials, follow=True)
        self.assertTemplateUsed(response, 'account/profile.html')
        response = self.client.post(reverse('account:profile'), data={'about': 'test about section'}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertEqual(Profile.objects.first().about, 'test about section')
        self.assertContains(response, 'test about section')

    def test_list_user_questions(self):
        response = self.client.post(reverse('account:login'), self.credentials, follow=True)
        self.assertContains(response, 'first question')
        self.assertContains(response, 'second question')


class ListUserQuestionsAndAnswersTest(TestCase, BaseTestMixins):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.create_test_data()

    def test_list_user_questions(self):
        response = self.client.get(reverse('account:user_questions', args=['john']))
        self.assertContains(response, 'first question')
        self.assertContains(response, 'second question')

    def test_list_user_answers(self):
        response = self.client.get(reverse('account:user_answers', args=['john']))
        self.assertContains(response, 'first question')
        self.assertFalse('second question' in response)

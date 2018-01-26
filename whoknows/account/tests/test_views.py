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

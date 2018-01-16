from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from account.models import Profile


class ProfileTest(TestCase):

    def setUp(self):
        User = get_user_model()
        self.credentials = {'username': 'john', 'password': 'p@ssw0rd'}
        self.user = User.objects.create_user(**self.credentials)

    def test_update_and_view_profile(self):
        response = self.client.post(reverse('account:login'), self.credentials, follow=True)
        self.assertTemplateUsed(response, 'account/profile.html')
        response = self.client.post(reverse('account:profile'), data={'about': 'test about section'}, follow=True)
        self.assertEquals(response.status_code, 200)
        self.assertEqual(Profile.objects.first().about, 'test about section')
        self.assertContains(response, 'test about section')

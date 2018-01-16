from django.test import TestCase
from django.contrib.auth import get_user_model
from account.models import Profile


class CreateAccount(TestCase):

    def test_new_user_creates_profile(self):
        User = get_user_model()
        self.credentials = {'username': 'john', 'password': 'p@ssw0rd'}
        self.user = User.objects.create_user(**self.credentials)
        profile = Profile.objects.first()
        self.assertEqual(str(profile), 'john')

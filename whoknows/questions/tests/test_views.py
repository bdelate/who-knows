from django.test import TestCase
from django.urls import reverse


class AskQuestionTest(TestCase):

    def test_uses_correct_template(self):
        url = reverse('questions:ask')
        response = self.client.get(url)
        self.assertTemplateUsed(response, 'questions/ask.html')

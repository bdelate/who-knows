from django.test import TestCase
from votes.forms import VoteForm


class VoteTest(TestCase):

    def test_valid_form(self):
        form = VoteForm(data={'object_id': '1', 'vote_type': 'question'})
        self.assertTrue(form.is_valid())
        form = VoteForm(data={'object_id': '1', 'vote_type': 'answer'})
        self.assertTrue(form.is_valid())

    def test_all_fields_required(self):
        form = VoteForm(data={'object_id': '', 'vote_type': ''})
        self.assertFalse(form.is_valid())
        object_id_error = str(form.errors['object_id'].as_data()[0].message)
        self.assertEqual(object_id_error, 'This field is required.')
        vote_type_error = str(form.errors['vote_type'].as_data()[0].message)
        self.assertEqual(vote_type_error, 'This field is required.')

    def test_valid_vote_types(self):
        form = VoteForm(data={'object_id': '1', 'vote_type': 'invalid'})
        self.assertFalse(form.is_valid())

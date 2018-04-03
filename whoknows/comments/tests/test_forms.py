from django.test import TestCase
from comments.forms import CommentForm


class CommentTest(TestCase):

    def test_valid_form(self):
        form = CommentForm(data={'object_id': '1',
                                 'comment_type': 'question',
                                 'content': 'test comment'})
        self.assertTrue(form.is_valid())
        form = CommentForm(data={'object_id': '1',
                                 'comment_type': 'answer',
                                 'content': 'test comment'})
        self.assertTrue(form.is_valid())

    def test_all_fields_required(self):
        form = CommentForm(data={'object_id': '',
                                 'comment_type': '',
                                 'content': ''})
        self.assertFalse(form.is_valid())
        object_id_error = str(form.errors['object_id']
                                  .as_data()[0]
                                  .message)
        self.assertEqual(object_id_error, 'This field is required.')
        comment_type_error = str(form.errors['comment_type']
                                     .as_data()[0]
                                     .message)
        self.assertEqual(comment_type_error, 'This field is required.')
        content_error = str(form.errors['content']
                                .as_data()[0]
                                .message)
        self.assertEqual(content_error, 'This field is required.')

    def test_valid_comment_types(self):
        form = CommentForm(data={'object_id': '1',
                                 'comment_type': 'invalid',
                                 'content': 'test comment'})
        self.assertFalse(form.is_valid())

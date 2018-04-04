from django import forms
from django.core.exceptions import ValidationError


class CommentForm(forms.Form):

    hidden_widget = forms.HiddenInput(attrs={'readonly': 'readonly'})
    object_id = forms.IntegerField(widget=hidden_widget,
                                   min_value=1)
    content = forms.CharField(widget=forms.Textarea)
    comment_type = forms.CharField(widget=hidden_widget,
                                   max_length=8)

    def clean_comment_type(self):
        if self.cleaned_data['comment_type'] in ['question', 'answer']:
            return self.cleaned_data['comment_type']
        else:
            raise ValidationError('Invalid comment type')

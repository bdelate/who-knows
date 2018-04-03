from django import forms
from django.core.exceptions import ValidationError


class VoteForm(forms.Form):

    hidden_input = forms.HiddenInput(attrs={'readonly': 'readonly'})
    object_id = forms.IntegerField(widget=hidden_input,
                                   min_value=1)
    vote_type = forms.CharField(widget=hidden_input,
                                max_length=8)

    def clean_vote_type(self):
        if self.cleaned_data['vote_type'] in ['question', 'answer', 'comment']:
            return self.cleaned_data['vote_type']
        else:
            raise ValidationError('Invalid vote type')

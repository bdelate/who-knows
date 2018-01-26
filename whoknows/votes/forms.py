from django import forms
from django.core.exceptions import ValidationError


class VoteForm(forms.Form):

    object_id = forms.IntegerField(widget=forms.HiddenInput(attrs={'readonly': 'readonly'}),
                                   min_value=1)
    vote_type = forms.CharField(widget=forms.HiddenInput(attrs={'readonly': 'readonly'}),
                                max_length=8)

    def clean_vote_type(self):
        if self.cleaned_data['vote_type'] in ['question', 'answer']:
            return self.cleaned_data['vote_type']
        else:
            raise ValidationError('Invalid vote type')

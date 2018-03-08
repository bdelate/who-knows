from django import forms
from .models import Answer


class AnswerForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['question'].widget = forms.HiddenInput()
        self.fields['user'].widget = forms.HiddenInput()

    class Meta:

        model = Answer
        fields = ['user', 'question', 'content']

from django.forms import ModelForm
from django import forms
from questions.models import (Question, Tag)


class QuestionForm(ModelForm):

    class Meta:
        model = Question
        fields = ['title', 'content']


class TagForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tags'] = forms.MultipleChoiceField(choices=Tag.objects.values_list())

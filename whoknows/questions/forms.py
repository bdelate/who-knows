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
        choices = Tag.objects.values_list('slug', 'name')
        widget = forms.SelectMultiple(attrs={'class': 'input select',
                                             'size': 8})
        self.fields['tags'] = forms.MultipleChoiceField(choices=choices,
                                                        widget=widget)


class SearchForm(forms.Form):

    search = forms.CharField()

from django.urls import path
from .views import (HomePage, QuestionCreate, QuestionDetail, TagsList,
                    TaggedQuestionList, QuestionSearch)

app_name = 'questions'

urlpatterns = [
    path('',
         HomePage.as_view(),
         name='home'),
    path('question/',
         QuestionCreate.as_view(),
         name='create'),
    path('question/search/',
         QuestionSearch.as_view(),
         name='search'),
    path('question/<str:slug>/',
         QuestionDetail.as_view(),
         name='detail'),
    path('tags/',
         TagsList.as_view(),
         name='tags_list'),
    path('tags/<str:slug>',
         TaggedQuestionList.as_view(),
         name='tagged_questions'),
]

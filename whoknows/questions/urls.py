from django.urls import path
from .views import HomePage, QuestionCreate, QuestionDetail

app_name = 'questions'

urlpatterns = [
    path('', HomePage.as_view(), name='home'),
    path('question/', QuestionCreate.as_view(), name='create'),
    path('question/<str:slug>/', QuestionDetail.as_view(), name='detail'),
]

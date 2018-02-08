from django.urls import path
from .views import CreateAnswer

app_name = 'answers'

urlpatterns = [
    path('create-answer', CreateAnswer.as_view(), name='create_answer'),
]

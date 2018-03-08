from django.urls import path
from .views import CreateAnswer, ToggleAccept

app_name = 'answers'

urlpatterns = [
    path('create-answer', CreateAnswer.as_view(), name='create_answer'),
    path('toggle-accept', ToggleAccept.as_view(), name='toggle_accept'),
]

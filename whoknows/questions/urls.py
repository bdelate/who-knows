from django.urls import path
from .views import HomePage, Ask

app_name = 'questions'

urlpatterns = [
    path('', HomePage.as_view()),
    path('ask/', Ask.as_view(), name='ask'),
]

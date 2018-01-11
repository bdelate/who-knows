from django.urls import path
from .views import Ask

app_name = 'questions'

urlpatterns = [
    path('ask/', Ask.as_view(), name='ask'),
]

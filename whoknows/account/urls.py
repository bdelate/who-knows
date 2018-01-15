from django.urls import path
from .views import Create

app_name = 'account'

urlpatterns = [
    path('create/', Create.as_view(), name='create'),
]

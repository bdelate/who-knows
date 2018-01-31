from django.urls import path
from .views import CreateComment

app_name = 'comments'

urlpatterns = [
    path('create-comment', CreateComment.as_view(), name='create_comment'),
]

from django.urls import path
from .views import UpVote

app_name = 'votes'

urlpatterns = [
    path('up-vote', UpVote.as_view(), name='up_vote'),
]

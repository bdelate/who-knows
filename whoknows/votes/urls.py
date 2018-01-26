from django.urls import path
from .views import UpVote, RemoveVote

app_name = 'votes'

urlpatterns = [
    path('up-vote', UpVote.as_view(), name='up_vote'),
    path('remove-vote', RemoveVote.as_view(), name='remove_vote'),
]

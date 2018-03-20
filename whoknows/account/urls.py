from django.urls import path
from .views import UserQuestionList, UserAnswerList, AccountCreate, Profile
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('', Profile.as_view(), name='profile'),  # used to access the current users profile page
    path('questions', UserQuestionList.as_view(), name='user_questions'),
    path('answers', UserAnswerList.as_view(), name='user_answers'),
    path('create/', AccountCreate.as_view(), name='create'),
    path("login/", auth_views.LoginView.as_view(template_name="account/login.html"), name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name='logout'),
    path('<str:username>/', Profile.as_view(), name='profile'),  # used to access another users profile page
]

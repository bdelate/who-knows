from django.urls import path
from .views import Create, ProfileDetail
from django.contrib.auth import views as auth_views

app_name = 'account'

urlpatterns = [
    path('', ProfileDetail.as_view(), name='profile'),
    path('create/', Create.as_view(), name='create'),
    path("login/", auth_views.LoginView.as_view(template_name="account/login.html"), name='login'),
    path("logout/", auth_views.LogoutView.as_view(), name='logout'),
]

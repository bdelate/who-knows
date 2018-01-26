from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import View, UpdateView, ListView
from django.contrib.auth import login, authenticate, get_user
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from votes.models import Vote
from questions.models import Question


class AccountCreate(View):

    def get(self, request):
        form = UserCreationForm()
        return render(request, 'account/create.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect(reverse('account:profile'))
        return render(request, 'account/create.html', {'form': form})


class ProfileUpdate(LoginRequiredMixin, UpdateView):

    model = Profile
    template_name = 'account/profile.html'
    fields = ['about']
    success_url = '/account/'

    def get_object(self, queryset=None):
        current_user = get_user(self.request)
        return current_user.profile

    def get_context_data(self, **kwargs):
        kwargs['question_votes_received'] = Vote.objects.filter(questions__user=self.request.user).count()
        kwargs['latest_questions'] = Question.objects.filter(user=self.request.user).order_by('-created_at')[:5]
        return super().get_context_data(**kwargs)


class UserQuestionList(LoginRequiredMixin, ListView):

    template_name = 'questions/index.html'
    paginate_by = 5

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user).order_by('-created_at')

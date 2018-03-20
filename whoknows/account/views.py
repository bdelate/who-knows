from django.shortcuts import redirect, get_object_or_404
from django.views.generic import UpdateView, ListView, CreateView
from django.contrib.auth import login, get_user, get_user_model
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from votes.models import Vote
from questions.models import Question
from answers.models import Answer


class AccountCreate(CreateView):

    model = settings.AUTH_USER_MODEL
    form_class = UserCreationForm
    template_name = 'account/create.html'

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('account:profile')


class Profile(UpdateView):

    model = Profile
    template_name = 'account/profile.html'
    fields = ['about']
    success_url = '/account/'

    def dispatch(self, request, *args, **kwargs):
        """
        If the user is trying to access 'account:profile' directly, the kwargs['username'] will not be present.
        If that user is not logged in, redirect to 'account:login'. If the user is logged in, call super()
        """
        try:
            self.kwargs['username']
        except KeyError:
            if not self.request.user.is_authenticated:
                return redirect('account:login')
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        try:
            profile_user = self.kwargs['username']
        except KeyError:
            profile_user = get_user(self.request)
        else:
            profile_user = get_object_or_404(get_user_model(), username=profile_user)
        self.kwargs['profile_user'] = profile_user
        return profile_user.profile

    def get_context_data(self, **kwargs):
        kwargs['question_votes_received'] = Vote.objects.filter(questions__user=self.kwargs['profile_user']).count()
        kwargs['comment_votes_received'] = Vote.objects.filter(comments__commenter=self.kwargs['profile_user']).count()
        kwargs['answer_votes_received'] = Vote.objects.filter(answers__user=self.kwargs['profile_user']).count()
        kwargs['latest_questions'] = Question.objects.filter(user=self.kwargs['profile_user']).order_by('-created_at')[:5]
        kwargs['latest_answers'] = Answer.objects.prefetch_related('question').filter(user=self.kwargs['profile_user']).order_by('-created_at')[:5]
        kwargs['profile_user'] = self.kwargs['profile_user']
        return super().get_context_data(**kwargs)


class UserQuestionList(LoginRequiredMixin, ListView):

    template_name = 'questions/index.html'
    paginate_by = 5

    def get_queryset(self):
        return Question.objects.filter(user=self.request.user).order_by('-created_at')


class UserAnswerList(LoginRequiredMixin, ListView):

    template_name = 'questions/index.html'
    paginate_by = 5

    def get_queryset(self):
        return Question.objects.prefetch_related('answer_set').filter(answer__user=self.request.user).order_by('-created_at')

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView
from .forms import AnswerForm
from django.http import JsonResponse
from .models import Answer


class CreateAnswer(LoginRequiredMixin, CreateView):

    model = Answer
    form_class = AnswerForm

    def form_valid(self, form):
        already_answered = Answer.objects.filter(question=form.cleaned_data['question'],
                                                 user=self.request.user).exists()
        if already_answered:
            return JsonResponse({'response': 'You have already answered this question', 'type': 'answer'}, status=400)
        form.save()
        return JsonResponse({'response': 'Answer created', 'type': 'answer'})

    def form_invalid(self, form):
        return JsonResponse({'response': 'Invalid Answer', 'type': 'answer'}, status=400)

    def get_form(self, form_class=None):
        return self.form_class(self.request.POST, prefix='answer')

    def handle_no_permission(self):
        return JsonResponse({'response': 'login required', 'type': 'answer'}, status=400)

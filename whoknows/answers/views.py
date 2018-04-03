from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, View
from .forms import AnswerForm
from django.http import JsonResponse
from .models import Answer
from django.core.exceptions import ObjectDoesNotExist


class CreateAnswer(LoginRequiredMixin, CreateView):

    model = Answer
    form_class = AnswerForm

    def form_valid(self, form):
        question = form.cleaned_data['question']
        already_answered = (Answer.objects
                                  .filter(question=question,
                                          user=self.request.user)
                                  .exists())
        if already_answered:
            return JsonResponse(
                {'response': 'You have already answered this question',
                 'type': 'answer'},
                status=400)
        form.save()
        return JsonResponse({'response': 'Answer created', 'type': 'answer'})

    def form_invalid(self, form):
        return JsonResponse({'response': 'Invalid Answer', 'type': 'answer'},
                            status=400)

    def get_form(self, form_class=None):
        return self.form_class(self.request.POST)

    def handle_no_permission(self):
        return JsonResponse(
            {'response': 'Please login or signup before doing this.',
             'type': 'answer'},
            status=400)


class ToggleAccept(LoginRequiredMixin, View):
    """
    1: Get answer if valid id is provided, else return error
    2: Unaccept all answers linked to this question
    3: Toggle the accept value of this answer and return confirmation
    """

    def post(self, request, *args, **kwargs):
        try:
            answer = (Answer.objects
                            .select_related('question', 'question__user')
                            .get(id=self.request.POST.get('answer_id')))
        except ObjectDoesNotExist:
            return JsonResponse({'response': 'Invalid answer'}, status=400)
        else:
            if self.request.user == answer.question.user:
                (Answer.objects
                       .filter(question=answer.question)
                       .update(accepted=False))
                answer.accepted = not answer.accepted
                answer.save()
                return JsonResponse({'response': 'Accepted answer toggled'})
            return JsonResponse({'response': 'Invalid user', 'type': 'answer'},
                                status=400)

    def handle_no_permission(self):
        return JsonResponse(
            {'response': 'Please login or signup before doing this.',
             'type': 'answer'},
            status=400)

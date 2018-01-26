from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import View
from questions.models import Question
from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from .forms import VoteForm


class UpVote(View):

    def post(self, request, *args, **kwargs):
        vote_form = VoteForm(request.POST)
        if vote_form.is_valid():
            object_id = vote_form.cleaned_data['object_id']
            if vote_form.cleaned_data['vote_type'] == 'question':
                try:
                    object_instance = Question.objects.get(id=object_id)
                except ObjectDoesNotExist:
                    return JsonResponse({'response': 'Invalid Question'}, status=400)
            if self.request.user.is_authenticated:
                if object_instance.user != self.request.user:
                    try:
                        object_instance.votes.create(voter=self.request.user)
                    except IntegrityError:
                        message = 'You have already voted for this {}'.format(vote_form.cleaned_data['vote_type'])
                        return JsonResponse({'response': message}, status=400)
                    else:
                        return JsonResponse({'response': 'Thanks for your vote'})
                else:
                    message = 'You cannot vote for your own {}'.format(vote_form.cleaned_data['vote_type'])
                    return JsonResponse({'response': message}, status=400)
            else:
                url = reverse('account:login')
                url = '{}?next={}'.format(url, reverse('questions:detail', args=[object_instance.slug]))
                url = 'You have to be logged in to vote. Login/Signup <a href="{}">here</a>'.format(url)
                return JsonResponse({'response': url})
        else:
            return JsonResponse({'response': 'Invalid Vote'}, status=400)


class RemoveVote(View):

    def post(self, request, *args, **kwargs):
        vote_form = VoteForm(request.POST)
        if vote_form.is_valid():
            object_id = vote_form.cleaned_data['object_id']
            if vote_form.cleaned_data['vote_type'] == 'question':
                try:
                    object_instance = Question.objects.get(id=object_id)
                except ObjectDoesNotExist:
                    return JsonResponse({'response': 'Invalid Question'}, status=400)
            try:
                vote = object_instance.votes.get(voter=request.user)
            except ObjectDoesNotExist:
                return JsonResponse({'response': 'Invalid Vote'}, status=400)
            else:
                vote.delete()
                return JsonResponse({'response': 'Your vote has been removed'})
        else:
            return JsonResponse({'response': 'Invalid Vote'}, status=400)

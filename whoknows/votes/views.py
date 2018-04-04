from django.http import JsonResponse
from django.views.generic import View
from questions.models import Question
from comments.models import Comment
from answers.models import Answer
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
                    return JsonResponse({'response': 'Invalid question'},
                                        status=400)
                else:
                    creator = object_instance.user
            elif vote_form.cleaned_data['vote_type'] == 'comment':
                try:
                    object_instance = Comment.objects.get(id=object_id)
                except ObjectDoesNotExist:
                    return JsonResponse({'response': 'Invalid comment'},
                                        status=400)
                else:
                    creator = object_instance.commenter
            elif vote_form.cleaned_data['vote_type'] == 'answer':
                try:
                    object_instance = Answer.objects.get(id=object_id)
                except ObjectDoesNotExist:
                    return JsonResponse({'response': 'Invalid answer'},
                                        status=400)
                else:
                    creator = object_instance.user
            if self.request.user.is_authenticated:
                if creator != self.request.user:
                    try:
                        object_instance.votes.create(voter=self.request.user)
                    except IntegrityError:
                        message = 'You have already voted for this {}'.format(
                            vote_form.cleaned_data['vote_type'])
                        return JsonResponse({'response': message}, status=400)
                    else:
                        return JsonResponse(
                            {'response': 'Thanks for your vote'})
                else:
                    message = 'You cannot vote for your own {}'.format(
                        vote_form.cleaned_data['vote_type'])
                    return JsonResponse({'response': message}, status=400)
            else:
                response = 'Please login or signup before doing this.'
                return JsonResponse({'response': response})
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
                    return JsonResponse({'response': 'Invalid question'},
                                        status=400)
            elif vote_form.cleaned_data['vote_type'] == 'comment':
                try:
                    object_instance = Comment.objects.get(id=object_id)
                except ObjectDoesNotExist:
                    return JsonResponse({'response': 'Invalid comment'},
                                        status=400)
            elif vote_form.cleaned_data['vote_type'] == 'answer':
                try:
                    object_instance = Answer.objects.get(id=object_id)
                except ObjectDoesNotExist:
                    return JsonResponse({'response': 'Invalid answer'},
                                        status=400)
            try:
                vote = object_instance.votes.get(voter=request.user)
            except ObjectDoesNotExist:
                return JsonResponse({'response': 'Invalid Vote'},
                                    status=400)
            else:
                vote.delete()
                return JsonResponse({'response': 'Your vote has been removed'})
        else:
            return JsonResponse({'response': 'Invalid Vote'}, status=400)

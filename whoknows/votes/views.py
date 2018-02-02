from django.urls import reverse
from django.http import JsonResponse
from django.views.generic import View
from questions.models import Question
from comments.models import Comment
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
                    return JsonResponse({'response': 'Invalid question', 'type': 'vote'}, status=400)
                else:
                    creator = object_instance.user
                    slug = object_instance.slug
            elif vote_form.cleaned_data['vote_type'] == 'comment':
                try:
                    object_instance = Comment.objects.get(id=object_id)
                except ObjectDoesNotExist:
                    return JsonResponse({'response': 'Invalid comment', 'type': 'vote'}, status=400)
                else:
                    creator = object_instance.commenter
                    slug = object_instance.content_object.slug  # get the slug of the question
            if self.request.user.is_authenticated:
                if creator != self.request.user:
                    try:
                        object_instance.votes.create(voter=self.request.user)
                    except IntegrityError:
                        message = 'You have already voted for this {}'.format(vote_form.cleaned_data['vote_type'])
                        return JsonResponse({'response': message, 'type': 'vote'}, status=400)
                    else:
                        return JsonResponse({'response': 'Thanks for your vote', 'type': 'vote'})
                else:
                    message = 'You cannot vote for your own {}'.format(vote_form.cleaned_data['vote_type'])
                    return JsonResponse({'response': message, 'type': 'vote'}, status=400)
            else:
                url = reverse('account:login')
                url = '{}?next={}'.format(url, reverse('questions:detail', args=[slug]))
                url = 'You have to be logged in to vote. Login/Signup <a href="{}">here</a>'.format(url)
                return JsonResponse({'response': url, 'type': 'vote'})
        else:
            return JsonResponse({'response': 'Invalid Vote', 'type': 'vote'}, status=400)


class RemoveVote(View):

    def post(self, request, *args, **kwargs):
        vote_form = VoteForm(request.POST)
        if vote_form.is_valid():
            object_id = vote_form.cleaned_data['object_id']
            if vote_form.cleaned_data['vote_type'] == 'question':
                try:
                    object_instance = Question.objects.get(id=object_id)
                except ObjectDoesNotExist:
                    return JsonResponse({'response': 'Invalid question', 'type': 'vote'}, status=400)
            elif vote_form.cleaned_data['vote_type'] == 'comment':
                try:
                    object_instance = Comment.objects.get(id=object_id)
                except ObjectDoesNotExist:
                    return JsonResponse({'response': 'Invalid comment', 'type': 'vote'}, status=400)
            try:
                vote = object_instance.votes.get(voter=request.user)
            except ObjectDoesNotExist:
                return JsonResponse({'response': 'Invalid Vote', 'type': 'vote'}, status=400)
            else:
                vote.delete()
                return JsonResponse({'response': 'Your vote has been removed', 'type': 'vote'})
        else:
            return JsonResponse({'response': 'Invalid Vote', 'type': 'vote'}, status=400)

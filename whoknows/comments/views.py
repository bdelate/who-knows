from django.views.generic import View
from comments.forms import CommentForm
from django.http import JsonResponse
from questions.models import Question
from django.core.exceptions import ObjectDoesNotExist
from django.urls import reverse


class CreateComment(View):

    def post(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                object_id = comment_form.cleaned_data['object_id']
                if comment_form.cleaned_data['comment_type'] == 'question':
                    try:
                        object_instance = Question.objects.get(id=object_id)
                    except ObjectDoesNotExist:
                        return JsonResponse({'response': 'Invalid Question', 'type': 'comment'}, status=400)
                object_instance.comments.create(commenter=self.request.user,
                                                content=comment_form.cleaned_data['content'])
                return JsonResponse({'response': 'Comment created', 'type': 'comment'})
            else:
                return JsonResponse({'response': 'Invalid Comment', 'type': 'comment'}, status=400)
        else:
            url = reverse('account:login')
            url = '{}?next={}'.format(url, reverse('questions:detail', args=[object_instance.slug]))
            url = 'You have to be logged in to comment. Login/Signup <a href="{}">here</a>'.format(url)
            return JsonResponse({'response': url, 'type': 'comment'})

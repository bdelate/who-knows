from django.views.generic import View
from comments.forms import CommentForm
from django.http import JsonResponse
from questions.models import Question
from answers.models import Answer
from django.core.exceptions import ObjectDoesNotExist


class CreateComment(View):

    def post(self, request, *args, **kwargs):
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            object_id = comment_form.cleaned_data['object_id']
            if comment_form.cleaned_data['comment_type'] == 'question':
                try:
                    object_instance = Question.objects.get(id=object_id)
                except ObjectDoesNotExist:
                    return JsonResponse({'response': 'Invalid Question'},
                                        status=400)
            if comment_form.cleaned_data['comment_type'] == 'answer':
                try:
                    object_instance = Answer.objects.get(id=object_id)
                except ObjectDoesNotExist:
                    return JsonResponse({'response': 'Invalid Answer'},
                                        status=400)
            if self.request.user.is_authenticated:
                content = comment_form.cleaned_data['content']
                object_instance.comments.create(commenter=self.request.user,
                                                content=content)
                return JsonResponse({'response': 'Comment created'})
            else:
                response = 'Please login or signup before doing this.'
                return JsonResponse({'response': response}, status=400)
        else:
            return JsonResponse({'response': 'Invalid Comment'}, status=400)

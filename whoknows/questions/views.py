from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, ListView
from .models import Question, Tag
from .forms import QuestionForm, TagForm
from django.shortcuts import redirect, render
from votes.forms import VoteForm
from comments.forms import CommentForm


class HomePage(ListView):

    model = Question
    queryset = Question.objects.order_by('-created_at')[:30]
    template_name = 'questions/index.html'
    paginate_by = 5


class QuestionCreate(LoginRequiredMixin, TemplateView):

    template_name = 'questions/create.html'

    def get_context_data(self, **kwargs):
        return {'question_form': QuestionForm(),
                'tag_form': TagForm()}

    def post(self, request, *args, **kwargs):
        question_form = QuestionForm(request.POST)
        tag_form = TagForm(request.POST)
        if question_form.is_valid() and tag_form.is_valid():
            question_form.instance.user = self.request.user
            question = question_form.save()
            tags = tag_form.cleaned_data['tags']
            for tag_slug in tags:
                obj, created = Tag.objects.get_or_create(slug=tag_slug)
                question.tags.add(obj)
            return redirect(question)
        return render(request,
                      self.template_name,
                      {'question_form': question_form,
                       'tag_form': tag_form})


class QuestionDetail(DetailView):

    model = Question
    template_name = 'questions/detail.html'

    def get(self, request, *args, **kwargs):
        question = get_object_or_404(Question, slug=kwargs['slug'])
        if self.request.user.is_authenticated:
            user = self.request.user
        else:  # anonymouse users cannot be used with filter(), therefore assign None if user is not logged in
            user = None
        context = {'vote_form': VoteForm(),
                   'comment_form': CommentForm(initial={'object_id': question.id, 'comment_type': 'question'}),
                   'question': {'object': question, 'voted': question.votes.filter(voter=user).exists(),
                                'comments': []}}
        for comment in question.comments.all():
            comment_detail = {'object': comment, 'voted': comment.votes.filter(voter=user).exists()}
            context['question']['comments'].append(comment_detail)
        return self.render_to_response(context)


class TagsList(ListView):

    model = Tag
    template_name = 'questions/tags_list.html'


class TaggedQuestionList(ListView):

    template_name = 'questions/index.html'
    paginate_by = 5

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Question.objects.filter(tags=tag).order_by('-created_at')

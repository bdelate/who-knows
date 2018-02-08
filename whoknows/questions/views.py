from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, ListView
from comments.models import Comment
from answers.models import Answer
from .models import Question, Tag
from django.db.models import Count
from django.db.models import Exists, OuterRef
from .forms import QuestionForm, TagForm
from answers.forms import AnswerForm
from django.shortcuts import redirect, render
from votes.forms import VoteForm


class HomePage(ListView):

    model = Question
    queryset = Question.objects.select_related('user').order_by('-created_at')[:30]
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
        # anonymous users cannot be used in fitler clause, therefore assign None
        user = self.request.user if self.request.user.is_authenticated else None
        voted_for_question = Question.objects.filter(votes__voter=user, votes__object_id=OuterRef('pk'))
        question_query = Question.objects.select_related('user').annotate(num_votes=Count('votes'),
                                                                          voted=Exists(voted_for_question))
        question = get_object_or_404(question_query, slug=kwargs['slug'])
        context = {'vote_form': VoteForm(),
                   'question': {'question': question, 'comments': []}}

        voted_for_comment = Comment.objects.filter(votes__voter=user, votes__object_id=OuterRef('pk'))
        comment_query = question.comments.prefetch_related('commenter').annotate(num_votes=Count('votes'),
                                                                                 voted=Exists(voted_for_comment))
        for comment in comment_query:
            context['question']['comments'].append(comment)

        voted_for_answer = Answer.objects.filter(votes__voter=user, votes__object_id=OuterRef('pk'))
        answers = Answer.objects.prefetch_related('user').filter(question=question).annotate(num_votes=Count('votes'),
                                                                                             voted=Exists(voted_for_answer))
        context['answers'] = answers
        context['answer_form'] = AnswerForm(initial={'question': question, 'user': self.request.user}, prefix='answer')

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

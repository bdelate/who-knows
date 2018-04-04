from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, ListView
from comments.models import Comment
from answers.models import Answer
from .models import Question, Tag
from django.db.models import Count, Exists, OuterRef, Q
from .forms import QuestionForm, TagForm, SearchForm
from answers.forms import AnswerForm
from django.shortcuts import redirect, render
from votes.forms import VoteForm


class HomePage(ListView):

    model = Question
    template_name = 'questions/index.html'
    paginate_by = 5
    ordering = '-created_at'

    def post(self, request, *args, **kwargs):
        # pagination is not used when filtering by category
        self.paginate_by = None
        category = self.request.POST.get('category', 'All questions')
        if category == 'No answers':
            self.object_list = (Question.objects
                                        .prefetch_related('votes',
                                                          'tags',
                                                          'answer_set')
                                        .select_related('user')
                                        .annotate(answer_count=Count('answer'))
                                        .filter(answer_count=0)
                                        .order_by('-created_at')[:30])
        elif category == 'No accepted answers':
            accepted_answers = Answer.objects.filter(accepted=True)
            self.object_list = (Question.objects
                                        .prefetch_related('votes',
                                                          'tags',
                                                          'answer_set')
                                        .select_related('user')
                                        .exclude(answer__in=accepted_answers)
                                        .order_by('-created_at')[:30])
        elif category == 'Accepted answers':
            accepted_answers = Answer.objects.filter(accepted=True)
            self.object_list = (Question.objects
                                        .prefetch_related('votes',
                                                          'tags',
                                                          'answer_set')
                                        .select_related('user')
                                        .filter(answer__in=accepted_answers)
                                        .order_by('-created_at')[:30])
        else:
            self.paginate_by = 5
            self.object_list = (Question.objects
                                        .prefetch_related('votes', 'tags',
                                                          'answer_set')
                                        .select_related('user')
                                        .order_by('-created_at')[:30])

        context = super().get_context_data(object_list=self.object_list,
                                           category=category,
                                           **kwargs)
        return super().render_to_response(context=context, **kwargs)


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
        # anonymous users cannot be used in fitler clause,
        # therefore assign None
        user = self.request.user if self.request.user.is_authenticated else None
        voted_for_question = (Question.objects
                                      .filter(votes__voter=user,
                                              votes__object_id=OuterRef('pk')))
        question_query = (Question.objects
                                  .select_related('user')
                                  .annotate(num_votes=Count('votes'),
                                            voted=Exists(voted_for_question)))
        question = get_object_or_404(question_query, slug=kwargs['slug'])
        question.num_views += 1
        question.save()

        answer_form_initial = {'question': question, 'user': self.request.user}
        context = {'vote_form': VoteForm(),
                   'answer_form': AnswerForm(initial=answer_form_initial),
                   'question': {'question': question, 'comments': []},
                   'answers': []}

        # get the comments for the question
        voted_for_comment = (Comment.objects
                                    .filter(votes__voter=user,
                                            votes__object_id=OuterRef('pk')))
        comment_query = (question.comments
                                 .prefetch_related('commenter')
                                 .annotate(num_votes=Count('votes'),
                                           voted=Exists(voted_for_comment))
                                 .order_by('created_at'))
        for comment in comment_query:
            context['question']['comments'].append(comment)

        # get the answers for the question
        voted_for_answer = (Answer.objects
                                  .filter(votes__voter=user,
                                          votes__object_id=OuterRef('pk')))
        answers = (Answer.objects
                         .prefetch_related('user')
                         .filter(question=question)
                         .annotate(num_votes=Count('votes'),
                                   voted=Exists(voted_for_answer))
                         .order_by('-accepted', '-num_votes', '-created_at'))
        for answer in answers:
            comments = []
            # get the comments for each answer
            comment_query = (answer.comments
                                   .prefetch_related('commenter')
                                   .annotate(num_votes=Count('votes'),
                                             voted=Exists(voted_for_comment))
                                   .order_by('created_at'))
            for comment in comment_query:
                comments.append(comment)
            # append this answer along with all its comments to context
            context['answers'].append({'answer': answer, 'comments': comments})

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

    def get_context_data(self, **kwargs):
        tag = self.kwargs['slug'].replace('-', ' ')
        kwargs['tagged_by'] = tag
        return super().get_context_data(**kwargs)


class QuestionSearch(ListView):

    template_name = 'questions/index.html'
    form_class = SearchForm

    def post(self, request, *args, **kwargs):
        search_form = self.form_class(self.request.POST)
        if search_form.is_valid():
            query_string = search_form.cleaned_data['search']
            filter = (Q(title__icontains=query_string)
                      | Q(content__icontains=query_string))
            self.queryset = (Question.objects
                                     .filter(filter)
                                     .order_by('-created_at'))
            self.extra_context = {'query_string': query_string}
        return self.get(request, *args, **kwargs)

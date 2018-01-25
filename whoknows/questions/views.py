from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, ListView
from .models import Question, Tag
from .forms import QuestionForm, TagForm
from django.shortcuts import redirect, render
from votes.forms import VoteForm


class HomePage(ListView):

    model = Question
    queryset = Question.objects.order_by('-created_at')[:30]
    template_name = 'questions/index.html'
    paginate_by = 3


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
        self.object = get_object_or_404(Question, slug=kwargs['slug'])
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

    def get_context_data(self, **kwargs):
        super().get_context_data()
        kwargs['vote_form'] = VoteForm(initial={'object_id': kwargs['object'].id, 'vote_type': 'question'})
        kwargs['num_votes'] = kwargs['object'].votes.count()
        if self.request.user.is_authenticated:
            kwargs['already_voted'] = kwargs['object'].votes.filter(user=self.request.user).count() == 1
        return kwargs


class TagsList(ListView):

    model = Tag
    template_name = 'questions/tags_list.html'


class TaggedQuestionList(ListView):

    template_name = 'questions/index.html'

    def get_queryset(self):
        tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return Question.objects.filter(tags=tag)

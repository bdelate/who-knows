from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, ListView
from .models import Question, Tag
from .forms import QuestionForm, TagForm
from django.shortcuts import redirect, render


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
            for tag_id in tags:
                obj, created = Tag.objects.get_or_create(id=tag_id)
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

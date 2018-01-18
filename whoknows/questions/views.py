from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, DetailView, ListView
from .models import Question


class HomePage(ListView):

    model = Question
    queryset = Question.objects.order_by('-created_at')[:30]
    template_name = 'questions/index.html'
    paginate_by = 3


class QuestionCreate(LoginRequiredMixin, CreateView):

    model = Question
    template_name = 'questions/create.html'
    fields = ['title', 'content']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class QuestionDetail(DetailView):

    model = Question
    template_name = 'questions/detail.html'

    def get(self, request, *args, **kwargs):
        self.object = get_object_or_404(Question, slug=kwargs['slug'])
        context = self.get_context_data(object=self.object)
        return self.render_to_response(context)

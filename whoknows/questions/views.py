from django.shortcuts import render
from django.views.generic import View, TemplateView


class HomePage(TemplateView):

    template_name = 'questions/index.html'


class Ask(View):

    def get(self, request):
        return render(request,
                      'questions/ask.html',
                      {})

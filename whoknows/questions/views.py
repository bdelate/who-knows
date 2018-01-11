from django.shortcuts import render
from django.views.generic import View


class Ask(View):

    def get(self, request):
        return render(request,
                      'questions/ask.html',
                      {})

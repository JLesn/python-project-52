from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.utils.translation import gettext_lazy as _, get_language

class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')

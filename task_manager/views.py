from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.utils.translation import gettext_lazy as _
from django.urls import reverse_lazy
from django.contrib import messages
from task_manager.users.forms import CustomAuthenticationForm
from django.views import View
from django.shortcuts import redirect
from django.contrib.auth import logout


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request, *args, **kwargs):
        return render(request, 'index.html')


class UserLoginView(LoginView):
    template_name = 'form.html'
    form_class = CustomAuthenticationForm
    next_page = reverse_lazy('index')
    extra_context = {'title': _('Entry'), 'button': _('Log in')}


class UserLogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        messages.success(request, _('You have successfully logged out!'))
        return redirect(reverse_lazy('index'))
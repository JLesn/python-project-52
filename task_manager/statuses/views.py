from django.shortcuts import render
from django.views.generic import ListView, CreateView
from .models import Status
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import StatusForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

class StatusesList(ListView):
    model = Status
    template_name = 'statuses/statuses_list.html'
    context_object_name = 'statuses'

    def get_queryset(self):
        return Status.objects.all()
    

class StatusCreationView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
     model = Status
     form_class = StatusForm
     success_url = reverse_lazy('statuses')
     template_name = 'form.html'
     success_message = _("Status successfully created")
     extra_context = {"title": _("Create status"), "button": _("Create")}







# class SignUpView(SuccessMessageMixin, CreateView):
#     model = MyUser
#     form_class = CustomUserCreationForm
#     success_url = reverse_lazy('login')
#     template_name = 'form.html'
#     extra_context = {'title': _('Registration'), 'button': _('Register')}
#     success_message = _('Registration completed successfully!')




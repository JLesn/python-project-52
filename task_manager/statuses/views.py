from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Status
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import LoginRequiredMessageMixin
from .forms import StatusForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

class StatusesList(ListView):
    model = Status
    template_name = 'statuses/statuses_list.html'
    context_object_name = 'statuses'

    def get_queryset(self):
        return Status.objects.all()
    

class StatusCreationView(LoginRequiredMessageMixin, SuccessMessageMixin, CreateView):
     model = Status
     form_class = StatusForm
     success_url = reverse_lazy('statuses')
     template_name = 'form.html'
     success_message = _("Status successfully created")
     extra_context = {"title": _("Create status"), "button": _("Create")}


class StatusUpdateView(LoginRequiredMessageMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'form.html'
    success_url = reverse_lazy('statuses')
    extra_context = {'title': _('Update status'), 'button': _('Update')}
    success_message = _('Status updated successfully!')

class StatusDeleteView(LoginRequiredMessageMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'delete_form.html'
    success_url = reverse_lazy('statuses')
    extra_context = {'header': _('Delete status')}
    success_message = _('Status deleted successfully!')
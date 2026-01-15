from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Label
from django.contrib.messages.views import SuccessMessageMixin
from task_manager.mixins import LoginRequiredMessageMixin
from .forms import LabelForm
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.db.models import ProtectedError
from django.shortcuts import redirect
from django.contrib import messages

class LabelsList(ListView):
    model = Label
    template_name = 'labels/labels_list.html'
    context_object_name = 'labels'

    def get_queryset(self):
        return Label.objects.all()
    


class LabelCreationView(LoginRequiredMessageMixin, SuccessMessageMixin, CreateView):
     model = Label
     form_class = LabelForm
     success_url = reverse_lazy('labels')
     template_name = 'form.html'
     success_message = _("Status successfully created")
     extra_context = {"title": _("Create label"), "button": _("Create")}




class LabelUpdateView(LoginRequiredMessageMixin, SuccessMessageMixin, UpdateView):
    model = Label
    form_class = LabelForm
    template_name = 'form.html'
    success_url = reverse_lazy('labels')
    extra_context = {'title': _('Update label'), 'button': _('Update')}
    success_message = _('Label updated successfully!')



class LabelDeleteView(LoginRequiredMessageMixin, SuccessMessageMixin, DeleteView):
    model = Label
    template_name = 'delete_form.html'
    success_url = reverse_lazy('labels')
    extra_context = {'header': _('Delete label')}
    success_message = _('Label deleted successfully!')

    def form_valid(self, form):
        label = self.get_object()
        if label.tasks.exists():
            messages.error(self.request, _("Cannot delete label because it is in use."))
            return redirect('labels')
        return super().form_valid(form)

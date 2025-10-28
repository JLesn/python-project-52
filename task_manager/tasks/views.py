from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Task
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import TaskFilterForm, TaskForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import ProtectedError


class TasksListView(LoginRequiredMixin, ListView):
    model = Task
    template_name = 'tasks/tasks_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        queryset = Task.objects.all()
        form = TaskFilterForm(self.request.GET)
        if form.is_valid():
            if form.cleaned_data.get('status'):
                queryset = queryset.filter(status=form.cleaned_data['status'])
            if form.cleaned_data.get('executor'):
                queryset = queryset.filter(executor=form.cleaned_data['executor'])
            if form.cleaned_data.get('label'):
                queryset = queryset.filter(labels=form.cleaned_data['label'])
            if form.cleaned_data.get('own_tasks'):
                queryset = queryset.filter(author=self.request.user)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TaskFilterForm(self.request.GET)
        return context
    


class TaskCreationView(LoginRequiredMixin, SuccessMessageMixin, CreateView):
     model = Task
     form_class = TaskForm
     success_url = reverse_lazy('tasks')
     template_name = 'form.html'
     success_message = _("Task successfully created")
     extra_context = {"title": _("Create task"), "button": _("Create")}

     def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
     


class TaskUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'form.html'
    success_url = reverse_lazy('tasks')
    extra_context = {'title': _('Update task'), 'button': _('Update')}
    success_message = _('Task updated successfully!')




class TaskDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'delete_form.html'
    success_url = reverse_lazy('tasks')
    extra_context = {'header': _('Delete task')}
    success_message = _('Task deleted successfully!')

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if self.object.author != request.user:
            messages.error(request, _("A task can only be deleted by its author."))
            return redirect('tasks')
        return super().dispatch(request, *args, **kwargs)



class TaskDetailView(LoginRequiredMixin, DetailView):
    model = Task
    template_name = 'tasks/task_view.html'
    context_object_name = 'task'
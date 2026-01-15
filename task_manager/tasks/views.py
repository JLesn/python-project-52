from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import Task
from django.utils.translation import gettext_lazy as _
from task_manager.mixins import LoginRequiredMessageMixin
from django.contrib.messages.views import SuccessMessageMixin
from .forms import TaskFilterForm, TaskForm
from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect
from django.db.models import ProtectedError


class TasksListView(LoginRequiredMessageMixin, ListView):
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
    


class TaskCreationView(LoginRequiredMessageMixin, SuccessMessageMixin, CreateView):
     model = Task
     form_class = TaskForm
     success_url = reverse_lazy('tasks')
     template_name = 'form.html'
     success_message = _("Task successfully created")
     extra_context = {"title": _("Create task"), "button": _("Create")}

     def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
     


class TaskUpdateView(LoginRequiredMessageMixin, SuccessMessageMixin, UpdateView):
    model = Task
    form_class = TaskForm
    template_name = 'form.html'
    success_url = reverse_lazy('tasks')
    extra_context = {'title': _('Update task'), 'button': _('Update')}
    success_message = _('Task updated successfully!')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        self.object = self.get_object()
        if self.object.author != request.user:
            messages.error(request, _("You don't have permission to edit this task."))
            return redirect('tasks')
        return super().dispatch(request, *args, **kwargs)




class TaskDeleteView(LoginRequiredMessageMixin, SuccessMessageMixin, DeleteView):
    model = Task
    template_name = 'delete_form.html'
    success_url = reverse_lazy('tasks')
    extra_context = {'header': _('Delete task')}
    success_message = _('Task deleted successfully!')

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission() 

        self.object = self.get_object()
        if self.object.author != request.user:
            messages.error(request, _("You don't have permission to edit this task."))
            return redirect('tasks')
        
        return super().dispatch(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            response = super().delete(request, *args, **kwargs)
            return response
        except ProtectedError:
            messages.error(request, _("The task cannot be deleted because it is in use."))
            return redirect(self.success_url)



class TaskDetailView(LoginRequiredMessageMixin, DetailView):
    model = Task
    template_name = 'tasks/task_view.html'
    context_object_name = 'task'
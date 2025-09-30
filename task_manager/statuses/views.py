from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.db.models.deletion import ProtectedError
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


class StatusUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Status
    form_class = StatusForm
    template_name = 'form.html'
    success_url = reverse_lazy('statuses')
    extra_context = {'title': _('Update status'), 'button': _('Update')}
    success_message = _('Status updated successfully!')

class StatusDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = Status
    template_name = 'delete_form.html'
    success_url = reverse_lazy('statuses')
    extra_context = {'header': _('Delete status')}
    success_message = _('Status deleted successfully!')

    
    def form_valid(self, form):
        try:
            return super().form_valid(form)
        except ProtectedError:
            messages.error(
                self.request,
                _("Cannot delete status because it is used in tasks.")
            )
            return redirect(self.success_url)


    







# class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
#     model = MyUser
#     template_name = 'users/user_delete.html'
#     success_url = reverse_lazy('index')

#     def dispatch(self, request, *args, **kwargs):
#         obj = self.get_object()
#         if obj != request.user:
#             messages.error(request, _("You do not have permission to delete another user."))
#             return redirect('users')
#         return super().dispatch(request, *args, **kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         messages.success(request, self.success_message)
#         return super().delete(request, *args, **kwargs)


# class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
#     model = MyUser
#     form_class = CustomUserChangeForm
#     template_name = 'form.html'
#     success_url = reverse_lazy('users')
#     extra_context = {'title': _('Update user'), 'button': _('Update')}
#     success_message = _('Profile updated successfully!')

#     def dispatch(self, request, *args, **kwargs):
#         obj = self.get_object()
#         if obj != request.user:
#             messages.error(request, _("You do not have permission to modify another user."))
#             return redirect('users')
#         return super().dispatch(request, *args, **kwargs)





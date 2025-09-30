from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from .models import MyUser
from .forms import CustomUserCreationForm, CustomUserChangeForm
from django.utils.translation import gettext_lazy as _
from django.contrib import messages
from django.shortcuts import redirect



class UsersView(ListView):
    model = MyUser
    template_name = 'users/users_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return MyUser.objects.all()
    

class SignUpView(SuccessMessageMixin, CreateView):
    model = MyUser
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'form.html'
    extra_context = {'title': _('Registration'), 'button': _('Register')}
    success_message = _('Registration completed successfully!')
    

   
class UserUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = MyUser
    form_class = CustomUserChangeForm
    template_name = 'form.html'
    success_url = reverse_lazy('users')
    extra_context = {'title': _('Update user'), 'button': _('Update')}
    success_message = _('Profile updated successfully!')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj != request.user:
            messages.error(request, _("You do not have permission to modify another user."))
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)


class UserDeleteView(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = MyUser
    template_name = 'delete_form.html'
    success_url = reverse_lazy('index')
    extra_context = {'header': _('Delete user')}

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj != request.user:
            messages.error(request, _("You do not have permission to delete another user."))
            return redirect('users')
        return super().dispatch(request, *args, **kwargs)
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, self.success_message)
        return super().delete(request, *args, **kwargs)


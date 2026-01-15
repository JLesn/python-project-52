from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _


class LoginRequiredMessageMixin(LoginRequiredMixin):

    permission_denied_message = _("You are not authorized! Please log in.")
    login_url = reverse_lazy('login')

    def handle_no_permission(self):
        messages.error(self.request, self.permission_denied_message)
        return redirect(f"{self.login_url}?next={self.request.path}")
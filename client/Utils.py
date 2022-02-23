from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, redirect_to_login
from django.views import View

from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy


class LoginRequiredView(LoginRequiredMixin, View):
    login_url = reverse_lazy('login')
    redirect_field_name = 'next'
    permission_denied_message = "Please Login First."

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, self.get_permission_denied_message())
            return self.handle_no_permission()
        return super(LoginRequiredView, self).dispatch(request, *args, **kwargs)

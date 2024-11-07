from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect


class CustomLoginRequiredMixin(LoginRequiredMixin):
    login_url = reverse_lazy("users:login")

    def handle_no_permission(self):
        messages.error(
            self.request, "Только авторизованные пользователи могут управлять товарами"
        )
        return redirect(self.login_url)
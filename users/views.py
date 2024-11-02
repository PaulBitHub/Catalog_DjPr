import secrets

from django.contrib import messages
from django.contrib.auth.hashers import make_password
from django.contrib.auth.views import LoginView
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DetailView

from users.forms import CustomAuthenticationForm, UserCreateForm, UserProfileForm
from users.models import User
from users.utils import (
    send_email_confirm,
    generate_random_password,
    send_email_reset_password,
)

class CustomLoginView(LoginView):
    form_class = CustomAuthenticationForm
    template_name = "login.html"

class UserCreateView(CreateView):
    model = User
    form_class = UserCreateForm
    template_name = "users/user_form.html"
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}"
        send_email_confirm(url, user.email)

        messages.success(
            self.request,
            "Ссылка для подтверждения вашего email была отправлена на указанный адрес.",
        )
        return super().form_valid(form)

class UserProfileUpdateView(UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/user_profile_form.html"
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        return self.request.user


class UserProfileDetailView(DetailView):
    model = User
    template_name = "users/user_profile_detail.html"
    context_object_name = "user_profile"

    def get_object(self, queryset=None):
        return self.request.user


def email_verification(request, token):
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()

    messages.success(
        request, "Ваш email был успешно подтвержден! Теперь вы можете войти в систему."
    )
    return redirect(reverse("users:login"))


def password_reset(request):
    if request.method == "POST":
        email = request.POST.get("email")
        try:
            user = User.objects.get(email=email)
            new_password = generate_random_password()
            user.password = make_password(new_password)
            user.save()

            send_email_reset_password(new_password, email)
            messages.success(
                request, "Новый пароль был отправлен на вашу электронную почту"
            )
            return redirect("users:login")
        except ObjectDoesNotExist:
            messages.error(request, "Пользователь с таким email не найден")

    return render(request, "users/password_reset.html")
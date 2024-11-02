from django.contrib.auth.views import LoginView, LogoutView

from users.apps import UsersConfig
from django.urls import path
from users.views import (
    CustomLoginView,
    UserCreateView,
    email_verification,
    password_reset,
    UserProfileUpdateView,
    UserProfileDetailView,
)


app_name = UsersConfig.name

urlpatterns = [
    path('login/', CustomLoginView.as_view(template_name="login.html"), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", UserCreateView.as_view(), name="register"),
    path("email-confirm/<str:token>/", email_verification, name="email_confirm"),
    path("password-reset/", password_reset, name="password_reset"),
    path("profile/edit/", UserProfileUpdateView.as_view(), name="edit_profile"),
    path("profile/", UserProfileDetailView.as_view(), name="profile"),
]

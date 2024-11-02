from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from catalog.forms import StyleFormMixin
from users.models import User

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите ваш Email"}
        ),
    )

class UserCreateForm(StyleFormMixin, UserCreationForm):

    email = forms.EmailField(
        label="Email",
        widget=forms.EmailInput(
            attrs={"class": "form-control", "placeholder": "Введите ваш Email"}
        ),
    )

    password1 = forms.CharField(
        label="Пароль",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Введите пароль"}
        ),
    )
    password2 = forms.CharField(
        label="Подтверждение пароля",
        widget=forms.PasswordInput(
            attrs={"class": "form-control", "placeholder": "Подтвердите пароль"}
        ),
    )

    class Meta:
        model = User
        fields = ("email", "password1", "password2")

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "phone", "avatar", "country"]
        widgets = {
            "email": forms.EmailInput(
                attrs={"class": "form-control", "placeholder": "Введите email"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите номер телефона"}
            ),
            "avatar": forms.ClearableFileInput(attrs={"class": "form-control"}),
            "country": forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Введите страну"}
            ),
        }


class UserProfileViewForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "phone", "avatar", "country"]
        widgets = {
            "email": forms.TextInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
            "phone": forms.TextInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
            "avatar": forms.ClearableFileInput(
                attrs={
                    "class": "form-control",
                    "readonly": "readonly",
                    "disabled": True,
                }
            ),
            "country": forms.TextInput(
                attrs={"class": "form-control", "readonly": "readonly"}
            ),
        }
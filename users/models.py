from django.contrib.auth.models import AbstractUser
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

from catalog.utils import upload_to

BLANK_NULL_TRUE = {"blank": True, "null": True}


class User(AbstractUser):
    """
    Model for the user
    """

    username = None
    email = models.EmailField(unique=True, verbose_name="Email")
    phone = PhoneNumberField(verbose_name="Номер телефона", **BLANK_NULL_TRUE)
    avatar = models.ImageField(
        upload_to=upload_to, **BLANK_NULL_TRUE, verbose_name="Аватар"
    )
    country = models.CharField(max_length=50, **BLANK_NULL_TRUE, verbose_name="Страна")
    token = models.CharField(max_length=150, verbose_name="Токен", **BLANK_NULL_TRUE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self):
        return self.email

from django.core.management.base import BaseCommand
from django.core.exceptions import ValidationError
from users.models import User
from django.utils.text import capfirst

class Command(BaseCommand):
    def handle(self, *args, **options):
        email = options.get("email")
        password = options.get("password")

        if not email:
            email = input(capfirst("Введите email для суперпользователя: "))

        if User.objects.filter(email=email).exists():
            self.stdout.write(
                self.style.ERROR(
                    f"Ошибка: Пользователь с email {email} уже существует!"
                )
            )
            return

        if not password:
            password = input(capfirst("Введите пароль для суперпользователя: "))

        try:
            if len(password) < 8:
                raise ValidationError("Пароль должен быть не менее 8 символов")
        except ValidationError as e:
            self.stdout.write(self.style.ERROR(f"Ошибка: {e}"))
            return

        try:
            user = User.objects.create(email=email)
            user.set_password(password)
            user.is_active = True
            user.is_staff = True
            user.is_superuser = True
            user.save()
            self.stdout.write(
                self.style.SUCCESS(f"Суперпользователь {email} успешно создан!")
            )
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f"Ошибка при создании суперпользователя: {e}")
            )
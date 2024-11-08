from django.contrib.auth.models import Group, Permission
from django.core.management import BaseCommand

from users.models import User
from catalog.models import Product


class Command(BaseCommand):
    help = "Создание группы moderator и двух пользователей"

    def handle(self, *args, **options):
        superuser = User.objects.filter(is_superuser=True).first()
        if superuser:
            users_to_delete = User.objects.exclude(id=superuser.id)
            users_to_delete.delete()
        else:
            User.objects.all().delete()
        Group.objects.all().delete()
        moderator_group, created = Group.objects.get_or_create(name="Модератор")
        permissions = [
            "can_unpublish_product",
            "can_change_description",
            "can_change_category",
        ]
        for perm_codename in permissions:
            permission = Permission.objects.get(
                codename=perm_codename, content_type__model="product"
            )
            moderator_group.permissions.add(permission)

        moderator_user = User.objects.create(email="moderator@test.com")
        moderator_user.set_password("12345678")
        moderator_user.save()
        moderator_user.groups.add(moderator_group)

        owner_user = User.objects.create(email="owner@test.com")
        owner_user.set_password("12345678")
        owner_user.save()
        Product.objects.filter(id__in=[30, 29]).update(owner=owner_user)

        user = User.objects.create(email="user@test.com")
        user.set_password("12345678")
        user.save()

        superusers = User.objects.filter(is_superuser=True)
        for superuser in superusers:
            superuser.groups.add(moderator_group)

        self.stdout.write(self.style.SUCCESS(f"Успешно"))

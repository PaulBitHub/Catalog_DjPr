from django.db import models

from users.models import User, BLANK_NULL_TRUE

NULLABLE = {"blank": True, "null": True}

class Category(models.Model):
    category_name = models.CharField(
        max_length=50,
        verbose_name="Наименование категории",
        help_text="Введите наименование категории",
    )
    category_description = models.TextField(
        verbose_name="Описание категории", help_text="Опишите категорию"
    )

    def __str__(self):
        return self.category_name

    class Meta:
        verbose_name = "категория"
        verbose_name_plural = "категории"


class Product(models.Model):
    product_name = models.CharField(
        max_length=50,
        verbose_name="Наименование продукта",
        help_text="Введите наименование продукта",
    )
    product_description = models.TextField(
        max_length=500, verbose_name="Описание продукта ", help_text="Опишите продукт"
    )
    image = models.ImageField(
        upload_to="products/",
        blank=True,
        null=True,
        verbose_name="Изображение продукта",
        help_text="Загрузите изображение продукта",
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        verbose_name="Категория",
        related_name="catalog",
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Стоимость",
        help_text="Введите стоимость продукта",
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата создания")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="Дата изменения")

    is_published = models.BooleanField(
        default=False,
        verbose_name="Опубликовано",
        help_text="Статус публикации продукта")

    views_counter = models.PositiveIntegerField(
        verbose_name="Счётчик просмотров",
        help_text="Укажите кол-во просмотров",
        default=0,
    )

    owner = models.ForeignKey(
        User,
        verbose_name="Владелец товара",
        **BLANK_NULL_TRUE,
        on_delete=models.SET_NULL,
    )

    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = "Продукт"
        verbose_name_plural = "Продукты"
        ordering = ["product_name", "product_description", "price"]

    def get_active_version(self):
        return self.versions.filter(is_current=True).first()

class Version(models.Model):
    product = models.ForeignKey(
        Product,
        verbose_name="Наименование продукта",
        related_name="version",
        on_delete=models.SET_NULL,
        **NULLABLE,
    )
    version_number = models.PositiveIntegerField(
        default=0,
        verbose_name="Номер версии продукта",
        help_text="Введите номер версии продукта",
        **NULLABLE,
    )
    version_name = models.CharField(
        max_length=50,
        verbose_name="Наименование версии продукта",
        help_text="Введите наименование версии продукта",
        **NULLABLE,
    )
    is_current = models.BooleanField(
        verbose_name="признак текущей версии", help_text="Версия активна?", default=True
    )

    def save(self, *args, **kwargs):
        # Если номер версии не установлен, получаем максимальный номер версии для продукта
        if not self.version_number:
            max_version = Version.objects.filter(product=self.product).aggregate(models.Max('version_number'))[
                'version_number__max']
            self.version_number = (max_version + 1) if max_version is not None else 1

        # Устанавливаем флаг is_current для всех предыдущих версий в False
        Version.objects.filter(product=self.product, is_current=True).update(is_current=False)

        # Устанавливаем текущую версию как актуальную
        self.is_current = True

        # Сохраняем версию
        super().save(*args, **kwargs)

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = "Версия"
        verbose_name_plural = "Версии"
        ordering = ["-is_current", "version_number"]
        constraints = [
            models.UniqueConstraint(fields=['product', 'version_number'], name='unique_product_version')
        ]

    def __str__(self):
        return self.version_name

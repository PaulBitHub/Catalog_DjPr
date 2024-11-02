from django.contrib import admin
from catalog.models import Product, Category, Version


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("id", "product_name", "price", "category")
    list_filter = ("category",)
    search_fields = (
        "product_name",
        "product_description",
        "category",
        "views_counter",
    )

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "category_name")

@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ('id', 'product', 'version_number', 'version_name', 'is_current',)
    list_filter = ('version_number', 'is_current', 'version_name',)
    search_fields = ('version_number', 'is_current',)

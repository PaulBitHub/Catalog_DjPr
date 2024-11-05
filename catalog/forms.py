from django import forms
from django.forms import BooleanField
from catalog.models import Product, Version


class StyleFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, BooleanField):
                field.widget.attrs['class'] = 'form-check-input'
            else:
                field.widget.attrs['class'] = 'form-control'


class ProductForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ("views_counter", "owner")

    def clean_product_name(self):
        clean_data = self.cleaned_data.get('product_name', '')

        words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        for word in words:
            if word in clean_data.lower():
                raise forms.ValidationError(
                    'Вы не можете использовать запрещенные слова в названии продукта или описании продукта'
                )

        return clean_data

    def clean_product_description(self):
        clean_data = self.cleaned_data.get('product_description', '')

        words = ['казино', 'криптовалюта', 'крипта', 'биржа', 'дешево', 'бесплатно', 'обман', 'полиция', 'радар']

        for word in words:
            if word in clean_data.lower():
                raise forms.ValidationError(
                    'Вы не можете использовать запрещенные слова в названии продукта или описании продукта'
                )

        return clean_data

class ProductModeratorForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ("description", "category", "is_published")
        widgets = {
            "description": forms.Textarea(
                attrs={
                    "class": "form-control",
                    "placeholder": "Введите описание товара",
                }
            ),
            "category": forms.Select(attrs={"class": "form-select"}),
            "is_published": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }

class VersionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Version
        fields = '__all__'

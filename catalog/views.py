from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from catalog.forms import ProductForm, VersionForm, ProductModeratorForm
from catalog.models import Product, Version


class ProductListView(ListView):
    model = Product

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        for product in context_data['product_list']:
            active_version = Version.objects.filter(product=product, is_current=True)
            if active_version:
                product.active_version = active_version.last().version_name
            else:
                product.active_version = 'Отсутствует'

            product.can_unpublish = self.request.user.has_perm('catalog.can_unpublish_product')
            product.can_edit_as_moderator = self.request.user.has_perm('catalog.can_change_product_description') or \
                                            self.request.user.has_perm('catalog.can_change_product_category')
        return context_data

class ProductDetailView(DetailView):
    model = Product
    template_name = "catalog/product_details.html"

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        self.object.views_counter += 1
        self.object.save()
        return self.object

class ProductCreateView(CreateView, LoginRequiredMixin):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        product = form.save()
        user = self.request.user
        product.owner = user
        product.save()
        return super().form_valid(form)

    def get_form_class(self):
        required_perms = [
            "catalog.can_unpublish_product",
            "catalog.can_change_description",
            "catalog.can_change_category",
        ]
        user = self.request.user
        if user == self.object.owner or user.is_superuser:
            return ProductForm
        if user.has_perms(required_perms):
            return ProductModeratorForm
        raise PermissionDenied

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if (
                self.request.user == self.object.owner
                or self.request.user.groups.filter(name="moderator").exists()
                or self.request.user.is_superuser
        ):
            return self.object

        raise PermissionDenied


class ProductUpdateView(UpdateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def get_success_url(self):
        return reverse("catalog:product_details", args=[self.kwargs.get('pk')])

class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')

class VersionCreateView(CreateView):
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:product_list')


class VersionListView(ListView):
    model = Version
    context_object_name = 'versions'


class VersionDetailView(DetailView):
    model = Version


class VersionDeleteView(DeleteView):
    model = Version
    success_url = reverse_lazy('catalog:product_list')


class VersionUpdateView(UpdateView):
    model = Version
    form_class = VersionForm
    success_url = reverse_lazy('catalog:product_list')


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')

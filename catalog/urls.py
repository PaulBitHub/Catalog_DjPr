from django.urls import path
from django.views.decorators.cache import cache_page

from catalog.apps import CatalogConfig
from catalog.views import ProductListView, ProductDetailView, ProductCreateView, ProductUpdateView, ProductDeleteView, \
    VersionCreateView, VersionUpdateView, VersionDeleteView, VersionDetailView, VersionListView

app_name = CatalogConfig.name

urlpatterns = [
    path("", ProductListView.as_view(), name="product_list"),
    path('product/<int:pk>', cache_page(60)(ProductDetailView.as_view()), name="product_details"),
    path("create/", ProductCreateView.as_view(), name="product_create"),
    path("product/<int:pk>/update", ProductUpdateView.as_view(), name="product_update"),
    path("product/<int:pk>/delete/", ProductDeleteView.as_view(), name="product_delete"),
    # path('product/version/create', VersionCreateView.as_view(), name='version_create'),
    # path('product/version/update/<int:pk>', VersionUpdateView.as_view(), name='version_update'),
    # path('product/version/<int:pk>/delete', VersionDeleteView.as_view(), name='version_delete'),
    # path('product/version/<int:pk>/detail', VersionDetailView.as_view(), name='version_detail'),
    # path('product/version/list', VersionListView.as_view(), name='version_list'),
]

from django.core.cache import cache

from catalog.models import Product
from config.settings import  CACHES_ENABLE


def get_products_from_cache():
    '''
    Если кеш не включен, то он забирает данные из бд
    Если кеш включен, но нет данных, то он идет в бд забирает их и сохраняет,
    иначе он забирает их из кеша
    '''
    if not CACHES_ENABLE:
        return Product.objects.all()
    key = 'product_list'
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products)
    return products

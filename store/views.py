from django.shortcuts import render, get_object_or_404, redirect

from category.models import Category
from .models import Product

# Create your views here.

def store(request, category_slug=None):

    if category_slug is not None:
        categories = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.all().filter(category=categories, is_available=True)
    else:
        products= Product.objects.all().filter(is_available=True)

    products_count = products.count()

    context = {
        'products': products,
        'products_count': products_count,
               }
    return render(request, 'store/store.html', context)


def product_details(request, category_slug, product_slug):

    if product_slug is None:
        return redirect('store')

    product = get_object_or_404(
        Product,
        category__slug=category_slug,
        slug=product_slug)

    context = {
        'product': product,
    }

    return render(request, 'store/product-detail.html', context)

from django.shortcuts import render, get_object_or_404
from .models import Product, Category


def product_list(request):
    active_products = Product.objects.filter(is_active=True)
    context = {
        'products': active_products
    }
    return render(request, 'products/product_list.html', context)

def product_detail(request, slug):
    product = get_object_or_404(Product.objects.filter(is_active=True), slug=slug)
    context = {
        'product': product
    }
    return render(request, 'products/product_detail.html', context)

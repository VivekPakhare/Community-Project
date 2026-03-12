from django.shortcuts import render
from products.models import Product, Category


def home_view(request):
    featured = Product.objects.filter(status='active', is_featured=True)[:6]
    latest_products = Product.objects.filter(status='active')[:12]
    categories = Category.objects.all()
    return render(request, 'home.html', {
        'featured': featured,
        'latest_products': latest_products,
        'categories': categories,
    })


def privacy_view(request):
    return render(request, 'privacy.html')


def terms_view(request):
    return render(request, 'terms.html')

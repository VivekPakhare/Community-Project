from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Avg
from rest_framework import generics, permissions, filters
from rest_framework.parsers import MultiPartParser, FormParser

from .models import Product, ProductImage, Category, Review
from .forms import ProductForm, ProductImageForm
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer


# --- Template Views ---

def product_list_view(request):
    products = Product.objects.filter(status='active')
    categories = Category.objects.all()

    query = request.GET.get('q', '')
    category_slug = request.GET.get('category', '')
    min_price = request.GET.get('min_price', '')
    max_price = request.GET.get('max_price', '')
    condition = request.GET.get('condition', '')
    location = request.GET.get('location', '')

    if query:
        products = products.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category_slug:
        products = products.filter(category__slug=category_slug)
    if min_price:
        products = products.filter(price__gte=min_price)
    if max_price:
        products = products.filter(price__lte=max_price)
    if condition:
        products = products.filter(condition=condition)
    if location:
        products = products.filter(location__icontains=location)

    featured = Product.objects.filter(status='active', is_featured=True)[:6]

    context = {
        'products': products,
        'categories': categories,
        'featured': featured,
        'query': query,
        'selected_category': category_slug,
    }
    return render(request, 'products/product_list.html', context)


def product_detail_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    product.views_count += 1
    product.save(update_fields=['views_count'])
    reviews = product.reviews.all()
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg']
    return render(request, 'products/product_detail.html', {
        'product': product,
        'reviews': reviews,
        'avg_rating': avg_rating,
    })


@login_required
def product_create_view(request):
    if request.method == 'POST':
        form = ProductForm(request.POST)
        files = request.FILES.getlist('images')
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = request.user
            product.save()
            for i, f in enumerate(files):
                ProductImage.objects.create(product=product, image=f, is_primary=(i == 0))
            messages.success(request, 'Product listed successfully!')
            return redirect('products:detail', pk=product.pk)
    else:
        form = ProductForm()
    return render(request, 'products/product_form.html', {'form': form, 'editing': False})


@login_required
def product_edit_view(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        form = ProductForm(request.POST, instance=product)
        files = request.FILES.getlist('images')
        if form.is_valid():
            form.save()
            for f in files:
                ProductImage.objects.create(product=product, image=f)
            messages.success(request, 'Product updated successfully!')
            return redirect('products:detail', pk=product.pk)
    else:
        form = ProductForm(instance=product)
    return render(request, 'products/product_form.html', {'form': form, 'product': product, 'editing': True})


@login_required
def product_delete_view(request, pk):
    product = get_object_or_404(Product, pk=pk, seller=request.user)
    if request.method == 'POST':
        product.status = 'removed'
        product.save()
        messages.success(request, 'Product removed.')
        return redirect('products:list')
    return render(request, 'products/product_confirm_delete.html', {'product': product})


@login_required
def review_create_view(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk)
    if request.method == 'POST':
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        if rating:
            Review.objects.update_or_create(
                product=product, buyer=request.user,
                defaults={'seller': product.seller, 'rating': int(rating), 'comment': comment}
            )
            messages.success(request, 'Review submitted!')
    return redirect('products:detail', pk=product_pk)


# --- API Views ---

class ProductListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'description', 'location']
    ordering_fields = ['price', 'created_at', 'views_count']

    def get_queryset(self):
        qs = Product.objects.filter(status='active')
        category = self.request.query_params.get('category')
        if category:
            qs = qs.filter(category__slug=category)
        return qs

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class ProductDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProductSerializer
    queryset = Product.objects.all()

    def get_permissions(self):
        if self.request.method in ['PUT', 'PATCH', 'DELETE']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]


class CategoryListAPIView(generics.ListAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    permission_classes = [permissions.AllowAny]

from django.contrib import admin
from .models import Product, ProductImage, Category, Review


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'price', 'category', 'status', 'is_featured', 'created_at']
    list_filter = ['status', 'category', 'is_featured', 'condition']
    search_fields = ['title', 'description']
    inlines = [ProductImageInline]


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['buyer', 'seller', 'product', 'rating', 'created_at']
    list_filter = ['rating']

from rest_framework import serializers
from .models import Product, ProductImage, Category, Review


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ['id', 'image', 'is_primary']


class ProductSerializer(serializers.ModelSerializer):
    images = ProductImageSerializer(many=True, read_only=True)
    seller_name = serializers.CharField(source='seller.username', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)

    class Meta:
        model = Product
        fields = [
            'id', 'title', 'description', 'price', 'category', 'category_name',
            'seller', 'seller_name', 'condition', 'status', 'location',
            'is_featured', 'views_count', 'images', 'created_at', 'updated_at',
            'brand', 'ram', 'processor', 'storage', 'battery_health', 'author', 'edition',
            'city', 'area', 'pin_code',
            'seller_name', 'seller_phone', 'chat_enabled', 'call_enabled',
            'reason_for_selling', 'purchase_year', 'warranty_available', 'bill_available',
        ]
        read_only_fields = ['id', 'seller', 'views_count', 'created_at', 'updated_at']


class ReviewSerializer(serializers.ModelSerializer):
    buyer_name = serializers.CharField(source='buyer.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'product', 'buyer', 'buyer_name', 'seller', 'rating', 'comment', 'created_at']
        read_only_fields = ['id', 'buyer', 'created_at']

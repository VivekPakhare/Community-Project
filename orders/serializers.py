from rest_framework import serializers
from .models import Order, Payment


class OrderSerializer(serializers.ModelSerializer):
    product_title = serializers.CharField(source='product.title', read_only=True)
    buyer_name = serializers.CharField(source='buyer.username', read_only=True)
    seller_name = serializers.CharField(source='seller.username', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'product', 'product_title', 'buyer', 'buyer_name',
            'seller', 'seller_name', 'price', 'status', 'payment_method',
            'notes', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'buyer', 'seller', 'price', 'created_at', 'updated_at']


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['id', 'user', 'order', 'amount', 'payment_type', 'status', 'transaction_id', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

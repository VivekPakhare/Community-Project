from django.contrib import admin
from .models import Order, Payment


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'buyer', 'seller', 'price', 'status', 'created_at']
    list_filter = ['status', 'payment_method']
    search_fields = ['product__title', 'buyer__username', 'seller__username']


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'amount', 'payment_type', 'status', 'created_at']
    list_filter = ['payment_type', 'status']

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from rest_framework import generics, permissions

from products.models import Product
from .models import Order
from .serializers import OrderSerializer


# --- Template Views ---

@login_required
def order_create_view(request, product_pk):
    product = get_object_or_404(Product, pk=product_pk, status='active')
    if product.seller == request.user:
        messages.error(request, "You cannot buy your own product.")
        return redirect('products:detail', pk=product_pk)

    if request.method == 'POST':
        payment_method = request.POST.get('payment_method', 'cash')
        notes = request.POST.get('notes', '')
        order = Order.objects.create(
            product=product,
            buyer=request.user,
            seller=product.seller,
            price=product.price,
            payment_method=payment_method,
            notes=notes,
        )
        messages.success(request, f'Order #{order.id} placed successfully!')
        return redirect('orders:detail', pk=order.pk)
    return render(request, 'orders/order_create.html', {'product': product})


@login_required
def order_list_view(request):
    purchases = Order.objects.filter(buyer=request.user)
    sales = Order.objects.filter(seller=request.user)
    return render(request, 'orders/order_list.html', {'purchases': purchases, 'sales': sales})


@login_required
def order_detail_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if order.buyer != request.user and order.seller != request.user:
        messages.error(request, "Access denied.")
        return redirect('orders:list')
    return render(request, 'orders/order_detail.html', {'order': order})


@login_required
def order_update_status_view(request, pk):
    order = get_object_or_404(Order, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if order.seller == request.user and new_status in ['confirmed', 'cancelled']:
            order.status = new_status
            order.save()
            if new_status == 'confirmed':
                order.product.status = 'sold'
                order.product.save()
            messages.success(request, f'Order status updated to {new_status}.')
        elif order.buyer == request.user and new_status == 'completed':
            order.status = 'completed'
            order.save()
            messages.success(request, 'Order marked as completed.')
        elif order.buyer == request.user and new_status == 'cancelled':
            order.status = 'cancelled'
            order.save()
            messages.success(request, 'Order cancelled.')
    return redirect('orders:detail', pk=pk)


# --- API Views ---

class OrderListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(buyer=user) | Order.objects.filter(seller=user)

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        serializer.save(
            buyer=self.request.user,
            seller=product.seller,
            price=product.price,
        )


class OrderDetailAPIView(generics.RetrieveUpdateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Order.objects.filter(buyer=user) | Order.objects.filter(seller=user)

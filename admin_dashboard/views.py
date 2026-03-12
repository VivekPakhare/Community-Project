from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Count, Sum

from accounts.models import User
from products.models import Product, Category
from orders.models import Order, Payment
from messaging.models import Report


def is_admin(user):
    return user.is_superuser or user.role == 'admin'


@login_required
@user_passes_test(is_admin)
def dashboard_view(request):
    context = {
        'total_users': User.objects.count(),
        'total_products': Product.objects.count(),
        'active_products': Product.objects.filter(status='active').count(),
        'total_orders': Order.objects.count(),
        'pending_orders': Order.objects.filter(status='pending').count(),
        'total_revenue': Payment.objects.filter(status='completed').aggregate(total=Sum('amount'))['total'] or 0,
        'open_reports': Report.objects.filter(is_resolved=False).count(),
        'recent_products': Product.objects.order_by('-created_at')[:10],
        'recent_orders': Order.objects.order_by('-created_at')[:10],
        'recent_reports': Report.objects.filter(is_resolved=False).order_by('-created_at')[:10],
    }
    return render(request, 'admin_dashboard/dashboard.html', context)


@login_required
@user_passes_test(is_admin)
def user_list_view(request):
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'admin_dashboard/user_list.html', {'users': users})


@login_required
@user_passes_test(is_admin)
def user_toggle_active_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.is_active = not user.is_active
        user.save()
        status = 'activated' if user.is_active else 'deactivated'
        messages.success(request, f'User {user.username} {status}.')
    return redirect('admin_dashboard:users')


@login_required
@user_passes_test(is_admin)
def user_verify_view(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == 'POST':
        user.is_verified = True
        user.save()
        messages.success(request, f'User {user.username} verified.')
    return redirect('admin_dashboard:users')


@login_required
@user_passes_test(is_admin)
def product_management_view(request):
    products = Product.objects.all().order_by('-created_at')
    return render(request, 'admin_dashboard/product_list.html', {'products': products})


@login_required
@user_passes_test(is_admin)
def product_toggle_status_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        new_status = request.POST.get('status', 'removed')
        product.status = new_status
        product.save()
        messages.success(request, f'Product status changed to {new_status}.')
    return redirect('admin_dashboard:products')


@login_required
@user_passes_test(is_admin)
def product_toggle_featured_view(request, pk):
    product = get_object_or_404(Product, pk=pk)
    if request.method == 'POST':
        product.is_featured = not product.is_featured
        product.save()
        messages.success(request, f'Product featured status updated.')
    return redirect('admin_dashboard:products')


@login_required
@user_passes_test(is_admin)
def report_list_view(request):
    reports = Report.objects.all().order_by('-created_at')
    return render(request, 'admin_dashboard/report_list.html', {'reports': reports})


@login_required
@user_passes_test(is_admin)
def report_resolve_view(request, pk):
    report = get_object_or_404(Report, pk=pk)
    if request.method == 'POST':
        report.is_resolved = True
        report.save()
        messages.success(request, 'Report resolved.')
    return redirect('admin_dashboard:reports')


@login_required
@user_passes_test(is_admin)
def analytics_view(request):
    context = {
        'users_by_role': User.objects.values('role').annotate(count=Count('id')),
        'products_by_category': Category.objects.annotate(product_count=Count('products')),
        'orders_by_status': Order.objects.values('status').annotate(count=Count('id')),
    }
    return render(request, 'admin_dashboard/analytics.html', context)

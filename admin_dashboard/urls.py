from django.urls import path
from . import views

app_name = 'admin_dashboard'

urlpatterns = [
    path('', views.dashboard_view, name='dashboard'),
    path('users/', views.user_list_view, name='users'),
    path('users/<int:pk>/toggle/', views.user_toggle_active_view, name='user_toggle'),
    path('users/<int:pk>/verify/', views.user_verify_view, name='user_verify'),
    path('products/', views.product_management_view, name='products'),
    path('products/<int:pk>/status/', views.product_toggle_status_view, name='product_status'),
    path('products/<int:pk>/featured/', views.product_toggle_featured_view, name='product_featured'),
    path('reports/', views.report_list_view, name='reports'),
    path('reports/<int:pk>/resolve/', views.report_resolve_view, name='report_resolve'),
    path('analytics/', views.analytics_view, name='analytics'),
]

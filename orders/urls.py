from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('', views.order_list_view, name='list'),
    path('<int:pk>/', views.order_detail_view, name='detail'),
    path('create/<int:product_pk>/', views.order_create_view, name='create'),
    path('<int:pk>/status/', views.order_update_status_view, name='update_status'),

    # API endpoints
    path('api/', views.OrderListCreateAPIView.as_view(), name='api_list'),
    path('api/<int:pk>/', views.OrderDetailAPIView.as_view(), name='api_detail'),
]

from django.urls import path
from . import views

app_name = 'products'

urlpatterns = [
    path('', views.product_list_view, name='list'),
    path('<int:pk>/', views.product_detail_view, name='detail'),
    path('create/', views.product_create_view, name='create'),
    path('<int:pk>/edit/', views.product_edit_view, name='edit'),
    path('<int:pk>/delete/', views.product_delete_view, name='delete'),
    path('<int:product_pk>/review/', views.review_create_view, name='review'),

    # API endpoints
    path('api/', views.ProductListCreateAPIView.as_view(), name='api_list'),
    path('api/<int:pk>/', views.ProductDetailAPIView.as_view(), name='api_detail'),
    path('api/categories/', views.CategoryListAPIView.as_view(), name='api_categories'),
]

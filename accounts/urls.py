from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('user/<str:username>/', views.public_profile_view, name='public_profile'),

    # API endpoints
    path('api/register/', views.RegisterAPIView.as_view(), name='api_register'),
    path('api/profile/', views.ProfileAPIView.as_view(), name='api_profile'),
]

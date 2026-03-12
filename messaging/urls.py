from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path('', views.conversation_list_view, name='list'),
    path('<int:pk>/', views.conversation_detail_view, name='detail'),
    path('start/<str:username>/', views.start_conversation_view, name='start'),
    path('report/', views.report_create_view, name='report'),

    # API endpoints
    path('api/', views.ConversationListAPIView.as_view(), name='api_conversations'),
    path('api/<int:conversation_pk>/messages/', views.MessageListCreateAPIView.as_view(), name='api_messages'),
]

# urls.py

from django.urls import path
from . import views
app_name = 'chat'

urlpatterns = [
    path('', views.ChatListView.as_view(), name='all'),
    path('new/', views.ChatCreateView.as_view(), name='new'),
    path('update/', views.update_chats, name='update'),  # 新增這條路由處理 AJAX 請求
]

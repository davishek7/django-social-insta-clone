from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('inbox/', views.inbox, name='inbox'),
    path('t/<slug:slug>/', views.chat, name='chat'),
    path('send-message/', views.send_message, name='send_message'),
    path('new-chat/', views.new_chat, name='new_chat'),
    path('get/users/', views.get_users, name='get_users')
]
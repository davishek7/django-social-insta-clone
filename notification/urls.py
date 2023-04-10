from django.urls import path
from . import views

app_name = 'notification'

urlpatterns = [
    path('', views.list, name='list'),
    path('mark-as-read/', views.read_notifications, name='read_notifications'),
]
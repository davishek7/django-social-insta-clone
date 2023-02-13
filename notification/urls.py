from django.urls import path
from . import views

app_name = 'notification'

urlpatterns = [
    path('mark-as-read', views.read_notifications, name='read_notifications'),
]
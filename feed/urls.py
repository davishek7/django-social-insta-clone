from django.urls import path
from . import views

app_name = 'feed'

urlpatterns = [
    path('', views.index, name='index'),
    path('custom/feed/', views.custom_feed, name='custom_feed')
]
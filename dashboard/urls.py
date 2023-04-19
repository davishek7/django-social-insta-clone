from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.home, name='home'),
    path('users/', views.users, name='users'),
    path('posts/', views.posts, name='posts'),
    path('stories/', views.stories, name='stories'),
]

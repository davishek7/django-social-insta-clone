from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [    
    path('follow/<str:user_id>/', views.follow, name='follow'),
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
    path('remove/follower/<str:user_id>/', views.remove_follower, name='remove_follower'),
]
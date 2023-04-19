from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [    
    path('follow/<str:user_id>/', views.follow, name='follow'),
    path('unfollow/<str:username>/', views.unfollow, name='unfollow'),
    path('remove/follower/<str:user_id>/', views.remove_follower, name='remove_follower'),
    path('upload-photo/<str:username>/', views.upload_profile_photo, name='upload_profile_photo'),
    path('create-highlight/<str:username>/', views.create_highlight, name='create_highlight'),
    path('edit-highlight/<slug:slug>/', views.edit_highlight, name='edit_highlight'),
    path('delete-highlight/<slug:slug>/', views.delete_highlight, name='delete_highlight'),
]
from django.urls import path
from . import views

app_name = 'post'

urlpatterns = [
    path('create/', views.create_post, name='create_post'),
    path('<slug:slug>/', views.post_details, name='post_details'),
    path('<slug:slug>/comments/', views.get_post_comments, name='post_comments'),
    path('add-comment/<str:pk>/', views.add_comment, name='add_comment'),
    path('delete-comment/<str:pk>/', views.delete_comment, name='delete_comment'),
    path('add-like/<str:pk>/', views.add_like, name='add_like'),
    path('add-bookmark/<str:pk>/', views.add_bookmark, name='add_bookmark'),
    path('delete/<str:pk>/', views.delete_post, name='delete_post'),
    path('update/<slug:slug>/', views.update_post, name='update_post'),
    path('like-comment/<str:pk>/', views.like_comment, name='like_comment'),
    path('add-favorite/<str:user_id>/', views.add_favorites, name='add_favorites'),
    path('add-reply/<str:pk>/', views.add_reply, name='add_reply'),
    path('delete-reply/<str:pk>/', views.delete_reply, name='delete_reply'),
    path('like-reply/<str:pk>/', views.like_reply, name='like_reply'),
]
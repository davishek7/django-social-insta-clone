from django.urls import path
from . import views

app_name = 'activity'

urlpatterns = [
    path('interactions/likes/', views.likes, name='likes'),
    path('interactions/comments/', views.comments, name='comments'),
    path('interactions/story-replies/', views.story_replies, name='story_replies'),
    path('photos/posts/', views.posts, name='posts'),
    path('photos/highlights/', views.highlights, name='highlights'),
]
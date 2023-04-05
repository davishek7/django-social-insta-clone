from django.urls import path
from . import views

app_name = 'story'

urlpatterns = [
    path('details/<str:username>/<str:slug>/', views.story_details, name='story_details'),
    path('add-to-story/', views.add_to_story, name='add_to_story'),
    path('like-story/<str:slug>/', views.like_story, name='like_story'),
    path('reply-story/<str:slug>/', views.reply_to_story, name='reply_to_story'),
]
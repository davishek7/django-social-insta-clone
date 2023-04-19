from django.urls import path
from . import views
from user import views as user_views

app_name = 'story'

urlpatterns = [
    path('details/<str:username>/<slug:slug>/', views.story_details, name='story_details'),
    path('add-to-story/', views.add_to_story, name='add_to_story'),
    path('like-story/<slug:slug>/', views.like_story, name='like_story'),
    path('reply-story/<slug:slug>/', views.reply_to_story, name='reply_to_story'),
    path('delete-story/<slug:slug>/', views.delete_story, name='delete_story'),
    path('highlights/<slug:slug>/<slug:story_slug>/', user_views.highlight_details, name='highlight_details'),
]
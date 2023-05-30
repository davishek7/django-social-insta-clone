from django.urls import path
from . import views

app_name = 'activity'

urlpatterns = [
    path('interactions/likes/', views.likes, name='likes'),
]
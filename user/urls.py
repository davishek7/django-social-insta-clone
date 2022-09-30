from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [    
    path('follow/<str:user_id>/', views.follow, name='follow'),
]
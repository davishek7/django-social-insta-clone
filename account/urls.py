from django.urls import path
from . import views
from user import views as user_views

app_name = 'account'

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('edit/', user_views.edit_profile, name='edit_profile'),
]
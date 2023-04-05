"""insta URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from user import views as user_views
from search import views as search_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('feed.urls', namespace='feed')),
    path('accounts/', include('account.urls', namespace='account')),
    path('p/', include('post.urls', namespace='post')),
    path('direct/', include('chat.urls', namespace='chat')),
    path('user/', include('user.urls', namespace='user')),
    path('stories/', include('story.urls', namespace='story')),
    path('notification/', include('notification.urls', namespace='notification')),
    # path('dashboard/', include('dashboard.urls', namespace='dashboard')),

    # user views
    path('<str:username>/', user_views.profile, name='profile'),
    path('explore/people/', user_views.suggestions, name='suggestions'),

    # search views
    path('search', search_views.search, name='search'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
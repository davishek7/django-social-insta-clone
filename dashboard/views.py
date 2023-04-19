from django.shortcuts import render
from django.contrib.auth import get_user_model
from post.models import Post
from commons.decorators import admin_only
from django.db.models import Count
from datetime import date, datetime
from django.contrib.auth.decorators import login_required
from story.models import Story

# Create your views here.

@login_required
@admin_only
def home(request):

    top_users = get_user_model().objects.select_related('profile').exclude(is_superuser = True).annotate(follower_count = Count('profile__followers'), post_count = Count('post')).order_by('-follower_count', '-post_count').all()[:5]
    top_posts = Post.objects.select_related('user').prefetch_related('likes').annotate(likes_count = Count('likes'), comment_count = Count('post_comments')).order_by('-likes_count', '-comment_count', '-created_at').filter(status=True).all()[:5]
    todays_posts = Post.objects.filter(created_at__date = date.today()).count()

    total_users = get_user_model().objects.select_related('profile').exclude(is_superuser = True).count()
    total_posts = Post.objects.select_related('user').prefetch_related('likes').count()

    context = {'top_users':top_users, 'top_posts':top_posts, 'todays_posts':todays_posts, 'total_users':total_users, 'total_posts':total_posts, 'title':'Home', 'nav':'home'}
    return render(request, 'dashboard/index.html', context=context)

@login_required
@admin_only
def users(request):
    users = get_user_model().objects.select_related('profile').exclude(is_superuser = True)
    context = {'users':users, 'nav':'users'}
    return render(request, 'dashboard/users/list.html', context=context)

@login_required
@admin_only
def posts(request):
    posts = Post.objects.order_by('-created_at').all()
    context = {'posts':posts, 'nav':'posts'}
    return render(request, 'dashboard/posts/list.html', context=context)

@login_required
@admin_only
def stories(request):
    stories = Story.objects.order_by('-created_at').all()
    context = {'stories':stories, 'nav':'stories'}
    return render(request, 'dashboard/stories/list.html', context=context)
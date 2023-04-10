from django.shortcuts import render
from django.contrib.auth import get_user_model
from post.models import Post
from commons.decorators import admin_only
from django.db.models import Count
from datetime import date

# Create your views here.

@admin_only
def home(request):

    users = get_user_model().objects.select_related('profile').exclude(is_superuser = True).annotate(follower_count = Count('profile__followers'), post_count = Count('post')).order_by('-follower_count', '-post_count').all()[:5]
    posts = Post.objects.select_related('user').prefetch_related('likes').annotate(likes_count = Count('likes'), comment_count = Count('post_comments')).order_by('-likes_count', '-comment_count').filter(status=True).all()[:5]
    todays_posts = Post.objects.filter(created_at__date = date.today()).count()

    total_users = get_user_model().objects.select_related('profile').exclude(is_superuser = True).count()
    total_posts = Post.objects.select_related('user').prefetch_related('likes').count()

    context = {'users':users, 'posts':posts, 'todays_posts':todays_posts, 'total_users':total_users, 'total_posts':total_posts}
    return render(request, 'dashboard/index.html', context=context)
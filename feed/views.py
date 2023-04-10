from django.shortcuts import render
from django.db.models import Q, Count
from post.models import Post
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model
from story.models import Story
from story.utils import check_user_active_story
from commons.decorators import normal_user_only

# Create your views here.


@login_required
@normal_user_only
def index(request):
    posts = Post.objects.select_related('user').prefetch_related('likes').filter(status=True).all()

    active_story_user_ids = Story.objects.filter(user__in = request.user.profile.followings.all(), status=True).order_by('created_at').distinct().values_list('user')
    print(active_story_user_ids)

    active_story_users = get_user_model().objects.filter(id__in = active_story_user_ids).all()
    print(active_story_users)

    my_active_story_count = Story.objects.filter(user=request.user, status=True).all()
    
    paginator = Paginator(posts, 25)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'posts': page_obj, 'story_users':active_story_users, 'my_active_story_count':my_active_story_count,}
    return render(request, 'index.html', context=context)


@login_required
@normal_user_only
def custom_feed(request):

    followings_posts = Post.objects.select_related('user').prefetch_related('likes').filter(
        status=True).filter(user__id__in=request.user.profile.followings.all())
    
    favourites_posts = Post.objects.select_related('user').prefetch_related('likes').filter(
        status=True).filter(user__id__in=request.user.profile.favourites.all())
    
    hot_posts = Post.objects.select_related('user').prefetch_related('likes').filter(
        status=True).annotate(likes_count = Count('likes'), comments_count = Count('post_comments')).order_by('-likes_count', '-comments_count').all()

    variant = request.GET['variant']
    
    context = {'variant':variant,}

    if variant == 'following':
        context.update({'posts':followings_posts})
    elif variant == 'favorites':
        context.update({'posts':favourites_posts})
    elif variant == 'hot':
        context.update({'posts':hot_posts})

    return render(request, 'feed/custom-feed.html', context=context)
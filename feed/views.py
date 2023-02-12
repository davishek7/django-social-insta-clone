from django.shortcuts import render
from django.db.models import Q
from post.models import Post
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib.auth import get_user_model

# Create your views here.


@login_required
def index(request):
    posts = Post.objects.select_related('user').prefetch_related('likes').filter(status=True).all()
    
    suggestions = get_user_model().objects.exclude(Q(id__in=request.user.profile.followings.all())|Q(id=request.user.id))
    
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'posts': page_obj, 'suggestions':suggestions}
    return render(request, 'index.html', context=context)


@login_required
def custom_feed(request):

    followings_posts = Post.objects.select_related('user').prefetch_related('likes').filter(
        status=True).filter(user__id__in=request.user.profile.followings.all())
    
    favourites_posts = Post.objects.select_related('user').prefetch_related('likes').filter(
        status=True).filter(user__id__in=request.user.profile.favourites.all())
    
    context = {}

    variant = request.GET['variant']

    if variant == 'following':
        context = {'posts':followings_posts, 'variant':variant}
    elif variant == 'favorites':
        context = {'posts':favourites_posts, 'variant':variant}

    return render(request, 'feed/custom-feed.html', context=context)
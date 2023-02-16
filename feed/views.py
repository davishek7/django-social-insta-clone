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
    
    suggestions = get_user_model().objects.exclude(Q(id__in=request.user.profile.followings.all()) | Q(id=request.user.id))[:3]
    
    paginator = Paginator(posts, 25)
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
    
    suggestions = get_user_model().objects.exclude(Q(id__in=request.user.profile.followings.all()) | Q(id=request.user.id))[:3]

    variant = request.GET['variant']
    
    context = {'variant':variant, 'suggestions':suggestions}

    if variant == 'following':
        context.update({'posts':followings_posts})
    elif variant == 'favorites':
        context.update({'posts':favourites_posts})

    return render(request, 'feed/custom-feed.html', context=context)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.db.models import Q
from account.models import Profile
from post.models import Post

# Create your views here.

def profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    title = f'{user.name} (@{user.username}) \u2022 Instagram photos and videos'
    user_posts = Post.objects.filter(user=user, status=True).order_by('-created_at')
    user_bookmarks = user.profile.bookmarks.all()
    context = {'user':user, 'title':title, 'user_posts':user_posts, 'user_bookmarks':user_bookmarks}
    return render(request, 'user/profile.html', context=context)

def suggestions(request):
    suggestions = get_user_model().objects.exclude(Q(id__in=request.user.profile.followings.all())|Q(id=request.user.id))
    context={'suggestions':suggestions}
    return render(request, 'user/suggestions.html', context=context)

def follow(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    if user not in request.user.profile.followings.all():
        request.user.profile.followings.add(user_id)
        user.profile.followers.add(request.user)
    return redirect(request.META.get('HTTP_REFERER'))

def unfollow(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    if request.method == 'POST':
        if user in request.user.profile.followings.all():
            request.user.profile.followings.remove(user)
            user.profile.followers.remove(request.user)
            return redirect(request.META.get('HTTP_REFERER'))
    context = {'user':user}
    return render(request, 'user/unfollow.html',context=context)

def remove_follower(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    if user in request.user.profile.followers.all():
        request.user.profile.followers.remove(user_id)
        user.profile.followings.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER'))
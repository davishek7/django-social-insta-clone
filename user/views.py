from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from account.models import Profile

# Create your views here.

def profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    title = f'{user.name} (@{user.username}) \u2022 Instagram photos and videos'
    context = {'user':user, 'title':title}
    return render(request, 'user/profile.html', context=context)

def suggestions(request):
    context={}
    return render(request, 'user/suggestions.html', context=context)

def follow(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    if user_id not in request.user.profile.followings.all():
        request.user.profile.followings.add(user_id)
        user.profile.followers.add(request.user)
    else:
        request.user.profile.followings.remove(user_id)
        user.profile.followers.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER'))
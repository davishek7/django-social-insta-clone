from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q
from account.models import Profile
from post.models import Post
from django.contrib.auth.decorators import login_required

# Create your views here.

def profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    title = f'{user.name} (@{user.username}) \u2022 Instagram photos and videos'
    user_posts = Post.objects.filter(user=user, status=True).order_by('-created_at')
    user_posts_count = user_posts.count()
    user_bookmarks = user.profile.bookmarks.filter(status=True)
    context = {'user':user, 'title':title, 'user_posts':user_posts, 'user_bookmarks':user_bookmarks, 'user_posts_count':user_posts_count}
    return render(request, 'user/profile.html', context=context)


@login_required
def upload_profile_photo(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    if request.method == 'POST':
        uploaded_photo = request.FILES.get('profile_photo')
        user.profile_photo = uploaded_photo
        user.save()
        messages.success(request, 'Profile picture updated successfully.')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def suggestions(request):
    suggestions = get_user_model().objects.exclude(Q(id__in=request.user.profile.followings.all())|Q(id=request.user.id)|Q(is_superuser=True))
    context={'suggestions':suggestions}
    return render(request, 'user/suggestions.html', context=context)

@login_required
def follow(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    if user not in request.user.profile.followings.all():
        request.user.profile.followings.add(user_id)
        user.profile.followers.add(request.user)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
def unfollow(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    if request.method == 'POST':
        if user in request.user.profile.followings.all():
            request.user.profile.followings.remove(user)
            user.profile.followers.remove(request.user)
            return redirect('profile', request.user.username)
    context = {'user':user}
    return render(request, 'user/unfollow.html',context=context)

@login_required
def remove_follower(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    if user in request.user.profile.followers.all():
        request.user.profile.followers.remove(user_id)
        user.profile.followings.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER'))
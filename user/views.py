from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.db.models import Q
from account.models import Profile
from post.models import Post
from django.contrib.auth.decorators import login_required
from commons.decorators import normal_user_only
from .models import Highlight
from story.models import Story
from .decorators import highlight_user_required, user_required

# Create your views here.

@normal_user_only
def profile(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    title = f'{user.name} (@{user.username}) \u2022 Instagram photos and videos'
    user_posts = Post.objects.filter(user=user, status=True).order_by('-created_at')
    stories_count = Story.objects.filter(user = user).count()
    highlights = Highlight.objects.filter(user = user, status = True).order_by('-created_at').all()
    user_posts_count = user_posts.count()
    context = {'user':user, 'title':title, 'user_profile':True, 'user_posts':user_posts,
               'user_posts_count':user_posts_count, 'highlights':highlights, 'stories_count':stories_count}
    return render(request, 'user/profile/profile.html', context=context)

@login_required
@normal_user_only
@user_required
def user_saved(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    title = f'{user.name} (@{user.username}) \u2022 Instagram photos and videos'
    user_posts = Post.objects.filter(user=user, status=True).order_by('-created_at')
    stories_count = Story.objects.filter(user = user).count()
    highlights = Highlight.objects.filter(user = user, status = True).order_by('-created_at').all()
    user_posts_count = user_posts.count()
    user_bookmarks = user.profile.bookmarks.filter(status=True)
    context = {'user':user, 'title':title, 'user_bookmarks':user_bookmarks, 'bookmark':True, 
               'user_posts_count':user_posts_count, 'highlights':highlights, 'stories_count':stories_count}
    return render(request, 'user/profile/profile.html', context=context)

@login_required
@normal_user_only
def upload_profile_photo(request, username):
    user = get_object_or_404(get_user_model(), username=username)
    if request.method == 'POST':
        uploaded_photo = request.FILES.get('profile_photo')
        user.profile_photo = uploaded_photo
        user.save()
        messages.success(request, 'Profile picture updated successfully.')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@normal_user_only
def suggestions(request):
    suggestions = get_user_model().objects.exclude(Q(id__in=request.user.profile.followings.all())|Q(id=request.user.id)|Q(is_superuser=True))
    context={'suggestions':suggestions}
    return render(request, 'user/suggestions.html', context=context)

@login_required
@normal_user_only
def follow(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    if user not in request.user.profile.followings.all():
        request.user.profile.followings.add(user_id)
        user.profile.followers.add(request.user)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@normal_user_only
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
@normal_user_only
def remove_follower(request, user_id):
    user = get_object_or_404(get_user_model(), id=user_id)
    if user in request.user.profile.followers.all():
        request.user.profile.followers.remove(user_id)
        user.profile.followings.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@normal_user_only
def create_highlight(request, username):
    user = get_user_model().objects.select_related('profile').filter(username = username, is_active = True).first()
    if request.method == 'POST':
        name = request.POST.get('highlight_name')
        _stories = request.POST.getlist('story')
        if len(_stories) > 0:
            highlight = Highlight.objects.create(name = name, user = user)
            stories = Story.objects.filter(id__in = _stories, user = user).all()
            highlight.stories.add(*stories)
            messages.info(request, 'Highlight added.')
        else:
            messages.warning(request, 'Please select atleast one story.')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@normal_user_only
def highlight_details(request, slug, story_slug):
    highlight = get_object_or_404(Highlight, slug = slug)
    story = get_object_or_404(Story, slug=story_slug)
    highlight_stories = Story.objects.filter(id__in = highlight.stories.all()).all()

    prev_story = Story.objects.filter(id__in = highlight.stories.all(), created_at__lt = story.created_at,).last()
    next_story = Story.objects.filter(id__in = highlight.stories.all(), created_at__gt = story.created_at,).first()

    context = {'highlight':highlight, 'story':story, 'highlight_stories':highlight_stories, 
               'prev_story':prev_story, 'next_story':next_story, 'title':'Stories'}
    return render(request, 'user/highlight-details.html', context=context)

@login_required
@normal_user_only
@highlight_user_required
def edit_highlight(request, slug):
    highlight = get_object_or_404(Highlight, slug=slug)
    if request.method == 'POST':
        name = request.POST.get('highlight_name')
        _stories = request.POST.getlist('story')
        if name != highlight.name:
            highlight.name = name
            highlight.save()
        stories = Story.objects.filter(id__in = _stories)
        for story in stories:
            if story not in highlight.stories.all():
                highlight.stories.add(story)
    return redirect('profile', username=highlight.user.username)

@login_required
@normal_user_only
@highlight_user_required
def delete_highlight(request, slug):
    highlight = get_object_or_404(Highlight, slug=slug)
    highlight.delete()
    return redirect('profile', username = highlight.user.username)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from post.models import Post, Comment
from story.models import Story, StoryReply
from user.models import Highlight
from itertools import chain

# Create your views here.

def likes(request):
    user = get_object_or_404(get_user_model(), username=request.user.username)
    liked_posts = user.post_likes.all()
    context = {'liked_posts':liked_posts, 'likes':True, 'interactions':True}
    return render(request, 'activity/interactions.html', context=context)

def comments(request):
    user = get_object_or_404(get_user_model(), username=request.user.username)
    user_comments = user.user_comments.all()
    user_replies = user.user_replies.all()
    all_comments = sorted(chain(user_comments, user_replies), key=lambda instance: instance.created_at, reverse=True)
    context = {'all_comments':all_comments, 'comments':True, 'interactions':True, 'category':'all'}
    
    category = request.GET.get('category')

    if category == 'all':
        context.update({'all_comments':all_comments})
    elif category == 'comments':
        context.update({'all_comments':user_comments, 'category':'comments'})
    elif category == 'replies':
        context.update({'all_comments':user_replies, 'category':'replies'})

    return render(request, 'activity/interactions.html', context=context)

def story_replies(request):
    user = get_object_or_404(get_user_model(), username=request.user.username)
    story_replies = user.storyreply_set.all()
    context = {'story_replies':story_replies, 'story_replies_tab':True, 'interactions':True}
    return render(request, 'activity/interactions.html', context=context)

def posts(request):
    user = get_object_or_404(get_user_model(), username=request.user.username)
    user_posts = Post.objects.filter(user=user, status=True).order_by('-created_at')
    context = {'user_posts':user_posts, 'posts':True, 'photos':True}
    return render(request, 'activity/photos.html', context=context)

def highlights(request):
    user = get_object_or_404(get_user_model(), username=request.user.username)
    user_highlights = Highlight.objects.filter(user=user, status=True).order_by('-created_at')
    context = {'user_highlights':user_highlights, 'highlights':True, 'photos':True}
    return render(request, 'activity/photos.html', context=context)
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from post.models import Post, Comment
from story.models import Story, StoryReply
from user.models import Highlight

# Create your views here.

def likes(request):
    user = get_object_or_404(get_user_model(), username=request.user.username)
    liked_posts = user.post_likes.all()
    comments = user.user_comments.all()
    story_replies = user.storyreply_set.all()
    print(story_replies)
    # print(dir(user))
    context = {'liked_posts':liked_posts, 'comments':comments}
    return render(request, 'activity/list.html', context=context)
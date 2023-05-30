from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Story
from .forms import StoryForm, StoryReplyForm
from django.contrib import messages
from .decorators import increament_story_view_count, story_user_required, redirect_to_home_on_story_expire
from commons.decorators import normal_user_only
from feed.decorators import remove_old_stories

# Create your views here.

User = get_user_model()

@login_required
@redirect_to_home_on_story_expire
@remove_old_stories
@increament_story_view_count
def story_details(request, username, slug):
    user = get_user_model().objects.filter(username=username).first()
    story = Story.objects.filter(user = user, slug = slug, status = True).first()
    user_stories = Story.objects.filter(user=user, status = True).all()
    prev_story = Story.objects.filter(user = user, created_at__lt = story.created_at, status = True).last()
    next_story = Story.objects.filter(user = user, created_at__gt = story.created_at, status = True).first()
    story_reply_form = StoryReplyForm()
    context = {'user':user, 'story':story, 'user_stories':user_stories, 
               'prev_story':prev_story, 'next_story':next_story, 
               'story_reply_form':story_reply_form, 'title':'Stories', 'story_page':True}
    return render(request, 'story/story-details.html', context=context)

@login_required
@normal_user_only
def add_to_story(request):
    if request.method == 'POST':
        caption = request.POST.get('caption')
        images = request.FILES.getlist('images')      
        for image in images:
            Story.objects.create(caption=caption, user=request.user, image=image)
            messages.success(request, 'Your story updated successfully.')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@normal_user_only
def like_story(request, slug):
    story = get_object_or_404(Story, slug=slug)
    if request.user not in story.likes.all():
        story.likes.add(request.user)
    else:
        story.likes.remove(request.user)
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@normal_user_only
def reply_to_story(request, slug):
    story = get_object_or_404(Story, slug=slug)
    if request.method == 'POST':
        story_reply_form = StoryReplyForm(request.POST)
        if story_reply_form.is_valid():
            story_reply = story_reply_form.save(commit = False)
            story_reply.story = story
            story_reply.user = request.user
            story_reply.save()
            messages.success(request, 'Message sent.')
        else:
            messages.error(request, 'Something went wrong.')
    return redirect(request.META.get('HTTP_REFERER'))

@login_required
@normal_user_only
@story_user_required
def delete_story(request, slug):
    story = get_object_or_404(Story, slug=slug)
    story.status=False
    story.save()
    messages.info(request, 'Story deleted.')
    return redirect('/')

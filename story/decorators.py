from functools import wraps
from django.shortcuts import redirect, get_object_or_404
from .models import Story
from django.contrib import messages


def increament_story_view_count(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        story = get_object_or_404(Story, slug=kwargs.get('slug'))
        if not request.user.is_superuser and request.user != story.user and request.user not in story.views.all():
            story.views.add(request.user)
        return view_func(request, *args, **kwargs)
    return wrapper

def story_user_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'slug' in kwargs:
            story = get_object_or_404(Story, slug=kwargs.get('slug'))
        if story.user == request.user:
            return view_func(request, *args, **kwargs)
        else:
            messages.warning(request, 'You are not authorised!')
            return redirect(request.META.get('HTTP_REFERER'))
    return wrapper
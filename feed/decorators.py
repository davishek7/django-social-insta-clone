from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from story.models import Story
from django.db.models.functions import Now
from datetime import timedelta


def remove_old_stories(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if (old_stories := Story.objects.filter(status = True, created_at__lt = Now() - timedelta(days=1))).exists():
            old_stories.update(status = False)
        return view_func(request, *args, **kwargs)
    return wrapper
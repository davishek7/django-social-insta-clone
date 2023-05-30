from functools import wraps
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model
from .models import Highlight


def user_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        user = get_object_or_404(get_user_model(), username=kwargs.get('username'))
        if user == request.user:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('user_saved', username=request.user.username)
    return wrapper

def highlight_user_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'slug' in kwargs:
            highlight = get_object_or_404(Highlight, slug=kwargs.get('slug'))
        if highlight.user == request.user:
            return view_func(request, *args, **kwargs)
        else:
            return redirect(request.META.get('HTTP_REFERER'))
    return wrapper
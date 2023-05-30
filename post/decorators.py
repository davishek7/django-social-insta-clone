from functools import wraps
from django.shortcuts import redirect, get_object_or_404
from .models import Post, Comment, Reply


def post_user_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'pk' in kwargs:
            post = get_object_or_404(Post, id=kwargs.get('pk'))
        if 'slug' in kwargs:
            post = get_object_or_404(Post, slug=kwargs.get('slug'))
        if post.user == request.user:
            return view_func(request, *args, **kwargs)
        else:
            return redirect(request.META.get('HTTP_REFERER'))
    return wrapper

def comment_user_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'pk' in kwargs:
            comment = get_object_or_404(Comment, id=kwargs.get('pk'))
        if comment.user == request.user:
            return view_func(request, *args, **kwargs)
        else:
            return redirect(request.META.get('HTTP_REFERER'))
    return wrapper

def reply_user_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'pk' in kwargs:
            reply = get_object_or_404(Reply, id=kwargs.get('pk'))
        if reply.user == request.user:
            return view_func(request, *args, **kwargs)
        else:
            return redirect(request.META.get('HTTP_REFERER'))
    return wrapper
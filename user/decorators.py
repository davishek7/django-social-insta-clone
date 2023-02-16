from functools import wraps
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import get_user_model


def user_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'user_id' in kwargs:
            user = get_object_or_404(get_user_model(), id=kwargs.get('user_id'))
        if 'username' in kwargs:
            user = get_object_or_404(get_user_model(), slug=kwargs.get('username'))
        if user == request.user:
            return view_func(request, *args, **kwargs)
        else:
            return redirect(request.META.get('HTTP_REFERER'))
    return wrapper
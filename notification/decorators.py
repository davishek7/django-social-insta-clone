from functools import wraps
from django.shortcuts import redirect
from .models import Notification


def read_notifications(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if(unread_notifications := Notification.objects.filter(to_user = request.user, status = True, read_status = False)).exists():
            unread_notifications.update(read_status = True)
        return view_func(request, *args, **kwargs)
    return wrapper
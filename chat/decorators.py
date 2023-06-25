from functools import wraps
from django.shortcuts import redirect, get_object_or_404
from .models import Inbox, Message
from django.db.models import Q


def read_messages(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if 'slug' in kwargs:
            inbox = get_object_or_404(Inbox, slug=kwargs.get('slug'))
        if(unread_messages := Message.objects.filter(~Q(user = request.user), inbox = inbox, status = True, read_status = False)).exists():
            unread_messages.update(read_status = True)
        return view_func(request, *args, **kwargs)
    return wrapper
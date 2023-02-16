import os
from post.forms import PostForm, PostImageForm, CommentForm
from account.models import Profile
from django.shortcuts import get_object_or_404
from notification.models import Notification
from django.conf import settings

def common_context(request):
    return {
        'post_form' : PostForm(),
        'image_form' : PostImageForm(),
        'comment_form' : CommentForm(),
        'profile' : request.user.profile if request.user.is_authenticated else None,
        'unread_notifications' : Notification.objects.filter(to_user = request.user, status=True, read_status=False) if request.user.is_authenticated else None,
        'read_notifications' : Notification.objects.filter(to_user = request.user, status=True, read_status=True) if request.user.is_authenticated else None,
        'unread_notifications_count' : Notification.objects.filter(to_user = request.user, read_status = False).count() if request.user.is_authenticated else None,
        'host' : settings.HOST
    }
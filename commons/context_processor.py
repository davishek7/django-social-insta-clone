from post.forms import PostForm, PostImageForm, CommentForm
from account.models import Profile
from django.shortcuts import get_object_or_404
from notification.models import Notification

def common_context(request):
    return {
        'post_form' : PostForm(),
        'image_form' : PostImageForm(),
        'comment_form' : CommentForm(),
        'profile' : request.user.profile if request.user.is_authenticated else None,
        'notifications' : Notification.objects.filter(to_user = request.user) if request.user.is_authenticated else None
    }
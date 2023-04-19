from post.forms import PostForm, PostImageForm, CommentForm, ReplyForm
from account.models import Profile
from django.shortcuts import get_object_or_404
from notification.models import Notification
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from story.forms import StoryForm

def common_context(request):
    return {
        'post_form' : PostForm(),
        'image_form' : PostImageForm(),
        'comment_form' : CommentForm(),
        'reply_form' : ReplyForm(),
        'story_form' : StoryForm(),
        'profile' : request.user.profile if request.user.is_authenticated else None,
        'unread_notifications_count' : Notification.objects.filter(to_user = request.user, read_status = False).count() if request.user.is_authenticated else None,
        'host' : settings.HOST,
        'suggestions' : get_user_model().objects.exclude(Q(id__in=request.user.profile.followings.all()) | Q(id=request.user.id) | Q(is_superuser=True))[:3] if request.user.is_authenticated else None
    }
from post.forms import PostForm, PostImageForm, CommentForm, ReplyForm
from account.models import Profile, User
from django.shortcuts import get_object_or_404
from notification.models import Notification
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models import Q
from story.forms import StoryForm
from chat.forms import MessageForm
from chat.models import Message


def common_context(request):
    if request.user.is_authenticated:
        return {
            'post_form' : PostForm(),
            'image_form' : PostImageForm(),
            'comment_form' : CommentForm(),
            'reply_form' : ReplyForm(),
            'story_form' : StoryForm(),
            'message_form' : MessageForm(),
            'profile' : request.user.profile,
            'unread_notifications_count' : Notification.objects.filter(to_user = request.user, read_status = False).count(),
            'unread_messages_count' : Message.objects.filter(~Q(user=request.user), inbox__in  = request.user.user_inboxes.all(), status=True, read_status = False).count(),
            'host' : settings.HOST,
            'suggestions' : get_user_model().objects.exclude(Q(id__in=request.user.profile.followings.all()) | Q(id=request.user.id) | Q(is_superuser=True))[:3],
            'user_has_profile_photo' : True if request.user.profile_photo else False
        }
    return {}
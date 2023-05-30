from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from story.models import Story, StoryReply
from django.db.models.functions import Now
from django.db.models import Q
from datetime import timedelta
from notification.models import Notification


def remove_old_stories(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):

        if (old_stories := Story.objects.filter(created_at__lt = Now() - timedelta(hours=24))).exists():
            for old_story in old_stories:
                if old_story.status:
                    old_story.status = False
                    old_story.save()

                old_story_like_notifications = (Notification.objects.filter(entity_id = old_story.id)
                                        .filter(entity_type = Notification.STORY_LIKE).all())
                old_story_like_notifications.update(status = False, read_status = True)

                if (old_story_replies := StoryReply.objects.filter(story = old_story)).exists():
                    for story_reply in old_story_replies:
                        if story_reply.status:
                            story_reply.status = False
                            story_reply.save()

                        old_story_reply_notifications = (Notification.objects.filter(entity_id = story_reply.id)
                                                .filter(entity_type = Notification.STORY_REPLY).all())
                        old_story_reply_notifications.update(status = False, read_status = True)

        return view_func(request, *args, **kwargs)
    return wrapper
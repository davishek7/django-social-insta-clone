from django.db import models
from commons.models import TimeStampModel, StatusModel
from post.models import User, Post


# Create your models here.

class Notification(TimeStampModel, StatusModel):

    POST_LIKE = 'POST_LIKE'
    POST_COMMENT = 'POST_COMMENT'
    POST_COMMENT_LIKE = 'POST_COMMENT_LIKE'
    POST_COMMENT_REPLY = 'POST_COMMENT_REPLY'
    POST_COMMENT_REPLY_LIKE = 'POST_COMMENT_REPLY_LIKE'
    USER_FOLLOW = 'USER_FOLLOW'
    STORY_LIKE = 'STORY_LIKE'
    STORY_REPLY = 'STORY_REPLY'

    NOTIFICATION_TYPE = (
        ('POST_LIKE', POST_LIKE),
        ('POST_COMMENT', POST_COMMENT),
        ('POST_COMMENT_LIKE', POST_COMMENT_LIKE),
        ('POST_COMMENT_REPLY', POST_COMMENT_REPLY),
        ('POST_COMMENT_REPLY_LIKE', POST_COMMENT_REPLY_LIKE),
        ('USER_FOLLOW', USER_FOLLOW),
        ('STORY_LIKE', STORY_LIKE),
        ('STORY_REPLY', STORY_REPLY)
    )

    entity_id = models.IntegerField(default=0, blank=True, null=True)
    entity_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPE, blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_sender', blank=True, null=True)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_receiver', blank=True, null=True)
    read_status = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.from_user}'s notification to {self.to_user}"
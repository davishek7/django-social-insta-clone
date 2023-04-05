from django.db import models
from commons.models import TimeStampModel, StatusModel
from post.models import User, Post


# Create your models here.

class Notification(TimeStampModel, StatusModel):
    title = models.CharField(max_length=255, blank=True, null=True)
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_sender', blank=True, null=True)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notification_receiver', blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.DO_NOTHING, related_name='notification_post', blank=True, null=True)
    read_status = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.from_user}'s notification to {self.to_user}"
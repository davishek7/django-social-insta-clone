from django.db import models
from commons.models import TimeStampModel, StatusModel
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from post.random_slug import generate_random_slug

# Create your models here.

User = settings.AUTH_USER_MODEL

class Story(TimeStampModel, StatusModel):
    caption = models.CharField(max_length=500, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True, blank=True, null=True)
    image = models.ImageField(upload_to='story', blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='story_likes', blank=True)
    views = models.ManyToManyField(User, related_name='story_viewers', blank=True)

    def __str__(self):
        return f"{self.user}'s story - {self.caption}"
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = generate_random_slug()
        super(Story, self).save(*args, **kwargs)

    class Meta:
        ordering = ['created_at']
        verbose_name_plural = 'stories'


class StoryReply(TimeStampModel, StatusModel):
    story = models.ForeignKey(Story, on_delete=models.CASCADE, related_name='story_replies', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    body = models.TextField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"{self.user}'s reply"

    class Meta:
        ordering = ['-created_at']

    
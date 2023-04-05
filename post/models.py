from django.db import models
from commons.models import TimeStampModel, StatusModel
from django.contrib.auth.models import BaseUserManager
from django.conf import settings
from .random_slug import generate_random_slug

# Create your models here.

User = settings.AUTH_USER_MODEL

class Post(TimeStampModel, StatusModel):
    caption = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(max_length=255, db_index=True, unique=True, blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='post_likes', blank=True)

    def __str__(self):
        return self.caption

    def save(self, *args, **kwargs):
        if not self.id:
            self.slug = generate_random_slug()
        super(Post, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']


class PostImage(TimeStampModel, StatusModel):
    image = models.ImageField(upload_to='post', blank=True, null=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, blank=True, null=True)

    def __str__(self):
        return self.post.caption

class CommentManager(BaseUserManager):
    def get_queryset(self):
        return super().get_queryset().filter(status=True)
    
class Comment(TimeStampModel, StatusModel):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_comments', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_comments', blank=True, null=True)
    body = models.TextField(max_length=255, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='comment_likes', blank=True)
    objects = CommentManager()

    def __str__(self):
        return self.body
    
    class Meta:
        ordering = ['-created_at']


class Reply(TimeStampModel, StatusModel):
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_replies', blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user_replies', blank=True, null=True)
    body = models.TextField(max_length=255, blank=True, null=True)
    likes = models.ManyToManyField(User, related_name='reply_likes', blank=True)
    objects = CommentManager()

    class Meta:
        ordering = ['created_at']
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Notification
from account.models import Profile
from post.models import Post, Comment

User = get_user_model()

@receiver(m2m_changed, sender=Profile.followers.through)
def send_notification_on_follow(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        notification_sender = User.objects.get(id=list(pk_set)[0])
        notification_receiver = User.objects.get(id = instance.user_id)
        if instance.user != notification_sender:
            Notification.objects.create(
                title = f'{notification_sender.username} started following you.',
                from_user = notification_sender,
                to_user = notification_receiver
            )

@receiver(m2m_changed, sender=Post.likes.through)
def send_notification_on_like(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        notification_sender = User.objects.get(id=list(pk_set)[0])
        notification_receiver = User.objects.get(id = instance.user_id)
        if instance.user != notification_sender:
            Notification.objects.create(
                title = f'{notification_sender.username} liked your post.',
                from_user = notification_sender,
                to_user = notification_receiver,
                post = instance
            )

@receiver(post_save, sender=Comment)
def send_notification_on_comment(created, sender, instance, **kwargs):
    if created:
        notification_sender = User.objects.get(id=instance.user_id)
        notification_receiver = User.objects.get(id = instance.post.user_id)
        if instance.user != instance.post.user:
            Notification.objects.create(
                title = f'{notification_sender.username} commented on your post.',
                from_user = notification_sender,
                to_user = notification_receiver,
                post = instance.post
            )
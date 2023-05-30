from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from .models import Notification
from account.models import Profile
from post.models import Post, Comment, Reply
from story.models import Story, StoryReply
from django.db.models import Q

User = get_user_model()

@receiver(m2m_changed, sender=Profile.followers.through)
def send_notification_on_follow(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        notification_sender = User.objects.get(id=list(pk_set)[0])
        notification_receiver = User.objects.get(id = instance.user_id)

        if instance.user != notification_sender:
            if (existing_notifications := Notification.objects.filter( 
                entity_type = Notification.USER_FOLLOW,               
                title = ' started following you.',
                from_user = notification_sender,
                to_user = notification_receiver).all()).exists():
                existing_notifications.delete()

            Notification.objects.create(
                entity_type = Notification.USER_FOLLOW,
                title = ' started following you.',
                from_user = notification_sender,
                to_user = notification_receiver
            )

    elif action == 'post_remove':
        notification_sender = User.objects.get(id=list(pk_set)[0])
        notification_receiver = User.objects.get(id = instance.user_id)

        if (existing_notifications := Notification.objects.filter( 
            entity_type = Notification.USER_FOLLOW,               
            title = ' started following you.',
            from_user = notification_sender,
            to_user = notification_receiver).all()).exists():
            existing_notifications.update(status = False, read_status = True)

@receiver(m2m_changed, sender=Post.likes.through)
def send_notification_on_post_like(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        notification_sender = User.objects.get(id=list(pk_set)[0])
        notification_receiver = User.objects.get(id = instance.user_id)

        if instance.user != notification_sender:
            if (existing_notifications := Notification.objects.filter( 
                entity_id = instance.id,
                entity_type = Notification.POST_LIKE,               
                title = ' liked your post.',
                from_user = notification_sender,
                to_user = notification_receiver)
                .all()).exists():
                existing_notifications.delete()

            Notification.objects.create(
                entity_id = instance.id,
                entity_type = Notification.POST_LIKE,
                title = ' liked your post.',
                from_user = notification_sender,
                to_user = notification_receiver
            )

    elif action == 'post_remove':
        notification_sender = User.objects.get(id=list(pk_set)[0])
        notification_receiver = User.objects.get(id = instance.user_id)

        if (existing_notifications := Notification.objects.filter( 
            entity_id = instance.id,
            entity_type = Notification.POST_LIKE,               
            title = ' liked your post.',
            from_user = notification_sender,
            to_user = notification_receiver)
            .all()).exists():
            existing_notifications.update(status = False, read_status = True)

@receiver(post_save, sender=Comment)
def send_notification_on_post_comment(created, sender, instance, **kwargs):
    if created:
        notification_sender = User.objects.get(id = instance.user_id)
        notification_receiver = User.objects.get(id = instance.post.user_id)

        if instance.user != notification_receiver:
            Notification.objects.create(
                entity_id = instance.id,
                entity_type = Notification.POST_COMMENT,  
                title = ' commented on your post.',
                from_user = notification_sender,
                to_user = notification_receiver
            )

    elif 'status' in kwargs['update_fields']:
        notification_sender = User.objects.get(id = instance.user_id)
        notification_receiver = User.objects.get(id = instance.post.user_id)

        Notification.objects.filter(
            entity_id = instance.id,
            entity_type = Notification.POST_COMMENT,  
            title = ' commented on your post.',
            from_user = notification_sender,
            to_user = notification_receiver
        ).delete()

@receiver(m2m_changed, sender=Comment.likes.through)
def send_notification_on_comment_like(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        notification_sender = User.objects.get(id=list(pk_set)[0])
        notification_receiver = User.objects.get(id = instance.user_id)

        if instance.user != notification_sender:
            if (existing_notifications := Notification.objects.filter( 
                entity_id = instance.id,
                entity_type = Notification.POST_COMMENT_LIKE,               
                title = ' liked your comment.',
                from_user = notification_sender,
                to_user = notification_receiver)
                .all()).exists():
                existing_notifications.delete()

            Notification.objects.create(
                entity_id = instance.id,
                entity_type = Notification.POST_COMMENT_LIKE,
                title = ' liked your comment.',
                from_user = notification_sender,
                to_user = notification_receiver
            )

    elif action == 'post_remove':
        notification_sender = User.objects.get(id=list(pk_set)[0])
        notification_receiver = User.objects.get(id = instance.user_id)

        if (existing_notifications := Notification.objects.filter( 
            entity_id = instance.id,
            entity_type = Notification.POST_COMMENT_LIKE,               
            title = ' liked your comment.',
            from_user = notification_sender,
            to_user = notification_receiver)
            .all()).exists():
            existing_notifications.update(status = False, read_status = True)

@receiver(post_save, sender=Reply)
def send_notification_on_post_comment_reply(created, sender, instance, **kwargs):
    if created:
        notification_sender = User.objects.get(id = instance.user_id)
        notification_receiver = User.objects.get(id = instance.comment.user_id)
        if instance.reply:
            notification_receiver = User.objects.get(id = instance.reply.user_id)

        if instance.user != notification_receiver:
            Notification.objects.create(
                entity_id = instance.id,
                entity_type = Notification.POST_COMMENT_REPLY,  
                title = ' replied to your comment.',
                from_user = notification_sender,
                to_user = notification_receiver
            )

    elif 'status' in kwargs['update_fields']:
        notification_sender = User.objects.get(id = instance.user_id)
        notification_receiver = User.objects.get(id = instance.comment.user_id)
        if instance.reply:
            notification_receiver = User.objects.get(id = instance.reply.user_id)

        Notification.objects.filter(
            entity_id = instance.id,
            entity_type = Notification.POST_COMMENT_REPLY,  
            title = ' replied to your comment.',
            from_user = notification_sender,
            to_user = notification_receiver
        ).delete()   

@receiver(m2m_changed, sender=Reply.likes.through)
def send_notification_on_comment_reply_like(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        notification_sender = User.objects.get(id=list(pk_set)[0])
        notification_receiver = User.objects.get(id = instance.user_id)

        if instance.user != notification_sender:
            if (existing_notifications := Notification.objects.filter( 
                entity_id = instance.id,
                entity_type = Notification.POST_COMMENT_REPLY_LIKE,               
                title = ' liked your reply.',
                from_user = notification_sender,
                to_user = notification_receiver)
                .all()).exists():
                existing_notifications.delete()

            Notification.objects.create(
                entity_id = instance.id,
                entity_type = Notification.POST_COMMENT_REPLY_LIKE,
                title = ' liked your reply.',
                from_user = notification_sender,
                to_user = notification_receiver
            )

    elif action == 'post_remove':
        notification_sender = User.objects.get(id=list(pk_set)[0])
        notification_receiver = User.objects.get(id = instance.user_id)

        if (existing_notifications := Notification.objects.filter( 
            entity_id = instance.id,
            entity_type = Notification.POST_COMMENT_REPLY_LIKE,               
            title = ' liked your reply.',
            from_user = notification_sender,
            to_user = notification_receiver)
            .all()).exists():
            existing_notifications.update(status = False, read_status = True)

@receiver(m2m_changed, sender=Story.likes.through)
def send_notification_on_story_like(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        notification_sender = User.objects.get(id=list(pk_set)[0])
        notification_receiver = User.objects.get(id = instance.user_id)

        if instance.user != notification_sender:
            if (existing_notifications := Notification.objects.filter(     
                entity_id = instance.id,
                entity_type = Notification.STORY_LIKE,
                title = ' liked your story.',
                from_user = notification_sender,
                to_user = notification_receiver)
                .all()).exists():
                existing_notifications.delete()

            Notification.objects.create(
                entity_id = instance.id,
                entity_type = Notification.STORY_LIKE,
                title = ' liked your story.',
                from_user = notification_sender,
                to_user = notification_receiver
            )
    
    elif action == 'post_remove':
        notification_sender = User.objects.get(id=list(pk_set)[0])
        notification_receiver = User.objects.get(id = instance.user_id)

        if (existing_notifications := Notification.objects.filter(     
            entity_id = instance.id,
            entity_type = Notification.STORY_LIKE,
            title = ' liked your story.',
            from_user = notification_sender,
            to_user = notification_receiver)
            .all()).exists():
            existing_notifications.update(status = False, read_status = True)

@receiver(post_save, sender=StoryReply)
def send_notification_on_story_reply(created, sender, instance, **kwargs):
    if created:
        notification_sender = User.objects.get(id=instance.user_id)
        notification_receiver = User.objects.get(id = instance.story.user_id)

        if instance.user != instance.story.user:
            Notification.objects.create(
                entity_id = instance.id,
                entity_type = Notification.STORY_REPLY,  
                title = ' replied to your story.',
                from_user = notification_sender,
                to_user = notification_receiver
            )
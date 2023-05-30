from django.shortcuts import render, redirect
from .models import Notification
from django.core.paginator import Paginator
from .decorators import read_notifications
from django.contrib.auth.decorators import login_required
from commons.decorators import normal_user_only
from post.models import Post, Comment, Reply
from story.models import Story, StoryReply
from django.db.models import Q

# Create your views here.

@login_required
@normal_user_only
@read_notifications
def list(request):
    notifications = Notification.objects.filter(to_user = request.user, status=True)

    category = request.GET.get('category')

    if category == 'all':
        return redirect('notification:list')

    elif category == 'likes':
        notifications = notifications.filter(Q(entity_type = 'POST_LIKE') | 
                        Q(entity_type = 'STORY_LIKE') | Q(entity_type = 'POST_COMMENT_LIKE') | 
                        Q(entity_type = 'POST_COMMENT_LIKE') | Q(entity_type = 'POST_COMMENT_REPLY_LIKE')).all()

    elif category == 'comments':
        notifications = notifications.filter(Q(entity_type = 'POST_COMMENT') | 
                        Q(entity_type = 'POST_COMMENT_REPLY') | 
                        Q(entity_type = 'STORY_REPLY')).all()

    elif category == 'follows':
        notifications = notifications.filter(entity_type = 'USER_FOLLOW').all()

    for noti in notifications:
        if noti.entity_type == 'POST_LIKE':
            noti.post = Post.objects.filter(id = noti.entity_id, status=True).first()
    
        elif noti.entity_type == 'POST_COMMENT' or noti.entity_type == 'POST_COMMENT_LIKE':
            comment = Comment.objects.filter(id = noti.entity_id, status=True).first()
            noti.post = Post.objects.filter(id = comment.post.id, status=True).first()

        elif noti.entity_type == 'POST_COMMENT_REPLY' or noti.entity_type == 'POST_COMMENT_REPLY_LIKE':
            reply = Reply.objects.filter(id = noti.entity_id, status=True).first()
            noti.post = Post.objects.filter(id = reply.comment.post.id, status=True).first()

        elif noti.entity_type == 'STORY_LIKE':
            noti.story = Story.objects.filter(id = noti.entity_id, status=True).first()

        elif noti.entity_type == 'STORY_REPLY':
            story_reply = StoryReply.objects.filter(id = noti.entity_id, status = True).first()
            noti.story = Story.objects.filter(id = story_reply.story.id, status=True).first()
    
    paginator = Paginator(notifications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'notifications':page_obj, 'category':category}
    return render(request, 'notification/list.html', context=context)

def read_notifications(request):
    unread_notifications = Notification.objects.filter(to_user = request.user, status = True, read_status = False).all()
    unread_notifications.update(read_status=True)
    return redirect(request.META.get('HTTP_REFERER'))

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from .models import Inbox, Message
from .forms import MessageForm
from django.db.models import Q, Subquery, OuterRef, Count
from itertools import groupby
from operator import attrgetter
from django.db.models.functions import TruncDate
from .utils import get_inbox
from .decorators import read_messages
from account.models import LoggedUser
from django.http import JsonResponse

# Create your views here.

@login_required
def inbox(request):
    last_message = Message.objects.filter(inbox = OuterRef('pk')).order_by('-created_at')
    unread_messages = Message.objects.filter(~Q(user = request.user), inbox = OuterRef('pk'), status=True, read_status=False).values('inbox').annotate(count = Count('pk')).values('count')
    user_inboxes = request.user.user_inboxes.annotate(
                last_message_sent_at = Subquery(last_message.values('created_at')[:1]),
                unread_message_count = Subquery(unread_messages.values('count')[:1])
                ).order_by('-last_message_sent_at').all()
    context = {'title':'Inbox \u2022 Chats', 'user_inboxes':user_inboxes}
    return render(request, 'chat/chat.html', context=context)

@login_required
@read_messages
def chat(request, slug):
    last_message = Message.objects.filter(inbox = OuterRef('pk')).order_by('-created_at')
    unread_messages = Message.objects.filter(~Q(user = request.user), inbox = OuterRef('pk'), status=True, read_status=False).values('inbox').annotate(count = Count('pk')).values('count')
    user_inboxes = request.user.user_inboxes.annotate(
                last_message_sent_at = Subquery(last_message.values('created_at')[:1]),
                unread_message_count = Subquery(unread_messages.values('count')[:1])
                ).order_by('-last_message_sent_at').all()
    current_inbox = get_object_or_404(Inbox, slug=slug)
    chat_user = get_user_model().objects.filter(id__in = current_inbox.users.all()).exclude(id=request.user.id).first()
    chat_user_active = LoggedUser.objects.filter(user = chat_user).first()
    messages = Message.objects.filter(inbox = current_inbox, status=True).annotate(
                                        created_at_date=TruncDate('created_at'),).order_by('created_at')
    grouped_messages = groupby(messages, attrgetter('created_at_date'))
    context = {'current_inbox':current_inbox, 'user_inboxes':user_inboxes, 'messages':messages,
               'title':'Instagram \u2022 Chats', 'chat':True, 'chat_user':chat_user, 'grouped_messages':grouped_messages, 'chat_user_active':chat_user_active}
    return render(request, 'chat/chat.html', context=context)

@login_required
def send_message(request):
    if request.method == 'POST':
        chat_user_id = request.POST.get('chat_user_id')
        message_body = request.POST.get('body')
        chat_user = get_object_or_404(get_user_model(), id = chat_user_id)
        message_type = request.POST.get('type')
        inbox = get_inbox(request.user, chat_user)
        image = request.FILES.get('image')

        message = Message()
        message.inbox = inbox
        message.user = request.user
        message.body = message_body
        message.type = message_type
        message.image = image
        message.save()

        return redirect(request.META.get('HTTP_REFERER') + '#page-end')
    
@login_required
def new_chat(request):
    if request.method == 'POST':
        username = request.POST.get('user')
        chat_user = get_object_or_404(get_user_model(), username=username)
        inbox = get_inbox(request.user, chat_user)
        return redirect('chat:chat', slug=inbox.slug)
    
@login_required
def get_users(request):
    username = request.GET.get('username')
    users = list(get_user_model().objects.filter(username__icontains=username).values('id', 'username', 'name', 'profile_photo'))
    return JsonResponse(users, safe=False)
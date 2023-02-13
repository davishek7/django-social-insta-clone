from django.shortcuts import render, redirect
from .models import Notification

# Create your views here.

def read_notifications(request):
    unread_notifications = Notification.objects.filter(to_user = request.user, status = True, read_status = False).all()
    unread_notifications.update(read_status=True)
    return redirect(request.META.get('HTTP_REFERER'))

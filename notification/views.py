from django.shortcuts import render, redirect
from .models import Notification
from django.core.paginator import Paginator
from .decorators import read_notifications
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
@read_notifications
def list(request):
    notifications = Notification.objects.filter(to_user = request.user, status=True).all()
    paginator = Paginator(notifications, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {'notifications':page_obj}
    return render(request, 'notification/list.html', context=context)

def read_notifications(request):
    unread_notifications = Notification.objects.filter(to_user = request.user, status = True, read_status = False).all()
    unread_notifications.update(read_status=True)
    return redirect(request.META.get('HTTP_REFERER'))

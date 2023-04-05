from django.contrib import admin
from .models import Notification

# Register your models here.

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['__str__','from_user', 'to_user', 'post', 'read_status',]
    readonly_fields = ['post']


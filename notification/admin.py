from typing import Any, List, Optional, Tuple, Union
from django.contrib import admin
from django.http.request import HttpRequest
from .models import Notification

# Register your models here.

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['__str__','from_user', 'to_user', 'entity_type', 'read_status', 'status']

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('entity_type', 'entity_id', 'to_user', 'from_user',)
        return self.readonly_fields


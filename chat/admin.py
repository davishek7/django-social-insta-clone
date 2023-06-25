from django.contrib import admin
from .models import Inbox, Message

# Register your models here.

class MessageAdmin(admin.TabularInline):
    model = Message

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('user',)
        return self.readonly_fields


@admin.register(Inbox)
class InboxAdmin(admin.ModelAdmin):
    inlines = [MessageAdmin]

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('users', 'slug',)
        return self.readonly_fields
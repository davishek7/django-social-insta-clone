from django.contrib import admin
from .models import Story, StoryReply

# Register your models here.

class StoryReplyAdmin(admin.TabularInline):
    model = StoryReply


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'status', 'like_count', 'view_count', 'reply_count']
    readonly_fields = ['slug', ]
    inlines = [StoryReplyAdmin]

    def like_count(self, obj):
        return obj.likes.count()
    
    def view_count(self, obj):
        return obj.views.count()
    
    def reply_count(self, obj):
        return obj.story_replies.count()
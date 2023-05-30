from django.contrib import admin
from .models import Story, StoryReply

# Register your models here.

class StoryReplyAdmin(admin.TabularInline):
    model = StoryReply

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('user',)
        return self.readonly_fields


@admin.register(Story)
class StoryAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'status', 'like_count', 'view_count', 'reply_count']
    inlines = [StoryReplyAdmin]

    def like_count(self, obj):
        return obj.likes.count()
    
    def view_count(self, obj):
        return obj.views.count()
    
    def reply_count(self, obj):
        return obj.story_replies.count()
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('slug', 'user',)
        return self.readonly_fields
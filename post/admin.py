from django.contrib import admin
from .models import Post, PostImage, Comment, Reply


class PostImageAdmin(admin.TabularInline):
    model = PostImage
    readonly_fields = ['post']


class ReplyAdmin(admin.TabularInline):
    model = Reply

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('reply', 'user',)
        return self.readonly_fields


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'user', 'post', 'body', 'like_count', 'status']
    inlines = [ReplyAdmin]

    def like_count(self, obj):
        return obj.likes.count()

    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('user', 'post',)
        return self.readonly_fields
    

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['caption', 'user', 'status', 'like_count', 'comment_count']
    inlines = [PostImageAdmin]

    def like_count(self, obj):
        return obj.likes.count()

    def comment_count(self, obj):
        return obj.post_comments.all().count()
    
    def get_readonly_fields(self, request, obj=None):
        if obj:
            return self.readonly_fields + ('slug', 'user',)
        return self.readonly_fields
from django.contrib import admin
from .models import Post, PostImage, Comment, Reply


class PostImageAdmin(admin.TabularInline):
    model = PostImage
    readonly_fields = ['post']


class ReplyAdmin(admin.TabularInline):
    model = Reply
    # readonly_fields = ['user']


class CommentAdmin(admin.TabularInline):
    model = Comment
    # readonly_fields = ['user']
    inlines = [ReplyAdmin]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['caption', 'user', 'status', 'like_count', 'comment_count']
    readonly_fields = ['slug', 'user']
    inlines = [PostImageAdmin, CommentAdmin]

    def like_count(self, obj):
        return obj.likes.count()

    def comment_count(self, obj):
        return obj.post_comments.all().count()
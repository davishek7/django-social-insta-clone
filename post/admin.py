from django.contrib import admin
from .models import Post, PostImage, Comment


class PostImageAdmin(admin.TabularInline):
    model=PostImage


class CommentAdmin(admin.TabularInline):
    model = Comment


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['caption', 'user', 'status', 'like_count', 'comment_count']
    readonly_fields = ['slug']
    inlines = [PostImageAdmin, CommentAdmin]

    def like_count(self, obj):
        return obj.likes.count()

    def comment_count(self, obj):
        return obj.post_comments.all().count()
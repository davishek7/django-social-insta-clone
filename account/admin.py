from django.contrib import admin
from .models import User, Profile

# Register your models here.

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'followers_count', 'followings_count', 'bookmarks_count', 'favourites_count']

    def followers_count(self, obj):
        return obj.followers.count()

    def followings_count(self, obj):
        return obj.followings.count()

    def bookmarks_count(self, obj):
        return obj.bookmarks.count()
    
    def favourites_count(self, obj):
        return obj.favourites.count()


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'username', 'profile_photo', 'is_active', 'is_superuser', 'last_login']
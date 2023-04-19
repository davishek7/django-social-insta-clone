from django.contrib import admin
from .models import Highlight

# Register your models here.

@admin.register(Highlight)
class HighlightAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'name', 'user', 'status']
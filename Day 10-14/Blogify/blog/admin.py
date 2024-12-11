from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Post
from .models import User


class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "email", "role", "is_staff", "is_superuser")


class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "updated_at")


admin.site.register(User, CustomUserAdmin)
admin.site.register(Post, PostAdmin)

from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Post
from .models import User

# Custom admin class for User model
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = ("username", "email", "role", "is_staff", "is_superuser")  # Fields displayed in admin list view

# Custom admin class for Post model
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "created_at", "updated_at")  # Fields displayed in admin list view

# Register models with the admin site
admin.site.register(User, CustomUserAdmin)
admin.site.register(Post, PostAdmin)

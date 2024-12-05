from __future__ import annotations

from django.contrib import admin

from .models import Author
from .models import Post

# admin.site.register(Author)
# admin.site.register(Post)


@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "email"]


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ["id", "title", "author"]

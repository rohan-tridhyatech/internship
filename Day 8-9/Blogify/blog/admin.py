from __future__ import annotations

from django.contrib import admin

from .models import Author
from .models import Category
from .models import Post

admin.site.register(Author)
admin.site.register(Post)
admin.site.register(Category)

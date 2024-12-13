from __future__ import annotations 

from django.contrib import admin  
from django.urls import include, path  

urlpatterns = [
    path("admin/", admin.site.urls),  # Admin panel URL
    path("", include("blog.urls")),  # Include URLs from the 'blog' app
]

from __future__ import annotations

from django.apps import AppConfig

# Configuration class for the Blog application
class BlogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField" 
    name = "blog"  

    def ready(self):
        import blog.signals  

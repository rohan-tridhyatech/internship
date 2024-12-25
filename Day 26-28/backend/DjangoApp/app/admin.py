# myapp/admin.py
from django.contrib import admin
from .models import CustomUser

@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'contact') 
    fieldsets = (
        (None, {
            'fields': ('username', 'email', 'password', 'contact')
        }),
    )
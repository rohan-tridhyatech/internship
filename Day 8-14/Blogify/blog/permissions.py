# permissions.py
from rest_framework.permissions import BasePermission

class IsAdminOrAuthorOrReadOnly(BasePermission):
    """
    Custom permission to only allow admins full access,
    authors to edit their own posts, and everyone else read-only access.
    """
    def has_permission(self, request, view):
        # Allow read-only access for all users (GET, HEAD, OPTIONS)
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Allow full access if the user is an admin
        if request.user and request.user.is_staff:
            return True
        
        # Allow authors to edit their own posts
        if request.user and hasattr(request.user, 'author'):
            # Assuming request.user is the author of the post
            if view.kwargs.get('pk') and view.get_object().author == request.user:
                return True
        
        # For other cases, no permission to modify
        return False

    def has_object_permission(self, request, view, obj):
        # Allow read-only access for all users (GET, HEAD, OPTIONS)
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        
        # Allow full access if the user is an admin
        if request.user and request.user.is_staff:
            return True
        
        # Allow authors to edit their own posts
        if request.user == obj.author:
            return True
        
        return False

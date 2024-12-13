from __future__ import annotations

from rest_framework.permissions import BasePermission
from rest_framework.permissions import SAFE_METHODS

# Custom permission to grant different access based on user role
class UserRolePermission(BasePermission):
    """
    Custom permission to grant different access based on user role.
    """

    def has_permission(self, request, view):
        user = request.user

        # Allow unauthenticated users only for POST requests
        if not user.is_authenticated:
            return request.method == "POST"

        # Check role-based permissions
        if user.role == "admin":
            return True  # Admin has all access (CRUD)

        elif user.role == "author":
            return request.method in ["POST"]  # Author has only POST access

        elif user.role == "user":
            # Regular User has only POST access
            return request.method in ["POST"]

        return False  # Default deny access

# Custom permission for handling post actions
class PostRolePermission(BasePermission):
    """
    Custom permission for handling post actions.
    - Admin can perform all actions.
    - Author can edit, delete, or create own posts.
    - User can GET only.
    - Unauthorized can GET only.
    """

    def has_permission(self, request, view):
        user = request.user

        # Allow read-only access for unauthenticated users
        if not user.is_authenticated:
            return request.method == "GET"

        # If the request method is safe (e.g., GET), allow access
        if request.method in SAFE_METHODS:
            return True

        # If the user is Admin, allow all actions
        if user.role == "admin":
            return True

        # If the user is Author, allow editing, deleting, and creating posts
        if user.role == "author":
            if request.method == "POST":
                return True
            else:
                post = view.get_object()
                return post.author == user

        # If the user is a regular user, only allow GET
        return user.role == "user" and request.method == "GET"

    def has_object_permission(self, request, view, obj):
        # Allow GET operations for all users and unauthorized users
        if request.method in SAFE_METHODS:
            return True

        # For unsafe methods, check if the user is the author of the post
        user = request.user
        if user.is_authenticated:
            return obj.author == user or user.role == "admin"

        return False

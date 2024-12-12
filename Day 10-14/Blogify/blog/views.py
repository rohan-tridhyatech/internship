from __future__ import annotations

from django.core.cache import cache
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle
from rest_framework.throttling import UserRateThrottle

from .models import Post
from .models import User
from .permissions import PostRolePermission
from .permissions import UserRolePermission
from .serializers import PostSerializer
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model.
    Throttling and permissions are applied based on user roles.
    """

    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserRolePermission]  # Role-based permissions
    throttle_classes = [UserRateThrottle, AnonRateThrottle]  # Role-based throttling


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Post model.
    Throttling and permissions are applied based on user roles.
    """

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostRolePermission]  # Role-based permissions
    # Post-specific role-based throttling
    throttle_classes = [UserRateThrottle, AnonRateThrottle]
    lookup_field = "pk"

    # def perform_create(self, serializer):
    #     """Set the author of the post to the current user."""
    #     serializer.save(author=self.request.user)

    def list(self, request, *args, **kwargs):
        cache_key = "post_list_view"
        cached_posts = cache.get(cache_key)

        if cached_posts is not None:
            return Response(cached_posts)

        posts = super().list(request, *args, **kwargs)
        cache.set(cache_key, posts.data, timeout=600)  # Cache for 1 hour

        return posts

    @action(detail=False, methods=["get"], url_path="by-author/(?P<author_id>[^/.]+)")
    def get_posts_by_author(self, request, author_id=None):
        """
        Fetch all posts by a particular author.
        """
        posts = Post.objects.filter(author_id=author_id)
        if not posts.exists():
            return Response(
                {"detail": "No posts found for the specified author."},
                status=status.HTTP_404_NOT_FOUND,
            )
        serializer = self.get_serializer(posts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

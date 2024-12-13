from __future__ import annotations  

from django.core.cache import cache  
from rest_framework import status 
from rest_framework import viewsets  
from rest_framework.decorators import action  
from rest_framework.response import Response  
from rest_framework.exceptions import ValidationError  

from .models import Post, User 
from .permissions import PostRolePermission, UserRolePermission  
from .serializers import PostSerializer, UserSerializer 

class UserViewSet(viewsets.ModelViewSet):
    """
    ViewSet for User model.
    Handles CRUD operations for users.
    Throttling and permissions are applied based on user roles.
    """

    queryset = User.objects.all()  
    serializer_class = UserSerializer  
    permission_classes = [UserRolePermission] 

class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Post model.
    Handles CRUD operations for posts.
    Throttling and permissions are applied based on user roles.
    """

    queryset = Post.objects.all() 
    serializer_class = PostSerializer  
    permission_classes = [PostRolePermission]  
    lookup_field = "pk" 

    def perform_create(self, serializer):
        """
        Ensure that the author has the role of 'author' before creating a post.
        """
        author = serializer.validated_data['author']
        if author.role != "author": 
            raise ValidationError({"detail": "Only users with the 'author' role can create posts."})
        serializer.save()  

    def list(self, request, *args, **kwargs):
        cache_key = "post_list_view"  
        cached_posts = cache.get(cache_key) 

        if cached_posts is not None:
            return Response(cached_posts)  

        posts = super().list(request, *args, **kwargs)  
        cache.set(cache_key, posts.data, timeout=3600)  

        return posts  # Return posts

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
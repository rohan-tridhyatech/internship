from __future__ import annotations

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.response import Response
# from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.authentication import SessionAuthentication
from .permissions import IsAdminOrAuthorOrReadOnly

from .models import *
from .serializers import *

# ViewSet for Author model


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    # authentication_classes = [JWTAuthentication]
    authentication_classes = [SessionAuthentication]
    permission_classes = [IsAdminOrAuthorOrReadOnly]

# ViewSet for Post model


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return PostReadSerializer  # For read operations
        return PostCreateSerializer  # For create/update operations



@api_view(["GET"])
def get_posts_by_author(request, author_id):
    """
    Retrieve all posts by a specific author.
    This will return all blog posts written by the author identified by `author_id`.
    """
    try:
        # Fetch the author by their ID
        author = Author.objects.get(pk=author_id)
    except Author.DoesNotExist:
        # Handle invalid author ID
        return Response({"status": 404, "message": "Author not found"},status=status.HTTP_404_NOT_FOUND)

    # Fetch posts by the author using the foreign key relationship
    # Filter posts that belong to this author
    posts = Post.objects.filter(author=author)
    # Serialize the list of posts
    serializer = PostReadSerializer(posts, many=True)

    # Return the serialized posts
    return Response({"Data": serializer.data})



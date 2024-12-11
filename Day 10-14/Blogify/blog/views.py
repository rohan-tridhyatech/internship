from __future__ import annotations

from rest_framework import viewsets

from .models import Post
from .models import User
from .permissions import PostRolePermission
from .permissions import UserRolePermission
from .serializers import PostSerializer
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [UserRolePermission]


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [PostRolePermission]
    lookup_field = "pk"

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

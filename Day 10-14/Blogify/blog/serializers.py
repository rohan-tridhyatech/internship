from __future__ import annotations

from rest_framework import serializers

from .models import Post
from .models import User


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "password"]


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
    )

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author", "created_at", "updated_at"]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["formatted_created_at"] = instance.created_at.strftime(
            "%Y-%m-%d %H:%M:%S"
        )
        return representation

from __future__ import annotations

from rest_framework import serializers

from .models import Post
from .models import User

# Serializer for the User model
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)  # Write-only field for password

    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "password"] 

# Serializer for the Post model
class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),  # Restrict author field to valid User instances
    )

    class Meta:
        model = Post
        fields = ["id", "title", "content", "author","sentiment"] 

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation["created_at"] = instance.created_at.strftime("%Y-%m-%d %H:%M:%S") 
        representation["updated_at"] = instance.updated_at.strftime("%Y-%m-%d %H:%M:%S") 
        return representation

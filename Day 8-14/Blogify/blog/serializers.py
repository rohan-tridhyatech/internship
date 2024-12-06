from rest_framework import serializers

from .models import Author
from .models import Post


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        # fields = ['name', 'email']
        exclude = ["id"]
        # fields = "__all__"

    def validate(self, data):
        if "name" in data:
            for char in data["name"]:
                if char != " ":
                    if not char.isalpha():  # Checking if all characters are alphabetic
                        raise serializers.ValidationError(
                            {"Error": "Name can only contain alphabetic characters."},
                        )
        return data


class PostReadSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Post
        fields = ["title", "content", "timestamp", "author"]


class PostCreateSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(queryset=Author.objects.all())

    class Meta:
        model = Post
        fields = ["title", "content", "timestamp", "author"]

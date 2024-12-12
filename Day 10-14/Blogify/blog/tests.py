from __future__ import annotations

from django.test import Client
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import Post
from .models import User
from .serializers import PostSerializer
from .serializers import UserSerializer


class UserModelTest(TestCase):
    def test_user_creation(self):
        user = User.objects.create(
            username="user", email="user@example.com", role="user"
        )
        admin = User.objects.create(
            username="admin", email="admin@example.com", role="admin"
        )
        author1 = User.objects.create(
            username="author1", email="author1@example.com", role="author"
        )
        author2 = User.objects.create(
            username="author2", email="author2@example.com", role="author"
        )
        self.assertEqual(user.username, "user")
        self.assertEqual(user.email, "user@example.com")
        self.assertEqual(user.role, "user")


class PostModelTest(TestCase):
    def test_post_creation(self):
        user = User.objects.create(
            username="testauthor", email="author@example.com", role="author"
        )
        post = Post.objects.create(
            title="Test Post", content="Content of the test post", author=user
        )
        self.assertEqual(post.title, "Test Post")
        self.assertEqual(post.content, "Content of the test post")
        self.assertEqual(post.author, user)


class UserSerializerTest(APITestCase):
    def test_user_serializer(self):
        user = User(
            username="testuser", email="test@example.com", password="password123"
        )
        serializer = UserSerializer(user)
        data = serializer.data
        self.assertEqual(data["username"], "testuser")
        self.assertEqual(data["email"], "test@example.com")


class PostSerializerTest(APITestCase):
    def test_post_serializer(self):
        user = User.objects.create(
            username="testauthor", email="author@example.com", role="author"
        )
        post = Post.objects.create(
            title="Test Post", content="Content of the test post", author=user
        )
        serializer = PostSerializer(post)
        data = serializer.data
        self.assertEqual(data["title"], "Test Post")
        self.assertEqual(data["content"], "Content of the test post")
        self.assertEqual(data["author"], user.id)


class APIUserTests(APITestCase):
    def test_create_user(self):
        data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "password123",
        }
        response = self.client.post("/api/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)

    def test_login_user(self):
        user = User.objects.create_user(
            username="testuser", email="test@example.com", password="password123"
        )
        response = self.client.post(
            "/api/token/", {"username": "testuser", "password": "password123"}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)

    def test_create_post_with_authorization(self):
        user = User.objects.create_user(username="testauthor", password="password123")
        self.client.force_authenticate(user=user)
        data = {
            "title": "Test Post",
            "content": "Content of test post",
            "author": user.id,
        }
        response = self.client.post("/api/posts/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_post_permission(self):
        user = User.objects.create_user(username="testauthor", password="password123")
        post = Post.objects.create(
            title="Test Post", content="Content of the test post", author=user
        )

        # Test GET by unauthenticated user
        response = self.client.get(f"/api/posts/{post.id}/")
        # User is unauthorized
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

        # Authenticate as the author
        self.client.force_authenticate(user=user)
        response = self.client.get(f"/api/posts/{post.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class APITokenTests(APITestCase):
    def test_refresh_token(self):
        user = User.objects.create_user(username="testuser", password="password123")
        response = self.client.post(
            "/api/token/", {"username": "testuser", "password": "password123"}
        )
        refresh_token = response.data["refresh"]

        response = self.client.post("/api/token/refresh/", {"refresh": refresh_token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_token(self):
        user = User.objects.create_user(username="testuser", password="password123")
        response = self.client.post(
            "/api/token/", {"username": "testuser", "password": "password123"}
        )
        token = response.data["access"]

        response = self.client.post("/api/token/verify/", {"token": token})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

from __future__ import annotations

from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Post
from .models import User
from .serializers import PostSerializer
from .serializers import UserSerializer


# User Model
class UserModelTest(TestCase):
    def test_user_creation(self):
        # Creating different users with varying roles
        user = User.objects.create(username="user", email="user@example.com", role="user")
        admin = User.objects.create(username="admin", email="admin@example.com", role="admin")
        author1 = User.objects.create(username="author1", email="author1@example.com", role="author")
        author2 = User.objects.create(username="author2", email="author2@example.com", role="author")
        
        # Testing if the created users have the correct attributes
        self.assertEqual(user.username, "user")
        self.assertEqual(user.email, "user@example.com")
        self.assertEqual(user.role, "user")
        
        self.assertEqual(admin.username, "admin")
        self.assertEqual(admin.email, "admin@example.com")
        self.assertEqual(admin.role, "admin")
        
        self.assertEqual(author1.username, "author1")
        self.assertEqual(author1.email, "author1@example.com")
        self.assertEqual(author1.role, "author")
        
        self.assertEqual(author2.username, "author2")
        self.assertEqual(author2.email, "author2@example.com")
        self.assertEqual(author2.role, "author")

# Post Model
class PostModelTest(TestCase):
    def test_multiple_post_creation(self):
        # Creating authors
        author1 = User.objects.create(username="author1", email="author1@example.com", role="author")
        author2 = User.objects.create(username="author2", email="author2@example.com", role="author")
        
        # Creating posts for different authors
        post1 = Post.objects.create(title="Test Post by Author1", content="Content of the test post by author1", author=author1)
        post2 = Post.objects.create(title="Test Post by Author2", content="Content of the test post by author2", author=author2)
        
        # Assertions to verify the created posts
        self.assertEqual(post1.title, "Test Post by Author1")
        self.assertEqual(post1.content, "Content of the test post by author1")
        self.assertEqual(post1.author, author1)
        
        self.assertEqual(post2.title, "Test Post by Author2")
        self.assertEqual(post2.content, "Content of the test post by author2")
        self.assertEqual(post2.author, author2)

# User Serializer
class UserSerializerTest(APITestCase):
    def test_user_serializer(self):
        # Creating a User instance
        user = User(username="user", email="user@example.com", password="user")
        serializer = UserSerializer(user)
        data = serializer.data
        
        self.assertEqual(data["username"], "user")
        self.assertEqual(data["email"], "user@example.com")

# Post Serializer
class PostSerializerTest(APITestCase):
    def test_post_serializer(self):
        # Creating a User instance
        user = User.objects.create(username="author", email="author@example.com", role="author")
        # Creating a Post instance
        post = Post.objects.create(title="Test Post", content="Content of the test post", author=user)
        serializer = PostSerializer(post)
        data = serializer.data
        # Assertions to verify serialized data
        self.assertEqual(data["title"], "Test Post")
        self.assertEqual(data["content"], "Content of the test post")
        self.assertEqual(data["author"], user.id)

# Model : Users, Role : Admin
class UserAdminTest(APITestCase):

    def setUp(self):
        self.admin = User.objects.create(username="admin", email="admin@example.com", role="admin")
        self.user = User.objects.create(username="user", email="user@example.com", role="user")
        self.refresh = RefreshToken.for_user(self.admin)
        self.access_token = str(self.refresh.access_token)

    def test_create_user_as_admin(self):
        url = '/api/users/'
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
            "role": "admin"
        }

        self.client.force_authenticate(user=self.admin, token=self.access_token)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 3)
        self.assertEqual(User.objects.get(username="newuser").email, "newuser@example.com")

    def test_retrieve_user_as_admin(self):
        url = '/api/users/'

        self.client.force_authenticate(user=self.admin, token=self.access_token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)

    def test_update_user_as_admin(self):
        url = f'/api/users/{self.user.id}/'
        data = {"email": "updatedemail@example.com"}

        self.client.force_authenticate(user=self.admin, token=self.access_token)
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "updatedemail@example.com")

    def test_delete_user_as_admin(self):
        url = f'/api/users/{self.user.id}/'

        self.client.force_authenticate(user=self.admin, token=self.access_token)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(User.objects.count(), 1)

# Model : Posts, Role : Admin
class PostAdminTest(APITestCase):

    def setUp(self):
        self.admin = User.objects.create(username="admin", email="admin@example.com", role="admin")
        self.author = User.objects.create(username="author", email="author@example.com", role="author")
        self.refresh = RefreshToken.for_user(self.admin)
        self.access_token = str(self.refresh.access_token)

    def test_create_post_as_admin(self):
        url = '/api/posts/'
        data = {
            "title": "Test Post",
            "content": "Content of the test post",
            "author": self.author.id
        }

        self.client.force_authenticate(user=self.admin, token=self.access_token)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get(title="Test Post").content, "Content of the test post")

    def test_retrieve_post_as_admin(self):
        post = Post.objects.create(title="Test Post", content="Content of the test post", author=self.author)
        
        url = f'/api/posts/{post.id}/'
        
        self.client.force_authenticate(user=self.admin, token=self.access_token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Test Post")

    def test_update_post_as_admin(self):
        post = Post.objects.create(title="Test Post", content="Content of the test post", author=self.author)
        
        url = f'/api/posts/{post.id}/'
        data = {"content": "Updated content"}

        self.client.force_authenticate(user=self.admin, token=self.access_token)
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.content, "Updated content")

    def test_delete_post_as_admin(self):
        post = Post.objects.create(title="Test Post", content="Content of the test post", author=self.author)
        
        url = f'/api/posts/{post.id}/'

        self.client.force_authenticate(user=self.admin, token=self.access_token)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

# Model : Users, Role : Author
class UserAuthorTest(APITestCase):

    def setUp(self):
        self.author = User.objects.create(username="author", email="author@example.com", role="author")
        self.refresh = RefreshToken.for_user(self.author)
        self.access_token = str(self.refresh.access_token)

    def test_create_user_as_author(self):
        url = '/api/users/'
        data = {
            "username": "newauthor",
            "email": "newauthor@example.com",
            "password": "password123",
            "role": "author"
        }

        self.client.force_authenticate(user=self.author, token=self.access_token)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_retrieve_user_as_author(self):
        url = '/api/users/'

        self.client.force_authenticate(user=self.author, token=self.access_token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_as_author(self):
        url = f'/api/users/{self.author.id}/'
        data = {"email": "updatedauthor@example.com"}

        self.client.force_authenticate(user=self.author, token=self.access_token)
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.author.refresh_from_db()
        self.assertEqual(self.author.email, "author@example.com")

    def test_delete_user_as_author(self):
        url = f'/api/users/{self.author.id}/'

        self.client.force_authenticate(user=self.author, token=self.access_token)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 1)

# Model : Posts, Role : Author
class PostAuthorTest(APITestCase):

    def setUp(self):
        self.author = User.objects.create(username="author", email="author@example.com", role="author")
        self.other_author = User.objects.create(username="otherauthor", email="otherauthor@example.com", role="author")
        self.refresh = RefreshToken.for_user(self.author)
        self.access_token = str(self.refresh.access_token)

    def test_create_post_as_author(self):
        url = '/api/posts/'
        data = {
            "title": "Author Post",
            "content": "This is a post by an author",
            "author": self.author.id
        }

        self.client.force_authenticate(user=self.author, token=self.access_token)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        self.assertEqual(Post.objects.get(title="Author Post").content, "This is a post by an author")

    def test_retrieve_post_as_author(self):
        post = Post.objects.create(title="Author Post", content="Content of author's post", author=self.author)
        url = f'/api/posts/{post.id}/'

        self.client.force_authenticate(user=self.author, token=self.access_token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Author Post")

    def test_update_post_as_author(self):
        post = Post.objects.create(title="Author Post", content="Content of author's post", author=self.author)
        url = f'/api/posts/{post.id}/'
        data = {"content": "Updated content for own post"}

        self.client.force_authenticate(user=self.author, token=self.access_token)
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        post.refresh_from_db()
        self.assertEqual(post.content, "Updated content for own post")

        # Attempt to update other's post
        self.client.force_authenticate(user=self.other_author, token=self.access_token)
        response_other = self.client.patch(url, data)
        self.assertEqual(response_other.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_post_as_author(self):
        post = Post.objects.create(title="Author Post", content="Content of author's post", author=self.author)

        # Attempt to delete other's post
        self.client.force_authenticate(user=self.other_author, token=self.access_token)
        url_other = f'/api/posts/{post.id}/'
        response_other = self.client.delete(url_other)
        self.assertEqual(response_other.status_code, status.HTTP_403_FORBIDDEN)

        # Attempt to delete own post
        self.client.force_authenticate(user=self.author, token=self.access_token)
        url = f'/api/posts/{post.id}/'
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Post.objects.count(), 0)

# Model : Users, Role : User
class UserTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username="user", email="user@example.com", role="user")
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

    def test_create_user_as_user(self):
        url = '/api/users/'
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
            "role": "user"
        }

        self.client.force_authenticate(user=self.user, token=self.access_token)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 2)

    def test_retrieve_user_as_user(self):
        url = '/api/users/'

        self.client.force_authenticate(user=self.user, token=self.access_token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_update_user_as_user(self):
        url = f'/api/users/{self.user.id}/'
        data = {"email": "updateduser@example.com"}

        self.client.force_authenticate(user=self.user, token=self.access_token)
        response = self.client.put(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.user.refresh_from_db()
        self.assertEqual(self.user.email, "user@example.com")

    def test_delete_user_as_user(self):
        url = f'/api/users/{self.user.id}/'

        self.client.force_authenticate(user=self.user, token=self.access_token)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(User.objects.count(), 1)

# Model : Posts, Role : User
class PostTest(APITestCase):

    def setUp(self):
        self.user = User.objects.create(username="user", email="user@example.com", role="user")
        self.author = User.objects.create(username="author", email="author@example.com", role="author")
        self.post = Post.objects.create(title="Author Post", content="Content of author's post", author=self.author)
        self.refresh = RefreshToken.for_user(self.user)
        self.access_token = str(self.refresh.access_token)

    def test_create_post_as_user(self):
        url = '/api/posts/'
        data = {
            "title": "User Post",
            "content": "This is a post by a user",
            "author": self.user.id
        }

        self.client.force_authenticate(user=self.user, token=self.access_token)
        response = self.client.post(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)

    def test_retrieve_post_as_user(self):
        url = f'/api/posts/{self.post.id}/'

        self.client.force_authenticate(user=self.user, token=self.access_token)
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Author Post")

    def test_update_post_as_user(self):
        url = f'/api/posts/{self.post.id}/'
        data = {"content": "Updated content for own post"}

        self.client.force_authenticate(user=self.user, token=self.access_token)
        response = self.client.patch(url, data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(self.post.content, "Content of author's post")

    def test_delete_post_as_user(self):
        url = f'/api/posts/{self.post.id}/'

        self.client.force_authenticate(user=self.user, token=self.access_token)
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.count(), 1)

# Model : Users, Role : Unauthorized
class UserUnauthorizedTest(APITestCase):

    def test_create_user_unauthorized(self):
        url = '/api/users/'
        data = {
            "username": "newuser",
            "email": "newuser@example.com",
            "password": "password123",
            "role": "user"
        }
        
        response = self.client.post(url, data)
        
        # Assuming user creation is allowed for unauthenticated users
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get(username="newuser").email, "newuser@example.com")

    def test_retrieve_users_unauthorized(self):
        User.objects.create(username="user", email="user@example.com", role="user")
        User.objects.create(username="author", email="author@example.com", role="author")
        
        url = '/api/users/'
        
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_unauthorized(self):
        user = User.objects.create(username="user", email="user@example.com", role="user")
        url = f'/api/users/{user.id}/'
        data = {"email": "updateduser@example.com"}
        
        response = self.client.put(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        user.refresh_from_db()
        self.assertEqual(user.email, "user@example.com")

    def test_delete_user_unauthorized(self):
        user = User.objects.create(username="user", email="user@example.com", role="user")
        url = f'/api/users/{user.id}/'
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(User.objects.count(), 1)

# Model : Posts, Role : Unauthorized
class PostUnauthorizedTest(APITestCase):

    def test_create_post_unauthorized(self):
        url = '/api/posts/'
        data = {
            "title": "Unauthorized Post",
            "content": "This is a post without JWT token",
            "author": 1
        }
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 0)

    def test_retrieve_post_unauthorized(self):
        author = User.objects.create(username="author", email="author@example.com", role="author")
        post = Post.objects.create(title="Unauthorized Post", content="Content of unauthorized post", author=author)
        
        url = f'/api/posts/{post.id}/'
        response = self.client.get(url)
        
        # Expect 401 unless public access is explicitly allowed
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_post_unauthorized(self):
        author = User.objects.create(username="author", email="author@example.com", role="author")
        post = Post.objects.create(title="Unauthorized Post", content="Content of unauthorized post", author=author)
        
        url = f'/api/posts/{post.id}/'
        data = {"content": "Updated content for unauthorized post"}
        
        response = self.client.patch(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        post.refresh_from_db()
        self.assertEqual(post.content, "Content of unauthorized post")

    def test_delete_post_unauthorized(self):
        author = User.objects.create(username="author", email="author@example.com", role="author")
        post = Post.objects.create(title="Unauthorized Post", content="Content of unauthorized post", author=author)
        
        url = f'/api/posts/{post.id}/'
        
        response = self.client.delete(url)
        
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Post.objects.count(), 1)





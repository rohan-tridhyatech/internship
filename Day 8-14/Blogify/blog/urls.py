from __future__ import annotations

from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from .views import *
from .views import AuthorViewSet
from .views import PostViewSet

router = DefaultRouter()
router.register(r"authors", AuthorViewSet)
router.register(r"posts", PostViewSet)

# Core CRUD Operations for Author
# 1. GET /api/authors/ → List all authors
# 2. GET /api/authors/{id}/ → Retrieve a single author by ID
# 3. POST /api/authors/ → Create a new author
# 4. PUT /api/authors/{id}/ → Update an author
# 5. DELETE /api/authors/{id}/ → Delete an author

# Core CRUD Operations for Post
# 6. GET /api/posts/ → List all posts
# 7. GET /api/posts/{id}/ → Retrieve a single post by ID
# 8. POST /api/posts/ → Create a new post
# 9. PUT /api/posts/{id}/ → Update a post
# 10. DELETE /api/posts/{id}/ → Delete a post

# Custom API for Posts by Author
# 11. GET /api/posts/by-author/{author_id}/ → Get all posts by a specific author

urlpatterns = [
    path("api/", include(router.urls)),  # Register the router URLs
    path(
        "api/posts/by-author/<int:author_id>/",
        get_posts_by_author,
        name="get_posts_by_author",
    ),
]

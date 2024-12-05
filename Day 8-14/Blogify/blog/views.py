from __future__ import annotations

from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import *
from .serializers import *

# ViewSet for Author model


class AuthorViewSet(viewsets.ModelViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer


# ViewSet for Post model


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostReadSerializer


# AUTHOR APIs


@api_view(["GET"])
def read_author(request):
    """
    Retrieve all authors.
    """
    authors = Author.objects.all()  # Fetch all authors
    # Serialize list of authors
    serializer = AuthorSerializer(authors, many=True)
    # Return serialized data
    return Response({"status": 200, "payload": serializer.data})


@api_view(["GET"])
def get_author_by_id(request, pk):
    """
    Retrieve a single author by their ID.
    """
    try:
        # author = Author.objects.get(pk=pk)  # Fetch author by ID
        author = Author.objects.filter(pk=pk).first()
    except Author.DoesNotExist:
        # Handle invalid ID
        return Response(
            {"status": 404, "message": "Author not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    serializer = AuthorSerializer(author)  # Serialize the author
    # Return serialized data
    return Response(
        {"status": 200, "payload": serializer.data}, status=status.HTTP_200_OK
    )


@api_view(["POST"])
def create_author(request):
    """
    Create a new author.
    """
    serializer = AuthorSerializer(data=request.data)  # Deserialize input data
    if not serializer.is_valid():
        return Response(
            {
                "status": 403,
                "error": serializer.errors,
                "message": "Invalid data",
            },
        )  # Handle validation errors

    serializer.save()  # Save the new author
    return Response(
        {
            "status": 200,
            "payload": serializer.data,
            "message": "Author created successfully",
        },
    )


@api_view(["PUT"])
def update_author(request, pk):
    """
    Update an existing author by ID.
    """
    try:
        author = Author.objects.get(pk=pk)  # Fetch author by ID
    except Author.DoesNotExist:
        # Handle invalid ID
        return Response({"status": 404, "message": "Author not found"})

    serializer = AuthorSerializer(
        instance=author,
        data=request.data,
        partial=True,
    )  # Deserialize input data
    if not serializer.is_valid():
        return Response(
            {
                "status": 403,
                "error": serializer.errors,
                "message": "Invalid data",
            },
        )  # Handle validation errors

    serializer.save()  # Save updated author
    return Response(
        {
            "status": 200,
            "payload": serializer.data,
            "message": "Author updated successfully",
        },
    )


@api_view(["DELETE"])
def delete_author(request, pk):
    """
    Delete an author by ID.
    """
    try:
        author = Author.objects.get(pk=pk)  # Fetch author by ID
    except Author.DoesNotExist:
        # Handle invalid ID
        return Response({"status": 404, "message": "Author not found"})

    author.delete()  # Delete the author
    return Response({"status": 200, "message": "Author deleted successfully"})


# POST APIs
@api_view(["GET"])
def read_posts(request):
    """
    Retrieve all posts.
    """
    posts = Post.objects.select_related(
        "author",
    ).all()  # Fetch posts with related authors
    serializer = PostReadSerializer(posts, many=True)  # Serialize list of posts
    # Return serialized data
    return Response({"status": 200, "payload": serializer.data})


@api_view(["GET"])
def get_post_by_id(request, pk):
    """
    Retrieve a single post by its ID.
    """
    try:
        post = Post.objects.select_related("author").get(pk=pk)  # Fetch post by ID
    except Post.DoesNotExist:
        # Handle invalid ID
        return Response({"status": 404, "message": "Post not found"})

    serializer = PostReadSerializer(post)  # Serialize the post
    # Return serialized data
    return Response({"status": 200, "payload": serializer.data})


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
        return Response({"status": 404, "message": "Author not found"})

    # Fetch posts by the author using the foreign key relationship
    # Filter posts that belong to this author
    posts = Post.objects.filter(author=author)
    # Serialize the list of posts
    serializer = PostReadSerializer(posts, many=True)

    # Return the serialized posts
    return Response({"status": 200, "payload": serializer.data})


@api_view(["POST"])
def create_post(request):
    """
    Create a new post.
    """
    serializer = PostCreateSerializer(data=request.data)  # Deserialize input data
    if not serializer.is_valid():
        return Response(
            {
                "status": 403,
                "error": serializer.errors,
                "message": "Invalid data",
            },
        )  # Handle validation errors

    serializer.save()  # Save the new post
    return Response(
        {
            "status": 200,
            "payload": serializer.data,
            "message": "Post created successfully",
        },
    )


@api_view(["PUT"])
def update_post(request, pk):
    """
    Update an existing post by ID.
    """
    try:
        post = Post.objects.get(pk=pk)  # Fetch post by ID
    except Post.DoesNotExist:
        # Handle invalid ID
        return Response({"status": 404, "message": "Post not found"})

    serializer = PostCreateSerializer(
        instance=post,
        data=request.data,
        partial=True,
    )  # Deserialize input data
    if not serializer.is_valid():
        return Response(
            {
                "status": 403,
                "error": serializer.errors,
                "message": "Invalid data",
            },
        )  # Handle validation errors

    serializer.save()  # Save updated post
    return Response(
        {
            "status": 200,
            "payload": serializer.data,
            "message": "Post updated successfully",
        },
    )


@api_view(["DELETE"])
def delete_post(request, pk):
    """
    Delete a post by ID.
    """
    try:
        post = Post.objects.get(pk=pk)  # Fetch post by ID
    except Post.DoesNotExist:
        # Handle invalid ID
        return Response({"status": 404, "message": "Post not found"})

    post.delete()  # Delete the post
    return Response({"status": 200, "message": "Post deleted successfully"})

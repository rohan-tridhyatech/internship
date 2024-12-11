from __future__ import annotations

import json

from django.http import HttpResponse
from django.http import JsonResponse
from django.shortcuts import get_object_or_404

from .models import Author
from .models import Category
from .models import Post

# Utility to parse JSON request body


def parse_request_body(request):
    try:
        return json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return {}


# CRUD for Author


def author_list(request):
    if request.method == "GET":
        authors = Author.objects.all()
        data = [{"name": author.name, "email": author.email} for author in authors]
        return JsonResponse(data, safe=False)

    if request.method == "POST":
        data = parse_request_body(request)
        author = Author.objects.create(name=data.get("name"), email=data.get("email"))
        return JsonResponse({"name": author.name, "email": author.email}, status=201)


def author_detail(request, author_id):
    author = get_object_or_404(Author, id=author_id)

    if request.method == "GET":
        return JsonResponse({"name": author.name, "email": author.email})

    if request.method == "PUT":
        data = parse_request_body(request)
        author.name = data.get("name", author.name)
        author.email = data.get("email", author.email)
        author.save()
        return JsonResponse({"name": author.name, "email": author.email})

    if request.method == "DELETE":
        author.delete()
        return HttpResponse(status=204)


# CRUD for Post


def post_list(request):
    if request.method == "GET":
        posts = (
            Post.objects.select_related("author").prefetch_related("categories").all()
        )
        data = [
            {
                "title": post.title,
                "content": post.content,
                "author": {"name": post.author.name},
                "categories": [
                    {"id": category.id, "name": category.name}
                    for category in post.categories.all()
                ],
                "created_at": post.created_at.isoformat(),
            }
            for post in posts
        ]
        return JsonResponse(data, safe=False)

    if request.method == "POST":
        data = parse_request_body(request)
        author = get_object_or_404(Author, id=data.get("author_id"))
        post = Post.objects.create(
            title=data.get("title"),
            content=data.get("content"),
            author=author,
        )
        if "category_ids" in data:
            post.categories.set(Category.objects.filter(id__in=data["category_ids"]))
        return JsonResponse({"title": post.title}, status=201)


def post_detail(request, post_id):
    post = get_object_or_404(
        Post.objects.select_related("author").prefetch_related("categories"),
        id=post_id,
    )

    if request.method == "GET":
        data = {
            "title": post.title,
            "content": post.content,
            "author": {"name": post.author.name},
            "categories": [
                {"id": category.id, "name": category.name}
                for category in post.categories.all()
            ],
            "created_at": post.created_at.isoformat(),
        }
        return JsonResponse(data)

    if request.method == "PUT":
        data = parse_request_body(request)
        post.title = data.get("title", post.title)
        post.content = data.get("content", post.content)
        post.save()
        if "category_ids" in data:
            post.categories.set(Category.objects.filter(id__in=data["category_ids"]))
        return JsonResponse({"title": post.title})

    if request.method == "DELETE":
        post.delete()
        return HttpResponse(status=204)

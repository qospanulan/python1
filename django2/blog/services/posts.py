from django.db.models import QuerySet, Q
from django.http import QueryDict
from django.shortcuts import get_object_or_404  # noqa
from rest_framework import exceptions

from blog.filters import PostFilter
from blog.models import Post


class PostService:
    @staticmethod
    def get_all_posts(request_params: QueryDict) -> QuerySet[Post]:

        posts = Post.objects.select_related('author')  # noqa

        if request_params:
            posts = PostFilter(request_params, posts).qs

        search_text = request_params.get('search', None)
        if search_text:
            posts = posts.filter(
                Q(title__icontains=search_text) |
                Q(content__icontains=search_text)
            )

        ordering = request_params.get('ordering', '-created_at')
        if ordering:
            posts = posts.order_by(ordering)

        return posts

    @staticmethod
    def create_post(*, author_id: int, data: dict) -> Post:
        data['author_id'] = author_id
        post = Post(**data)
        post.save()

        return post

    @staticmethod
    def get_post_by_id(*, post_id: int) -> Post:

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist as e:
            raise exceptions.NotFound(
                detail=f"Post by ID {post_id} not found!"
            )

        return post

    @staticmethod
    def delete_post_by_id(*, post_id: int, author_id: int) -> None:

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist as e:
            raise exceptions.NotFound(
                detail=f"Post by ID {post_id} not found!"
            )

        if post.author.id != author_id:
            raise exceptions.PermissionDenied(
                detail="You can delete only your posts!"
            )

        post.delete()

    @staticmethod
    def update_post_by_id(*, post_id: int, author_id: int, data: dict) -> Post:

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist as e:
            raise exceptions.NotFound(
                detail=f"Post by ID {post_id} not found!"
            )

        # post = get_object_or_404(Post, id=post_id)

        if post.author.id != author_id:
            raise exceptions.PermissionDenied(
                detail="You can update only your posts!"
            )

        # TODO: refactor later
        if data.get("title"):
            post.title = data.get("title")
        if data.get("content"):
            post.content = data.get("content")
        if data.get("likes_count"):
            post.likes_count = data.get("likes_count")

        post.save()

        return post

    @staticmethod
    def get_post_by_id_with_comments(*, post_id: int) -> Post:

        post = Post.objects.prefetch_related('comments', 'comments__author').filter(id=post_id).first()
        return post

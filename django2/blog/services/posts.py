from django.db.models import QuerySet, Q
from django.http import QueryDict
from rest_framework import exceptions

from blog.filters import PostFilter
from blog.models import Post


class PostService:
    @staticmethod
    def get_all_posts(request_params: QueryDict) -> QuerySet[Post]:

        posts = Post.objects.all()

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
    def create_post( *, author_id: int, data: dict) -> Post:
        data['author_id'] = author_id
        post = Post(**data)
        post.save()

        return post

    @staticmethod
    def get_post_by_id(*, post_id: int) -> Post:

        try:
            post = Post.objects.get(id=post_id)
        except Post.DoesNotExist:
            raise exceptions.NotFound

        return post
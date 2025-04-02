from django.db.models import QuerySet
from rest_framework import exceptions

from blog.models import Post


class PostService:
    @staticmethod
    def get_all_posts() -> QuerySet[Post]:
        return Post.objects.all()

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
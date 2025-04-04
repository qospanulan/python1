from django.db.models import QuerySet
from django.http import QueryDict
from rest_framework import exceptions

from blog.filters import PostFilter
from blog.models import Post


class PostService:
    @staticmethod
    def get_all_posts(request_params: QueryDict) -> QuerySet[Post]:

        posts = Post.objects.all()

        if request_params:
            posts = PostFilter(request_params, posts).qs  # query set

        # if 'author_id' in request_params.keys():
        #     posts = posts.filter(author_id__exact=request_params.get('author_id'))
        # if 'tags' in request_params.keys():
        #     posts = posts.filter(tags__name__in=request_params.getlist('tags'))

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
from django.http import QueryDict
from rest_framework import status, serializers, exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.services.posts import PostService
from common.utils import inline_serializer


class CustomPaginationClass(PageNumberPagination):
    page_size_query_param = 'page_size'


class PostListAPIView(GenericAPIView):

    permission_classes = (AllowAny,)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField(max_length=200)
        content = serializers.CharField()
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()
        likes_count = serializers.IntegerField()

        author = inline_serializer(
            name="AuthorSerializer",
            fields={
                "id": serializers.IntegerField(),
                "username": serializers.CharField(max_length=255),
                "created_at": serializers.DateTimeField()
            }
        )


    def get(self, request: Request, *args, **kwargs):

        request_params: QueryDict = request.GET

        post_service = PostService()
        posts = post_service.get_all_posts(request_params=request_params)

        paginator = CustomPaginationClass()
        paginated_posts = paginator.paginate_queryset(posts, request)

        return paginator.get_paginated_response(
            data=self.OutputSerializer(paginated_posts, many=True).data
        )


class PostCreateAPIView(APIView):

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=200)
        content = serializers.CharField()
        likes_count = serializers.IntegerField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField(max_length=200)
        content = serializers.CharField()
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()
        likes_count = serializers.IntegerField()

        author_id = serializers.IntegerField()

    def post(self, request):

        data = self.InputSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        post_service = PostService()
        post = post_service.create_post(
            author_id=request.user.id,
            data=data.validated_data
        )

        return Response(
            data=self.OutputSerializer(post).data,
            status=status.HTTP_201_CREATED
        )

class PostDetailAPIView(APIView):

    permission_classes = (AllowAny,)

    class OutputSerializer(serializers.ModelSerializer):
        id = serializers.IntegerField()
        title = serializers.CharField(max_length=200)
        content = serializers.CharField()
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()
        likes_count = serializers.IntegerField()

        author_id = serializers.IntegerField()

    def get(self, request: Request, post_id: int) -> Response:

        post_service = PostService()

        post = post_service.get_post_by_id(post_id=post_id)

        return Response(
            data=self.OutputSerializer(post).data,
            status=status.HTTP_200_OK
        )


class PostDeleteAPIView(APIView):

    def delete(self, request, post_id: int, *args, **kwargs):

        post_service = PostService()

        post_service.delete_post_by_id(
            post_id=post_id,
            author_id=request.user.id
        )

        return Response(
            data={
                "detail": f"Post by ID {post_id} deleted!"
            },
            status=status.HTTP_200_OK
        )


class PostUpdateAPIView(APIView):

    # update - PUT -> {title, content, likes_count}
    # partial_update - PATCH -> {content}

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=200, required=False)
        content = serializers.CharField(required=False)
        likes_count = serializers.IntegerField(required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField(max_length=200)
        content = serializers.CharField()
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()
        likes_count = serializers.IntegerField()

        author_id = serializers.IntegerField()

    def patch(self, request, post_id: int):

        data = self.InputSerializer(data=request.data)
        data.is_valid(raise_exception=True)

        post_service = PostService()
        post = post_service.update_post_by_id(
            author_id=request.user.id,
            data=data.validated_data,
            post_id=post_id
        )

        return Response(
            data=self.OutputSerializer(post).data,
            status=status.HTTP_201_CREATED
        )


class PostCommentsListAPIView(APIView):

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField(max_length=200)
        content = serializers.CharField()

        comments = inline_serializer(
            name="CommentsInlineSerializer",
            fields={
                "text": serializers.CharField(),
                "author": inline_serializer(
                    name="CommentsAuthorInlineSerializer",
                    fields={
                        "id": serializers.IntegerField(),
                        "username": serializers.CharField()
                    }
                )
            },
            many=True
        )

    def get(self, request, post_id: int):

        post_service = PostService()

        comments = post_service.get_post_by_id_with_comments(
            post_id=post_id
        )

        return Response(
            data=self.OutputSerializer(comments).data,
            status=status.HTTP_200_OK
        )











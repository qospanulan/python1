from django.http import QueryDict
from rest_framework import status, serializers, exceptions
from rest_framework.generics import GenericAPIView
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.services.posts import PostService

# +Filter  ?author_id=123
# +Search  ?search=test

# Ordering  ?order=-created_at

# Pagination ?page=1

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

        author_id = serializers.IntegerField()


    def get(self, request: Request, *args, **kwargs):

        request_params: QueryDict = request.GET

        post_service = PostService()
        posts = post_service.get_all_posts(request_params=request_params)

        paginator = CustomPaginationClass()  # ?page=x&page_size=y
        # paginator = LimitOffsetPagination()  # ?offset=x&limit=y
        paginated_posts = paginator.paginate_queryset(posts, request)

        return paginator.get_paginated_response(
            data=self.OutputSerializer(paginated_posts, many=True).data
        )

        # print("Получены все данные!")
        #
        # page_size = int(request_params.get('page_size', 3))
        # page = int(request_params.get('page', 1))
        #
        # print("Получаем количество постов...")
        # total_pages = posts.count() // page_size
        # print("Получили!")
        #
        # l = (page - 1) * page_size
        # r = l + page_size
        # print("Начинаем пагинацию...")
        # posts = posts[l:r]
        # print("Закончили пагинацию!")
        #
        # url_template = f"http://localhost:8000/blog/posts/?page_size={page_size}"
        # prev_page = url_template + f"&page={page - 1}" if page > 1 else None
        # next_page = url_template + f"&page={page + 1}" if page < total_pages else None
        #
        # return Response(
        #     data={
        #         "page": page,
        #         "total_pages": total_pages,
        #         "prev": prev_page,
        #         "next": next_page,
        #         "results": self.OutputSerializer(posts, many=True).data,
        #     },
        #     status=status.HTTP_200_OK
        # )

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

        try:
            post = post_service.get_post_by_id(post_id=post_id)
        except exceptions.NotFound:
            return Response(
                data={
                    "detail": f"Post by ID {post_id} not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )

        return Response(
            data=self.OutputSerializer(post).data,
            status=status.HTTP_200_OK
        )

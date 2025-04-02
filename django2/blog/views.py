from rest_framework import status, serializers, exceptions
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Post
from blog.services.posts import PostService


class PostListAPIView(APIView):

    permission_classes = (AllowAny,)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField(max_length=200)
        content = serializers.CharField()
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()
        likes_count = serializers.IntegerField()

        author_id = serializers.IntegerField()

    def get(self, request, *args, **kwargs):

        post_service = PostService()
        posts = post_service.get_all_posts()

        return Response(
            data=self.OutputSerializer(posts, many=True).data,
            status=status.HTTP_200_OK
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

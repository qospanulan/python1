from rest_framework import status, serializers
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

    permission_classes = (IsAuthenticated,)

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = ('title', 'content', 'likes_count')

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = "__all__"

    def post(self, request):

        new_post = self.InputSerializer(data=request.data)

        if new_post.is_valid(raise_exception=True):
            new_post.validated_data['author_id'] = request.user.id
            post = new_post.save()

            post_data = self.OutputSerializer(post).data
            return Response(post_data)

class PostDetailAPIView(APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = "__all__"

    def get(self, request: Request, post_id) -> Response:

        post = Post.objects.get(pk=post_id)
        post_data = self.OutputSerializer(post).data

        return Response(post_data)

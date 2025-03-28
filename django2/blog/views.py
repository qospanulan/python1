from xmlrpc.client import ResponseError

from django.db.models import Q
from rest_framework import generics
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ModelSerializer
from rest_framework.views import APIView

from blog.models import Post
from blog.serializers import PostCreateSerializer, PostListGenericSerializer, PostCreateGenericSerializer


class PostListGenericAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostListGenericSerializer

    def get_queryset(self):

        queryset = self.queryset.filter(title__icontains="ser")
        return queryset


class PostCreateGenericAPIView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateGenericSerializer


class PostListCreateGenericAPIView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostCreateGenericSerializer


class PostDetailGenericAPIView(generics.RetrieveAPIView):
    queryset = Post.objects.all()

    def get_serializer_class(self):
        return PostListGenericSerializer

    def get_object(self):

        print("Custom Get Object method called.")
        print(f"URL Path Params: {self.kwargs}")

        queryset = self.get_queryset()

        obj = queryset.get(
            id=self.kwargs.get('post_id'),
            title__icontains=self.kwargs.get('title')
        )

        return obj



class PostListAPIView(APIView):

    permission_classes = (AllowAny,)

    class OutputSerializer(ModelSerializer):
        class Meta:
            model = Post
            fields = (
                "id", "title", "content",
                "created_at", "updated_at",
                "likes_count", "author_id"
            )

    def get(self, request):

        posts = Post.objects.all()
        posts_data = self.OutputSerializer(posts, many=True).data

        return Response(posts_data)

class PostCreateAPIView(APIView):

    permission_classes = (IsAuthenticated,)

    class InputSerializer(ModelSerializer):
        class Meta:
            model = Post
            fields = ('title', 'content', 'likes_count')

    class OutputSerializer(ModelSerializer):
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
    class OutputSerializer(ModelSerializer):
        class Meta:
            model = Post
            fields = "__all__"

    def get(self, request: Request, post_id) -> Response:

        post = Post.objects.get(pk=post_id)
        post_data = self.OutputSerializer(post).data

        return Response(post_data)


class TestAPIView(APIView):

    def get(self, request):

        filter_params = request.GET
        posts = Post.objects.all()

        # query = None
        # if filter_params.get("title"):
        #     query = Q(title__icontains=filter_params.get("title"))
        # if filter_params.get("content"):
        #     query = query | Q(content__icontains=filter_params.get("content"))
        #
        # if query:
        #     posts = posts.filter(query)

        if filter_params.get("title"):
            posts = posts.filter(title__icontains=filter_params.get("title"))
        if filter_params.get("content"):
            posts = posts.filter(content__icontains=filter_params.get("content"))

        posts_data = [ {
            "title": post.title,
            "content": post.content
        } for post in posts ]

        return Response(posts_data)

    def post(self, request):

        title = request.data.get("title")
        content = request.data.get("content")
        likes_count = request.data.get("likes_count")

        new_post = Post(
            title=title,
            content=content,
            likes_count=likes_count,
            author_id=2
        )

        new_post.save()

        return Response({
            "title": new_post.title,
            "content": new_post.content,
            "likes_count": new_post.likes_count
        })


# @api_view()
# def test_view(request):
#     return Response([
#         {
#             "title": "Test Title 1",
#             "content": "Test Content 1"
#         },
#         {
#             "title": "Test Title 2",
#             "content": "Test Content 2"
#         },
#         {
#             "title": "Test Title 3",
#             "content": "Test Content 3"
#         }
#     ])

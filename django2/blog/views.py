from xmlrpc.client import ResponseError

from django.db.models import Q
from rest_framework.response import Response
from rest_framework.views import APIView

from blog.models import Post
from blog.serializers import PostCreateSerializer


class PostListAPIView(APIView):

    def get(self, request):

        posts = Post.objects.all()


        posts_data = [ {
            "title": post.title,
            "content": post.content
        } for post in posts ]

        return Response(posts_data)


class PostCreateAPIView(APIView):

    def post(self, request):

        new_post = PostCreateSerializer(data=request.data)

        if new_post.is_valid(raise_exception=True):
            new_post.validated_data['author_id'] = 3
            new_post.save()

            return Response(new_post.data)



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

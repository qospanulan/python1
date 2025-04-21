from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers

from blog.services.comments import CommentService
from common.utils import inline_serializer


class CommentListAPIView(APIView):

    class OutputSerializer(serializers.Serializer):
        text = serializers.CharField()

        post = inline_serializer(
            name="CommentsPostSerializer",
            fields={
                "id": serializers.IntegerField(),
                "title": serializers.CharField(),
                "content": serializers.CharField(),
                "author": inline_serializer(
                    fields={
                        "id": serializers.IntegerField(),
                        "username": serializers.CharField(),
                    }
                )
            }
        )

    def get(self, request):

        comment_service = CommentService()
        comments = comment_service.get_comments_by_author(
            author_id=request.user.id
        )

        return Response(self.OutputSerializer(comments, many=True).data)


class CommentCreateAPIView(APIView):

    class InputSerializer(serializers.Serializer):
        post_id = serializers.IntegerField()
        text = serializers.CharField()

    class OutputSerializer(serializers.Serializer):
        text = serializers.CharField()
        post_id = serializers.IntegerField()

    def post(self, request):

        serializer = self.InputSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        comment_service = CommentService()

        comment = comment_service.create_comment(
            author_id=request.user.id,
            post_id=serializer.validated_data.get("post_id"),
            text=serializer.validated_data.get("text")
        )

        return Response(self.OutputSerializer(comment).data)


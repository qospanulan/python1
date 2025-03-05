from rest_framework.serializers import ModelSerializer

from blog.models import Post


class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'content', 'likes_count')


class PostListGenericSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id", "title", "content",
            "created_at", "updated_at",
            "likes_count", "author_id"
        )

class PostCreateGenericSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = (
            "id", "title", "content",
            "created_at", "updated_at",
            "likes_count", "author"
        )
        read_only = (
            "id", "created_at", "updated_at"
        )



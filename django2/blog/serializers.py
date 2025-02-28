from rest_framework.serializers import ModelSerializer

from blog.models import Post


class PostCreateSerializer(ModelSerializer):
    class Meta:
        model = Post
        fields = ('title', 'content', 'likes_count')


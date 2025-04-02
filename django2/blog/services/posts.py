from blog.models import Post


class PostService:

    def get_all_posts(self):
        return Post.objects.all()


"""


http://localhost:8000/

http://localhost:8000/admin/

http://localhost:8000/blog/posts/
http://localhost:8000/blog/posts/create
http://localhost:8000/blog/posts/1
http://localhost:8000/blog/posts/1/delete

http://localhost:8000/blog/posts/comments/


"""
from django.urls import path

from blog.views import posts_list_view, posts_detail_view, post_create_view, PostListView, PostListViewOld, \
    CommentListViewOld, CommentListView, PostDetailView, PostCreateView

urlpatterns = [
    path("posts/", PostListViewOld.as_view(), name="posts_list"),
    path("comments/", CommentListView.as_view(), name="comments_list"),
    path("posts/create/", PostCreateView.as_view(), name="post_create"),
    path("posts/<int:post_id>/", PostDetailView.as_view(), name="posts_detail"),
]


from django.urls import path

from blog.views import posts as post_views
from blog.views import comments as comment_views

urlpatterns = [
    # posts
    path('posts/', post_views.PostListAPIView.as_view()),
    path('posts/create/', post_views.PostCreateAPIView.as_view()),
    path('posts/<int:post_id>/', post_views.PostDetailAPIView.as_view()),
    path('posts/<int:post_id>/delete/', post_views.PostDeleteAPIView.as_view()),
    path('posts/<int:post_id>/update/', post_views.PostUpdateAPIView.as_view()),

    path('posts/<int:post_id>/comments/', post_views.PostCommentsListAPIView.as_view()),
    path('posts/<int:post_id>/comments/create/', post_views.PostCommentsCreateAPIView.as_view()),

    # comments
    path('comments/', comment_views.CommentListAPIView.as_view()),
    path('comments/create/', comment_views.CommentCreateAPIView.as_view()),

]


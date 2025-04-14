from django.urls import path

from blog import views

urlpatterns = [
    path('posts/', views.PostListAPIView.as_view()),
    path('posts/create/', views.PostCreateAPIView.as_view()),
    path('posts/<int:post_id>/', views.PostDetailAPIView.as_view()),
    path('posts/<int:post_id>/delete/', views.PostDeleteAPIView.as_view()),
]


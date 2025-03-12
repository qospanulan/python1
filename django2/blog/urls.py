from django.urls import path

from blog import views

urlpatterns = [
    path('test/', views.TestAPIView.as_view()),
    path('posts/', views.PostListAPIView.as_view()),
    path('posts/create/', views.PostCreateAPIView.as_view()),
    path('posts/<int:post_id>/', views.PostDetailAPIView.as_view()),

    # path('generic/posts/', views.PostListGenericAPIView.as_view()),
    # path('generic/posts/create/', views.PostCreateGenericAPIView.as_view()),
    path('generic/posts/', views.PostListCreateGenericAPIView.as_view()),
    path('generic/posts/<int:post_id>/<str:title>/', views.PostDetailGenericAPIView.as_view()),
]


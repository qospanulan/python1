from django.urls import path

from blog import views

urlpatterns = [
    path('test/', views.TestAPIView.as_view()),
    path('posts/', views.PostListAPIView.as_view()),
    path('posts/create/', views.PostCreateAPIView.as_view()),
]

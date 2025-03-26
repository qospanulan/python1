from django.urls import path

from authorization import views

urlpatterns = [
    path('health/', views.HealthApiView.as_view()),
    path('register/', views.RegisterApiView.as_view()),
    path('login/', views.LoginApiView.as_view()),
    path('logout/', views.LogoutApiView.as_view()),
]

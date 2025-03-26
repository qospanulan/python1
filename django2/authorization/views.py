from django.contrib.auth import get_user_model, authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse
from rest_framework import serializers
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView


class HealthApiView(APIView):

    permission_classes = (IsAuthenticated,)
    # permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):

        print("Get request was sent by:", request.user)

        return HttpResponse("Ok!")


class LoginApiView(APIView):

    class InputSerializer(serializers.Serializer):
        username = serializers.CharField(max_length=150)
        password = serializers.CharField(max_length=128)


    def post(self, request, *args, **kwargs):
        serializer = self.InputSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            print(serializer.validated_data)

            user = authenticate(
                request,
                username=serializer.validated_data.get("username"),
                password=serializer.validated_data.get("password")
            )

            if user:
                login(request, user)

            print("user:", user.username)


        return Response({"message": "Login successful!"})


class LogoutApiView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request, *args, **kwargs):
        logout(request)

        return Response({"message": "Logout successful!"})


class RegisterApiView(APIView):

    class InputSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            fields = ['username', 'password']

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = get_user_model()
            # fields = ['username']
            fields = '__all__'

    def post(self, request, *args, **kwargs):

        serializer = self.InputSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            print(serializer.validated_data)
            hashed_password = make_password(serializer.validated_data.get("password"))
            print("hashed_password:", hashed_password)

            serializer.validated_data["password"] = hashed_password
            user = serializer.save()

        return Response(self.OutputSerializer(user).data)

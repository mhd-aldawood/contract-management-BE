
from django.contrib.auth.models import User
from django.contrib.auth import logout as django_logout
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    SignupSerializer,
    LoginSerializer,
    UserSerializer,
    TokenSerializer,
)


class SignupView(APIView):
    """POST /api/auth/signup/  ->  create user + return token"""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SignupSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                'message': 'User created successfully.',
                'user': UserSerializer(user).data,
                'token': token.key,
            },
            status=status.HTTP_201_CREATED,
        )


class LoginView(APIView):
    """POST /api/auth/login/  ->  authenticate + return token"""
    permission_classes = [AllowAny]

    def post(self, request):
        print("REQUEST DATA:", request.data)  # 👈 debug
        print("CONTENT TYPE:", request.content_type)
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)

        return Response(
            {
                'message': 'Login successful.',
                'user': UserSerializer(user).data,
                'token': token.key,
            },
            status=status.HTTP_200_OK,
        )


class LogoutView(APIView):
    """POST /api/auth/logout/  ->  delete user's token"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        django_logout(request)
        return Response({'message': 'Logged out.'}, status=status.HTTP_200_OK)


class MeView(APIView):
    """GET /api/auth/me/  ->  current user's info"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return Response(UserSerializer(request.user).data)


class TokenRefreshView(APIView):
    """POST /api/auth/token/refresh/  ->  rotate token"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        Token.objects.filter(user=request.user).delete()
        token = Token.objects.create(user=request.user)
        return Response(TokenSerializer(token).data, status=status.HTTP_200_OK)
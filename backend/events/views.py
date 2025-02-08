from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .serializers import UserSerializer, UserSignupSerializer
from rest_framework import status
import json

class UserSignup(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """ Crée un nouvel utilisateur """
        serializer = UserSignupSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"success": "User created successfully"}, status=status.HTTP_201_CREATED)
        
        return Response({"error": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """ Authentifie l'utilisateur et crée une session. """
        try:
            data = json.loads(request.body)
            username = data.get("username")
            password = data.get("password")

            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return Response({"success": "Logged in successfully"}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)

        except json.JSONDecodeError:
            return Response({"error": "Invalid JSON format"}, status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """ Déconnecte l'utilisateur. """
        logout(request)
        return Response({"success": "Logged out successfully"}, status=status.HTTP_200_OK)


class UserIsAuthenticated(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """ Vérifie si l'utilisateur est connecté. """
        return Response({"authenticated": True, "user": request.user.username}, status=200)

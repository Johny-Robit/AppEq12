from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.middleware.csrf import get_token
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import UserSerializer, UserSignupSerializer, UserLoginSerializer


class UserSignup(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """Creates a new user"""
        serializer = UserSignupSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.save()
            return Response({"success": "User created successfully", "userid": user.id}, status=status.HTTP_201_CREATED)

        error_messages = serializer.errors

        if "username" in error_messages or "email" in error_messages:
            return Response({"error": "Email or username already taken"}, status=status.HTTP_400_BAD_REQUEST)

        if "password" in error_messages:
            return Response({"error": "Invalid password format"}, status=status.HTTP_400_BAD_REQUEST)

        return Response({"error": "Bad request."}, status=status.HTTP_400_BAD_REQUEST)


class UserLogin(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        """Authentifie l'utilisateur et crée une session."""
        serializer = UserLoginSerializer(data=request.data)

        if serializer.is_valid():
            user = serializer.validated_data["user"]
            login(request, user)  # Connecte l'utilisateur
            
            # Création de la réponse
            response = Response({"message": "Login successful"}, status=status.HTTP_200_OK)

            # Django gère automatiquement la session et le cookie.
            # Le cookie est ajouté automatiqument à la réponse HTTP.

            return response
        
        # Filtrage des erreurs pour éviter de donner des infos sensibles
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)



class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """ Déconnecte l'utilisateur. """
        logout(request)
        return Response({"success": "Logged out successfully"}, status=status.HTTP_200_OK)


class UserIsAuthenticated(APIView):
    def get(self, request):
        """ Vérifie si l'utilisateur est connecté. """
        if request.user.is_authenticated:
            return Response({"authenticated": True, "user": request.user.username}, status=200)
        return Response({"authenticated": False}, status=200)

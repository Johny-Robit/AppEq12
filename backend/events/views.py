from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import AccessToken
from django.contrib.auth import get_user_model

from .serializers import UserLoginSerializer, UserSignupSerializer, UserProfileSerializer
import logging

User = get_user_model()

logger = logging.getLogger("eventify")

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

            # Supprimer l'ancien token (si existant)
            AccessToken.objects.filter(user=user).delete()

            # Générer un nouveau token
            access_token = AccessToken.objects.create(user=user)

            return Response({
                "token": str(access_token.token)
            }, status=status.HTTP_200_OK)
        
        return Response({"error": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)


class UserLogout(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        """ Déconnecte l'utilisateur en blacklistant le refresh token. """
        try: 
            token = request.headers.get("Authorization")
            if not token:
                logger.error(f"UserLogout failed in UserLogout View: request.data.get('refresh') failed to fetch token")
                return Response({"error": "No access token provided"}, status=status.HTTP_400_BAD_REQUEST)

            token = token.replace("Bearer ", "")
            delete_count, _ = AccessToken.objects.filter(token=token).delete()      

            if delete_count == 0:
                logger.warning(f"Invalid or expired token provided in logout UserLogout view.")
                return Response({"error": "Invalid or expired token"}, status=status.HTTP_400_BAD_REQUEST)

            return Response({"success": "Logged out successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"UserLogout failed in UserLogout View: {e}")
            return Response({"error": "Unexpected error logging out."}, status=status.HTTP_400_BAD_REQUEST)


class EditProfile(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        """Permet à l'utilisateur d'éditer son profil"""
        try:
            user = request.user # Récupère l'instance de User
            serializer = UserProfileSerializer(user, data=request.data, partial=True)

            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Profile updated successfully"}, status=status.HTTP_200_OK)
            
            return Response({"error": "Description or image link is invalid"}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"EditProfile View failed: {e}")
            return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetProfile(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        """Permet à l'utilisateur de récupérer son profil"""
        try:
            user = request.user  # Récupère l'instance de User

            if not user:
                return Response(status=status.HTTP_404_NOT_FOUND)
            
            username = user.username
            description = user.description
            profile_image_link = user.profile_image_link

            return Response(
                {
                    "username": str(username),
                    "description": str(description),
                    "profile_image_link": str(profile_image_link)
                },
                status=status.HTTP_200_OK
            )

        except Exception as e:
            logger.error(f"GetProfile View failed: {e}")
            return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import AccessToken, Event
from django.contrib.auth import get_user_model

from .serializers import UserLoginSerializer, UserSignupSerializer, UserProfileSerializer, EventSerializer, GetEventSerializer, AttendeeSerializer
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


class GetJoinedEventsList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            joined_events = Event.objects.filter(attendees=request.user)

            serializer = GetEventSerializer(joined_events, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"GetJoinedEventsList View failed: {e}")
            return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class JoinEvent(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            event_id = request.data.get("event_id")
            user = request.user
            event = Event.objects.filter(event_id=event_id).first()

            # Check if event exists
            if not event:
                return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

            # Check if user is already an attendee
            if event.attendees.filter(id=user.id).exists():
                return Response({"error": "User already joined the event"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if user is already invited
            if event.pending_invites.filter(id=user.id).exists():
                event.pending_invites.remove(user)
            
            # Add user to attendees
            event.attendees.add(user)
            print(event.attendees.all()) 
            return Response({"message": "Joined event successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"JoinEvent View failed: {e}")
            return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LeaveEvent(APIView):
    permission_classes = [IsAuthenticated]


    def put(self, request):
        try:
            event_id = request.data.get("event_id")
            user = request.user
            event = Event.objects.filter(event_id=event_id).first()

            # Check if event exists
            if not event:
                return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

            # Check if user is an attendee
            if not event.attendees.filter(id=user.id).exists():
                return Response({"error": "User is not part of the event"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Remove user from attendees
            event.attendees.remove(user)
            return Response({"message": "Left event successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"LeaveEvent View failed: {e}")
            return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class InviteToEvent(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            event_id = request.data.get("event_id")
            user_id = request.data.get("user_id")
            event = Event.objects.filter(event_id=event_id).first()
            invitee = User.objects.filter(id=user_id).first()

            # Check if event exists
            if not event:
                return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

            # Check if invitee exists
            if not invitee:
                return Response({"error": "Invitee not found"}, status=status.HTTP_404_NOT_FOUND)

            # Check if invitee is already an attendee
            if event.attendees.filter(id=user_id).exists():
                return Response({"error": "Invitee already joined the event"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Check if invitee is already invited
            if event.pending_invites.filter(id=user_id).exists():
                return Response({"error": "Invitee already invited to the event"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Add invitee to pending invites
            event.pending_invites.add(invitee)
            return Response({"message": "Invited to event successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"InviteToEvent View failed: {e}")
            return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class RemoveAttendee(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            event_id = request.data.get("event_id")
            user_id = request.data.get("user_id")
            event = Event.objects.filter(event_id=event_id).first()
            user = User.objects.filter(id=user_id).first()

            # Check if event is owned by user
            if event.owner != request.user:
                return Response({"error": "Unauthorized access"}, status=status.HTTP_403_FORBIDDEN)

            # check if user_id is owner's id
            if int(user_id) == event.owner.id:
                return Response({"error": "Owner cannot be removed from attendees"}, status=status.HTTP_400_BAD_REQUEST)


            # Check if event exists
            if not event:
                return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

            # Check if user exists
            if not user:
                return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

            # Check if user is an attendee
            if not event.attendees.filter(id=user_id).exists():
                return Response({"error": "User is not part of the event"}, status=status.HTTP_400_BAD_REQUEST)
            
            # Remove user from attendees
            event.attendees.remove(user)
            return Response({"message": "Removed attendee successfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"RemoveAttendee View failed: {e}")
            return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateEvent(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            serializer = EventSerializer(data=request.data)
            if serializer.is_valid():
                event = serializer.save(owner=request.user)
                return Response({"message": "Event created successfully", "event_id": event.event_id}, status=status.HTTP_201_CREATED)
            
            return Response({"error": "Invalid input data"}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as e:
            logger.error(f"GetProfile View failed: {e}")
            return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class EditEvent(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        try:
            event_id = request.data.get("event_id")
            event = Event.objects.filter(event_id=event_id, owner=request.user).first()

            if not event:
                return Response({"error": "Event not found or unauthorized"}, status=status.HTTP_404_NOT_FOUND)

            serializer = EventSerializer(event, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message": "Event updated successfully"}, status=status.HTTP_200_OK)

            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            logger.error(f"EditEvent View failed: {e}")
            return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class DeleteEvent(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        try:
            event_id = request.data.get("event_id")
            if not event_id:
                return Response({"error": "Event ID is required"}, status=status.HTTP_400_BAD_REQUEST)

            event = Event.objects.filter(event_id=event_id, owner=request.user).first()

            if not event:
                return Response({"error": "Event not found or you do not have permission to delete it."},
                                status=status.HTTP_404_NOT_FOUND)

            event.delete()
            return Response({"message": "Event deleted successfully"}, status=status.HTTP_200_OK)

        except Exception as e:
            logger.error(f"DeleteEvent View failed: {e}")
            return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetEventView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, event_id):
        try:
            event = Event.objects.filter(event_id=event_id).first()
            if not event:
                return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

            serializer = GetEventSerializer(event)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"GetEventView failed: {e}")
            return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class GetAttendeeList(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        try:
            event = Event.objects.filter(event_id=event_id).first()
            if not event:
                return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

            attendees = event.attendees.all()
            serializer = AttendeeSerializer(attendees, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"AttendeeList failed: {e}")
            return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetPendingInvites(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, event_id):
        try:
            event = Event.objects.filter(event_id=event_id).first()
            if not event:
                return Response({"error": "Event not found"}, status=status.HTTP_404_NOT_FOUND)

            if request.user != event.owner:
                return Response({"error": "Access to pending invites only allowed to owner."}, status=status.HTTP_403_FORBIDDEN)

            pending_invites = event.pending_invites.all()
            serializer = AttendeeSerializer(pending_invites, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error(f"GetPendingInvites failed: {e}")
            return Response({"error": "Internal server error."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

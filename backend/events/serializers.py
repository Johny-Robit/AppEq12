from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError 
from .models import Event
import logging
import re

User = get_user_model()

logger = logging.getLogger("eventify")

class UserSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ["username", "email", "password"]

    def validate(self, data):
        """Check if username OR email is already taken and return a generic error message"""
        if User.objects.filter(username=data["username"]).exists() or User.objects.filter(email=data["email"]).exists():
            logger.error(f"Validation Error: Email or username already taken - Data: {data}")
            raise ValidationError("Email or username already taken") 
        return data

    def create(self, validated_data):
        # Separate and hash the password
        password = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """Vérifie que l'utilisateur existe et que les identifiants sont corrects"""
        email = data["email"]
        password = data["password"]

        user_model = User.objects.get(email=email)

        user = authenticate(username=user_model.username, password=password)

        if not user:
            raise serializers.ValidationError("Invalid credentials.")

        # Ajout de l'utilisateur validé
        data["user"] = user
        return data

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['description', 'profile_image_link']
    
    def validate_profile_image_link(self, value):
        """
        Vérifie que l'URL de l'image est valide.
        """
        url_pattern = re.compile(
            r'^(https?:\/\/)?'  # http:// ou https:// (optionnel)
            r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}'  # Nom de domaine
            r'(:\d+)?(\/.*)?$'  # Port optionnel et chemin
        )

        if not url_pattern.match(value):
            raise ValidationError("L'URL fournie n'est pas valide.")

        return value

    def update(self, instance, validated_data):
        """Met à jour uniquement les champs description et profile_image_link"""
        instance.description = validated_data.get('description', instance.description)
        instance.profile_image_link = validated_data.get('profile_image_link', instance.profile_image_link)
        instance.save()
        return instance

class GetAllUsersSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source='id')
    username = serializers.CharField()

    class Meta:
        model = User
        fields = ['user_id', 'username']
    
class EventSerializer(serializers.ModelSerializer):
    is_public = serializers.BooleanField(source="event_is_public")
    event_id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Event
        fields = [
            "event_id", "event_name", "event_address", "start_datetime",
            "end_datetime", "description", "is_public", "event_image_link"
        ]

    def validate_event_image_link(self, value):
        """
        Vérifie que l'URL de l'image est valide.
        """
        url_pattern = re.compile(
            r'^(https?:\/\/)?'  # http:// ou https:// (optionnel)
            r'([a-zA-Z0-9-]+\.)+[a-zA-Z]{2,6}'  # Nom de domaine
            r'(:\d+)?(\/.*)?$'  # Port optionnel et chemin
        )

        if not url_pattern.match(value):
            raise serializers.ValidationError("L'URL fournie n'est pas valide.")

        return value
    
class GetEventSerializer(serializers.ModelSerializer):
    ownerID = serializers.IntegerField(source="owner.id", read_only=True)
    is_public = serializers.BooleanField(source="event_is_public")

    class Meta:
        model = Event
        fields = [
            "ownerID", "event_name", "event_address", "start_datetime",
            "end_datetime", "description", "is_public", "event_id"
        ]

class AttendeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id"]
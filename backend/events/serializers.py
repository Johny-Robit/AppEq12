from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError 
import logging

logger = logging.getLogger("eventify")

class UserSerializer(serializers.ModelSerializer):
    """Sérialiseur pour afficher les infos utilisateurs"""
    class Meta:
        model = User
        fields = ["id", "username", "email"]


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

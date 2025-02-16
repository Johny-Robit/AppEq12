from rest_framework import serializers
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError 
import logging

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




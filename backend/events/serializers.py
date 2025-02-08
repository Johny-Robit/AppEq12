from rest_framework import serializers
from django.contrib.auth.models import User

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

    def create(self, validated_data):
        # séparer le mot de passe
        password = validated_data.pop("password")
        # créer l'utilisateur
        user = User(**validated_data)
        # hasher le mot de passe
        user.set_password(password)
        # sauvegarder l'utilisateur
        user.save()
        return user

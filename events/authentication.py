from rest_framework.authentication import BaseAuthentication
from .models import AccessToken
from datetime import datetime

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization")
        if not token:
            return None  # Pas de token = pas d'authentification

        token = token.replace("Bearer ", "")  # Enlever "Bearer "

        try:
            access_token = AccessToken.objects.get(token=token)

            if access_token.expires_at < datetime.now():
                return None # Token expiré

            return (access_token.user, None)
        except AccessToken.DoesNotExist:
            return None

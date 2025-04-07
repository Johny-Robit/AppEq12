from rest_framework.authentication import BaseAuthentication
from .models import AccessToken
from django.utils.timezone import now
import logging

logger = logging.getLogger("eventify")

class TokenAuthentication(BaseAuthentication):
    def authenticate(self, request):
        token = request.headers.get("Authorization")

        if not token:
            logger.warning("No Authorization header provided.")
            return None  # Pas de token = pas d'authentification

        token = token.replace("Bearer ", "")  # Enlever "Bearer "

        try:
            access_token = AccessToken.objects.get(token=token)
            logger.info(now())

            if access_token.expires_at < now():
                logger.warning(f"Token expired for user {access_token.user.username}.")
                return None  # Token expiré

            logger.info(f"Token authenticated for user {access_token.user.username}.")
            return (access_token.user, None)
        except AccessToken.DoesNotExist:
            logger.error("Invalid token provided.")
            return None

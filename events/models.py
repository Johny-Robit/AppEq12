from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid


class AccessToken(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    token = models.UUIDField(default=uuid.uuid4, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)


class CustomUser(AbstractUser):
    description = models.TextField(blank=True, null=True)
    profile_image_link = models.URLField(blank=True, null=True)

    class Meta:
        verbose_name = "Utilisateur"
        verbose_name_plural = "Utilisateurs"


class Event(models.Model):
    event_id = models.AutoField(primary_key=True)
    event_name = models.CharField(max_length=255)
    event_address = models.CharField(max_length=255)
    start_datetime = models.CharField(max_length=255)
    end_datetime = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    event_is_public = models.BooleanField(default=True)
    event_image_link = models.URLField(blank=True, null=True)

    # Relations avec les utilisateurs
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="owned_events") # ForeignKey UserID
    pending_invites = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="pending_invites", blank=True) # UserId
    attendees = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="attended_events", blank=True) #UserID

    def __str__(self):
        return self.event_name

    class Meta:
        verbose_name = "Événement"
        verbose_name_plural = "Événements"
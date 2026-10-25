from django.conf import settings
from django.db import models
from apps.core.models import UUIDTimeStampedModel

class Notification(UUIDTimeStampedModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="notifications")
    title = models.CharField(max_length=255)
    message = models.TextField()
    type = models.CharField(max_length=50)
    is_read = models.BooleanField(default=False, db_index=True)
    related_entity_type = models.CharField(max_length=100, blank=True)
    related_entity_id = models.CharField(max_length=64, blank=True)
    read_at = models.DateTimeField(null=True, blank=True)


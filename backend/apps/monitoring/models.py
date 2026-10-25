from django.conf import settings
from django.db import models
from apps.core.models import UUIDTimeStampedModel

class MonitoringAlert(UUIDTimeStampedModel):
    class Status(models.TextChoices):
        OPEN="OPEN","Open"; ACKNOWLEDGED="ACKNOWLEDGED","Acknowledged"; RESOLVED="RESOLVED","Resolved"
    class Severity(models.TextChoices):
        INFO="INFO","Info"; WARNING="WARNING","Warning"; HIGH="HIGH","High"; CRITICAL="CRITICAL","Critical"
    alert_type = models.CharField(max_length=80, db_index=True)
    severity = models.CharField(max_length=20, choices=Severity.choices, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    related_entity_type = models.CharField(max_length=100)
    related_entity_id = models.CharField(max_length=64)
    office = models.ForeignKey("organization.Office", null=True, on_delete=models.SET_NULL)
    generated_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN, db_index=True)
    acknowledged_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="acknowledged_alerts")
    acknowledged_at = models.DateTimeField(null=True, blank=True)
    resolved_at = models.DateTimeField(null=True, blank=True)
    fingerprint = models.CharField(max_length=255, db_index=True)
    class Meta:
        constraints = [models.UniqueConstraint(fields=["fingerprint"], condition=models.Q(status__in=["OPEN","ACKNOWLEDGED"]), name="unique_active_alert_condition")]


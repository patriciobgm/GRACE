from django.db import models
from apps.core.models import UUIDTimeStampedModel

class Office(UUIDTimeStampedModel):
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    office_head = models.ForeignKey("accounts.User", null=True, blank=True, on_delete=models.SET_NULL, related_name="headed_offices")
    is_active = models.BooleanField(default=True, db_index=True)
    class Meta:
        ordering = ["code"]
    def __str__(self): return f"{self.code} — {self.name}"


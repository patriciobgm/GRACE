import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        SYSTEM_ADMIN = "SYSTEM_ADMIN", "System Administrator"
        GRC_ADMIN = "GRC_ADMIN", "GRC Administrator"
        EXECUTIVE = "EXECUTIVE", "Executive / Approver"
        COMPLIANCE_OFFICER = "COMPLIANCE_OFFICER", "Compliance Officer"
        RISK_OWNER = "RISK_OWNER", "Risk Owner / Office Head"
        AUDITOR = "AUDITOR", "Auditor / Reviewer"
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=32, choices=Role.choices, default=Role.RISK_OWNER, db_index=True)
    office = models.ForeignKey("organization.Office", null=True, blank=True, on_delete=models.SET_NULL, related_name="members")
    REQUIRED_FIELDS = ["email"]


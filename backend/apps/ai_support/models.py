from django.conf import settings
from django.db import models
from apps.core.models import UUIDTimeStampedModel

class AIAnalysis(UUIDTimeStampedModel):
    class Type(models.TextChoices):
        RISK="RISK","Risk Analysis"; COMPLIANCE="COMPLIANCE","Compliance Analysis"; EXECUTIVE_BRIEF="EXECUTIVE_BRIEF","Executive GRC Brief"
    class ReviewStatus(models.TextChoices):
        PENDING_REVIEW="PENDING_REVIEW","Pending Review"; ACCEPTED="ACCEPTED","Accepted"; ACCEPTED_WITH_MODIFICATION="ACCEPTED_WITH_MODIFICATION","Accepted With Modification"; REJECTED="REJECTED","Rejected"
    analysis_type = models.CharField(max_length=30, choices=Type.choices, db_index=True)
    related_entity_type = models.CharField(max_length=100, blank=True)
    related_entity_id = models.CharField(max_length=64, blank=True)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="requested_ai_analyses")
    requested_at = models.DateTimeField(auto_now_add=True)
    input_snapshot = models.JSONField()
    provider = models.CharField(max_length=50)
    model_name = models.CharField(max_length=100, blank=True)
    generated_response = models.TextField()
    evidence_references = models.JSONField(default=list)
    human_review_status = models.CharField(max_length=40, choices=ReviewStatus.choices, default=ReviewStatus.PENDING_REVIEW, db_index=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name="reviewed_ai_analyses")
    reviewed_at = models.DateTimeField(null=True, blank=True)
    reviewer_comments = models.TextField(blank=True)
    final_management_note = models.TextField(blank=True)


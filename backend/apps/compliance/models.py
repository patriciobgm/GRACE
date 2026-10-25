from django.conf import settings
from django.core.validators import MaxValueValidator
from django.db import models
from apps.core.models import UUIDTimeStampedModel

class ComplianceObligation(UUIDTimeStampedModel):
    class SourceType(models.TextChoices):
        LAW="LAW","Law"; REGULATION="REGULATION","Regulation"; GOVERNMENT_REQUIREMENT="GOVERNMENT_REQUIREMENT","Government Requirement"; INSTITUTIONAL_POLICY="INSTITUTIONAL_POLICY","Institutional Policy"; ACCREDITATION="ACCREDITATION","Accreditation"; INTERNAL_STANDARD="INTERNAL_STANDARD","Internal Standard"; OTHER="OTHER","Other"
    class Status(models.TextChoices):
        DRAFT="DRAFT","Draft"; ACTIVE="ACTIVE","Active"; DUE_SOON="DUE_SOON","Due Soon"; OVERDUE="OVERDUE","Overdue"; COMPLETED="COMPLETED","Completed"; CANCELLED="CANCELLED","Cancelled"
    obligation_code = models.CharField(max_length=30, unique=True, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    source_type = models.CharField(max_length=30, choices=SourceType.choices)
    source_reference = models.CharField(max_length=255)
    regulatory_body = models.CharField(max_length=255, blank=True)
    responsible_office = models.ForeignKey("organization.Office", on_delete=models.PROTECT)
    responsible_person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    frequency = models.CharField(max_length=50)
    effective_date = models.DateField()
    due_date = models.DateField(db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)
    risk_level = models.CharField(max_length=20, choices=[(v,v.title()) for v in ["LOW","MODERATE","HIGH","CRITICAL"]])
    requirements = models.TextField()
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="created_obligations")

class ComplianceEvidence(UUIDTimeStampedModel):
    class ReviewStatus(models.TextChoices):
        PENDING_REVIEW="PENDING_REVIEW","Pending Review"; ACCEPTED="ACCEPTED","Accepted"; REJECTED="REJECTED","Rejected"; NEEDS_REVISION="NEEDS_REVISION","Needs Revision"
    obligation = models.ForeignKey(ComplianceObligation, on_delete=models.CASCADE, related_name="evidence")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    attachment = models.ForeignKey("core.Attachment", null=True, blank=True, on_delete=models.PROTECT)
    submitted_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="submitted_evidence")
    submitted_at = models.DateTimeField(auto_now_add=True)
    review_status = models.CharField(max_length=20, choices=ReviewStatus.choices, default=ReviewStatus.PENDING_REVIEW, db_index=True)
    reviewed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name="reviewed_evidence")
    reviewed_at = models.DateTimeField(null=True, blank=True)
    review_remarks = models.TextField(blank=True)

class ComplianceFinding(UUIDTimeStampedModel):
    class Status(models.TextChoices):
        OPEN="OPEN","Open"; IN_PROGRESS="IN_PROGRESS","In Progress"; CLOSED="CLOSED","Closed"; ACCEPTED_RISK="ACCEPTED_RISK","Accepted Risk"
    finding_number = models.CharField(max_length=30, unique=True, db_index=True)
    obligation = models.ForeignKey(ComplianceObligation, on_delete=models.PROTECT, related_name="findings")
    description = models.TextField()
    severity = models.CharField(max_length=20, choices=[(v,v.title()) for v in ["LOW","MODERATE","HIGH","CRITICAL"]], db_index=True)
    date_identified = models.DateField()
    identified_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="identified_findings")
    responsible_office = models.ForeignKey("organization.Office", on_delete=models.PROTECT)
    due_date = models.DateField(db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN, db_index=True)
    closed_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.PROTECT, related_name="closed_findings")
    closed_at = models.DateTimeField(null=True, blank=True)
    closure_remarks = models.TextField(blank=True)

class CorrectiveAction(UUIDTimeStampedModel):
    class Status(models.TextChoices):
        NOT_STARTED="NOT_STARTED","Not Started"; IN_PROGRESS="IN_PROGRESS","In Progress"; COMPLETED="COMPLETED","Completed"; OVERDUE="OVERDUE","Overdue"; CANCELLED="CANCELLED","Cancelled"
    finding = models.ForeignKey(ComplianceFinding, on_delete=models.CASCADE, related_name="corrective_actions")
    action = models.TextField()
    assigned_to = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    responsible_office = models.ForeignKey("organization.Office", on_delete=models.PROTECT)
    target_date = models.DateField(db_index=True)
    progress_percentage = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_STARTED, db_index=True)
    remarks = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)


from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from apps.core.models import UUIDTimeStampedModel

class RiskCategory(UUIDTimeStampedModel):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

class Risk(UUIDTimeStampedModel):
    class Status(models.TextChoices):
        OPEN="OPEN","Open"; MONITORING="MONITORING","Monitoring"; TREATING="TREATING","Treating"; CLOSED="CLOSED","Closed"; ACCEPTED="ACCEPTED","Accepted"
    risk_code = models.CharField(max_length=30, unique=True, db_index=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.ForeignKey(RiskCategory, on_delete=models.PROTECT, related_name="risks")
    office = models.ForeignKey("organization.Office", on_delete=models.PROTECT, related_name="risks")
    risk_owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="owned_risks")
    date_identified = models.DateField()
    cause = models.TextField()
    potential_impact = models.TextField()
    existing_controls = models.TextField(blank=True)
    likelihood = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    impact = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    inherent_risk_score = models.PositiveSmallIntegerField(editable=False)
    inherent_risk_level = models.CharField(max_length=20, editable=False, db_index=True)
    residual_likelihood = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    residual_impact = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    residual_risk_score = models.PositiveSmallIntegerField(editable=False)
    residual_risk_level = models.CharField(max_length=20, editable=False, db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN, db_index=True)
    review_date = models.DateField()
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="created_risks")

class RiskMitigationAction(UUIDTimeStampedModel):
    class Status(models.TextChoices):
        NOT_STARTED="NOT_STARTED","Not Started"; IN_PROGRESS="IN_PROGRESS","In Progress"; COMPLETED="COMPLETED","Completed"; OVERDUE="OVERDUE","Overdue"; CANCELLED="CANCELLED","Cancelled"
    risk = models.ForeignKey(Risk, on_delete=models.CASCADE, related_name="mitigations")
    action = models.TextField()
    responsible_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    responsible_office = models.ForeignKey("organization.Office", on_delete=models.PROTECT)
    target_date = models.DateField(db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NOT_STARTED, db_index=True)
    completion_percentage = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    remarks = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

class RiskIndicator(UUIDTimeStampedModel):
    class Status(models.TextChoices):
        NORMAL="NORMAL","Normal"; WARNING="WARNING","Warning"; CRITICAL="CRITICAL","Critical"
    risk = models.ForeignKey(Risk, on_delete=models.CASCADE, related_name="indicators")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    current_value = models.DecimalField(max_digits=14, decimal_places=2)
    warning_threshold = models.DecimalField(max_digits=14, decimal_places=2)
    critical_threshold = models.DecimalField(max_digits=14, decimal_places=2)
    unit = models.CharField(max_length=50)
    measurement_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.NORMAL, db_index=True)


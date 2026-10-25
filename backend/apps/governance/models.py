from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone
from apps.core.models import UUIDTimeStampedModel

class StrategicObjective(UUIDTimeStampedModel):
    class Status(models.TextChoices):
        DRAFT="DRAFT","Draft"; ACTIVE="ACTIVE","Active"; AT_RISK="AT_RISK","At Risk"; COMPLETED="COMPLETED","Completed"; CANCELLED="CANCELLED","Cancelled"
    class Priority(models.TextChoices):
        LOW="LOW","Low"; MEDIUM="MEDIUM","Medium"; HIGH="HIGH","High"; CRITICAL="CRITICAL","Critical"
    objective_code = models.CharField(max_length=30, unique=True)
    title = models.CharField(max_length=255)
    description = models.TextField()
    responsible_office = models.ForeignKey("organization.Office", on_delete=models.PROTECT)
    start_date = models.DateField()
    target_date = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.DRAFT, db_index=True)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    progress_percentage = models.PositiveSmallIntegerField(default=0, validators=[MaxValueValidator(100)])
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)

class GovernanceKPI(UUIDTimeStampedModel):
    class Status(models.TextChoices):
        ON_TRACK="ON_TRACK","On Track"; WATCH="WATCH","Watch"; AT_RISK="AT_RISK","At Risk"
    strategic_objective = models.ForeignKey(StrategicObjective, on_delete=models.CASCADE, related_name="kpis")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    unit_of_measure = models.CharField(max_length=50)
    baseline_value = models.DecimalField(max_digits=14, decimal_places=2)
    target_value = models.DecimalField(max_digits=14, decimal_places=2)
    current_value = models.DecimalField(max_digits=14, decimal_places=2)
    reporting_frequency = models.CharField(max_length=50)
    warning_threshold = models.DecimalField(max_digits=14, decimal_places=2)
    critical_threshold = models.DecimalField(max_digits=14, decimal_places=2)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ON_TRACK, db_index=True)
    last_updated_at = models.DateTimeField(auto_now=True)

class GovernanceDecision(UUIDTimeStampedModel):
    class Status(models.TextChoices):
        PENDING="PENDING","Pending"; IN_PROGRESS="IN_PROGRESS","In Progress"; COMPLETED="COMPLETED","Completed"; OVERDUE="OVERDUE","Overdue"; CANCELLED="CANCELLED","Cancelled"
    decision_number = models.CharField(max_length=30, unique=True)
    source = models.CharField(max_length=100)
    meeting_reference = models.CharField(max_length=100, blank=True)
    decision_date = models.DateField()
    subject = models.CharField(max_length=255)
    description = models.TextField()
    responsible_office = models.ForeignKey("organization.Office", on_delete=models.PROTECT)
    responsible_person = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="governance_decisions")
    required_action = models.TextField()
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING, db_index=True)
    completion_date = models.DateField(null=True, blank=True)
    remarks = models.TextField(blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="created_governance_decisions")
    @property
    def effective_status(self):
        if self.status not in [self.Status.COMPLETED, self.Status.CANCELLED] and self.deadline < timezone.localdate(): return self.Status.OVERDUE
        return self.status


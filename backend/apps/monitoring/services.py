import logging
from django.db import transaction
from .models import MonitoringAlert
from .rules import CoreRules
logger = logging.getLogger(__name__)

@transaction.atomic
def run_monitoring():
    created = 0
    for condition in CoreRules().evaluate():
        fingerprint = f"{condition.alert_type}:{condition.entity.__class__.__name__}:{condition.entity.pk}"
        _, was_created = MonitoringAlert.objects.get_or_create(fingerprint=fingerprint, status="OPEN", defaults={
            "alert_type": condition.alert_type, "severity": condition.severity, "title": condition.title,
            "description": condition.description, "related_entity_type": condition.entity.__class__.__name__,
            "related_entity_id": str(condition.entity.pk), "office": condition.office, "due_date": condition.due_date})
        created += int(was_created)
    logger.info("GRACE monitoring completed: %s new alerts", created)
    return created


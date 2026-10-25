from apps.audit.models import AuditLog
from .models import ActivityHistory

def record_activity(*, actor, instance, action, description, changes=None, request=None):
    entity_type, entity_id = instance.__class__.__name__, str(instance.pk)
    ActivityHistory.objects.create(entity_type=entity_type, entity_id=entity_id, action=action, description=description, actor=actor, changes=changes or {})
    AuditLog.objects.create(user=actor, action=action, entity_type=entity_type, entity_id=entity_id, description=description,
        after_values=changes or {}, ip_address=(request.META.get("REMOTE_ADDR") if request else None), user_agent=(request.META.get("HTTP_USER_AGENT", "")[:500] if request else ""))


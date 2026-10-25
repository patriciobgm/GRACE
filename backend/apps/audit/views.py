from rest_framework import viewsets
from .models import AuditLog
from .serializers import AuditLogSerializer
class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset=AuditLog.objects.select_related("user"); serializer_class=AuditLogSerializer
    filterset_fields=["action","entity_type","user"]; search_fields=["description","entity_id"]; ordering_fields=["timestamp","action"]


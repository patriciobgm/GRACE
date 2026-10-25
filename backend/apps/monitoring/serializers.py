from django.utils import timezone
from rest_framework import serializers
from .models import MonitoringAlert
class MonitoringAlertSerializer(serializers.ModelSerializer):
    office_name=serializers.CharField(source="office.name",read_only=True)
    class Meta: model=MonitoringAlert; fields="__all__"; read_only_fields=["alert_type","severity","title","description","related_entity_type","related_entity_id","office","generated_at","due_date","fingerprint","acknowledged_by","acknowledged_at","resolved_at"]
    def update(self,instance,data):
        status=data.get("status",instance.status)
        if status=="ACKNOWLEDGED" and instance.status=="OPEN": instance.acknowledged_by=self.context["request"].user; instance.acknowledged_at=timezone.now()
        if status=="RESOLVED": instance.resolved_at=timezone.now()
        instance.status=status; instance.save(); return instance


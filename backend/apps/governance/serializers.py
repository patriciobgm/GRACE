from rest_framework import serializers
from .models import StrategicObjective, GovernanceKPI, GovernanceDecision
from .services import update_kpi_status
class StrategicObjectiveSerializer(serializers.ModelSerializer):
    class Meta: model=StrategicObjective; fields="__all__"; read_only_fields=["created_by"]
    def validate(self,data):
        if data.get("target_date",getattr(self.instance,"target_date",None)) < data.get("start_date",getattr(self.instance,"start_date",None)): raise serializers.ValidationError("Target date cannot precede start date.")
        return data
class GovernanceKPISerializer(serializers.ModelSerializer):
    class Meta: model=GovernanceKPI; fields="__all__"; read_only_fields=["status","last_updated_at"]
    def create(self,data): return update_kpi_status(GovernanceKPI.objects.create(**data))
    def update(self,instance,data):
        for k,v in data.items(): setattr(instance,k,v)
        return update_kpi_status(instance)
class GovernanceDecisionSerializer(serializers.ModelSerializer):
    effective_status=serializers.CharField(read_only=True)
    class Meta: model=GovernanceDecision; fields="__all__"; read_only_fields=["created_by"]
    def validate(self,data):
        if data.get("status",getattr(self.instance,"status",None)) == "COMPLETED" and not data.get("completion_date",getattr(self.instance,"completion_date",None)): raise serializers.ValidationError("Completion date is required when completed.")
        return data


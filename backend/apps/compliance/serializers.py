from django.utils import timezone
from rest_framework import serializers
from .models import ComplianceObligation,ComplianceEvidence,ComplianceFinding,CorrectiveAction
class ComplianceObligationSerializer(serializers.ModelSerializer):
    office_name=serializers.CharField(source="responsible_office.name",read_only=True)
    class Meta: model=ComplianceObligation; fields="__all__"; read_only_fields=["created_by"]
class ComplianceEvidenceSerializer(serializers.ModelSerializer):
    class Meta: model=ComplianceEvidence; fields="__all__"; read_only_fields=["submitted_by","submitted_at","reviewed_by","reviewed_at"]
    def validate(self,data):
        status=data.get("review_status",getattr(self.instance,"review_status",None))
        if status in ["REJECTED","NEEDS_REVISION"] and not data.get("review_remarks",getattr(self.instance,"review_remarks",None)): raise serializers.ValidationError("Review remarks are required.")
        return data
    def update(self,instance,data):
        if "review_status" in data and data["review_status"] != "PENDING_REVIEW": data.update(reviewed_by=self.context["request"].user,reviewed_at=timezone.now())
        return super().update(instance,data)
class ComplianceFindingSerializer(serializers.ModelSerializer):
    class Meta: model=ComplianceFinding; fields="__all__"; read_only_fields=["identified_by"]
    def validate(self,data):
        status=data.get("status",getattr(self.instance,"status",None))
        if status=="CLOSED":
            if not data.get("closure_remarks",getattr(self.instance,"closure_remarks",None)): raise serializers.ValidationError("Closure remarks are required.")
            data.setdefault("closed_by",self.context["request"].user); data.setdefault("closed_at",timezone.now())
        return data
class CorrectiveActionSerializer(serializers.ModelSerializer):
    class Meta: model=CorrectiveAction; fields="__all__"
    def validate(self,data):
        if data.get("status",getattr(self.instance,"status",None))=="COMPLETED" and not data.get("completed_at",getattr(self.instance,"completed_at",None)): data["completed_at"]=timezone.now()
        return data


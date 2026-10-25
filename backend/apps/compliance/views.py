from rest_framework import viewsets
from apps.core.services import record_activity
from .models import ComplianceObligation,ComplianceEvidence,ComplianceFinding,CorrectiveAction
from .serializers import ComplianceObligationSerializer,ComplianceEvidenceSerializer,ComplianceFindingSerializer,CorrectiveActionSerializer
class TrackedViewSet(viewsets.ModelViewSet):
    def perform_create(self,serializer):
        field_names=[f.name for f in serializer.Meta.model._meta.fields]; kwargs={}
        if "created_by" in field_names: kwargs["created_by"]=self.request.user
        if "submitted_by" in field_names: kwargs["submitted_by"]=self.request.user
        if "identified_by" in field_names: kwargs["identified_by"]=self.request.user
        obj=serializer.save(**kwargs); record_activity(actor=self.request.user,instance=obj,action="CREATE",description=f"Created {obj.__class__.__name__}",request=self.request)
    def perform_update(self,serializer):
        obj=serializer.save(); record_activity(actor=self.request.user,instance=obj,action="UPDATE",description=f"Updated {obj.__class__.__name__}",request=self.request)
class ComplianceObligationViewSet(TrackedViewSet):
    queryset=ComplianceObligation.objects.select_related("responsible_office","responsible_person","created_by"); serializer_class=ComplianceObligationSerializer
    filterset_fields=["source_type","responsible_office","responsible_person","status","risk_level"]; search_fields=["obligation_code","title","description","source_reference","requirements"]; ordering_fields=["due_date","risk_level","created_at"]
class ComplianceEvidenceViewSet(TrackedViewSet):
    queryset=ComplianceEvidence.objects.select_related("obligation","submitted_by","reviewed_by","attachment"); serializer_class=ComplianceEvidenceSerializer
    filterset_fields=["obligation","review_status","submitted_by"]; search_fields=["title","description","review_remarks"]; ordering_fields=["submitted_at","reviewed_at"]
class ComplianceFindingViewSet(TrackedViewSet):
    queryset=ComplianceFinding.objects.select_related("obligation","identified_by","responsible_office"); serializer_class=ComplianceFindingSerializer
    filterset_fields=["obligation","severity","status","responsible_office"]; search_fields=["finding_number","description"]; ordering_fields=["due_date","date_identified","severity"]
class CorrectiveActionViewSet(TrackedViewSet):
    queryset=CorrectiveAction.objects.select_related("finding","assigned_to","responsible_office"); serializer_class=CorrectiveActionSerializer
    filterset_fields=["finding","assigned_to","responsible_office","status"]; search_fields=["action","remarks"]; ordering_fields=["target_date","progress_percentage"]


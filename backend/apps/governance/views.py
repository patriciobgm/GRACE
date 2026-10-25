from rest_framework import viewsets
from apps.accounts.permissions import IsGRCManagerOrReadOnly
from apps.core.services import record_activity
from .models import StrategicObjective, GovernanceKPI, GovernanceDecision
from .serializers import StrategicObjectiveSerializer, GovernanceKPISerializer, GovernanceDecisionSerializer
class TrackedViewSet(viewsets.ModelViewSet):
    permission_classes=[IsGRCManagerOrReadOnly]
    def perform_create(self,serializer):
        kwargs={"created_by":self.request.user} if "created_by" in [f.name for f in serializer.Meta.model._meta.fields] else {}
        obj=serializer.save(**kwargs); record_activity(actor=self.request.user,instance=obj,action="CREATE",description=f"Created {obj.__class__.__name__}",request=self.request)
    def perform_update(self,serializer):
        obj=serializer.save(); record_activity(actor=self.request.user,instance=obj,action="UPDATE",description=f"Updated {obj.__class__.__name__}",request=self.request)
class StrategicObjectiveViewSet(TrackedViewSet):
    queryset=StrategicObjective.objects.select_related("responsible_office","created_by"); serializer_class=StrategicObjectiveSerializer
    filterset_fields=["status","priority","responsible_office"]; search_fields=["objective_code","title","description"]; ordering_fields=["target_date","priority","created_at"]
class GovernanceKPIViewSet(TrackedViewSet):
    queryset=GovernanceKPI.objects.select_related("strategic_objective"); serializer_class=GovernanceKPISerializer
    filterset_fields=["status","strategic_objective"]; search_fields=["name","description"]
class GovernanceDecisionViewSet(TrackedViewSet):
    queryset=GovernanceDecision.objects.select_related("responsible_office","responsible_person","created_by"); serializer_class=GovernanceDecisionSerializer
    filterset_fields=["status","responsible_office","responsible_person"]; search_fields=["decision_number","subject","description","required_action"]; ordering_fields=["deadline","decision_date","created_at"]


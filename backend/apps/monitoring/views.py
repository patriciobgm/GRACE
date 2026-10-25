from rest_framework import decorators,response,viewsets,serializers
from apps.accounts.permissions import IsGRCAdministrator
from apps.core.services import record_activity
from .models import MonitoringAlert
from .serializers import MonitoringAlertSerializer
from .services import run_monitoring
class RunMonitoringSerializer(serializers.Serializer):
    pass
class MonitoringAlertViewSet(viewsets.ModelViewSet):
    queryset=MonitoringAlert.objects.select_related("office","acknowledged_by"); serializer_class=MonitoringAlertSerializer
    http_method_names=["get","patch","head","options"]; filterset_fields=["status","severity","alert_type","office"]; search_fields=["title","description"]; ordering_fields=["generated_at","severity","due_date"]
class RunMonitoringViewSet(viewsets.ViewSet):
    permission_classes=[IsGRCAdministrator]
    serializer_class=RunMonitoringSerializer
    def create(self,request):
        count=run_monitoring(); record_activity(actor=request.user,instance=request.user,action="MONITORING_RUN",description=f"Monitoring generated {count} new alerts",request=request)
        return response.Response({"created_alerts":count,"message":"Deterministic monitoring completed."})


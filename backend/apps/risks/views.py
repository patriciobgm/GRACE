from django.db.models import Count
from rest_framework import decorators,response,viewsets
from apps.accounts.permissions import IsGRCManagerOrReadOnly
from apps.core.services import record_activity
from .models import RiskCategory,Risk,RiskMitigationAction,RiskIndicator
from .serializers import RiskCategorySerializer,RiskSerializer,RiskMitigationSerializer,RiskIndicatorSerializer
class RiskCategoryViewSet(viewsets.ModelViewSet):
    queryset=RiskCategory.objects.all(); serializer_class=RiskCategorySerializer; permission_classes=[IsGRCManagerOrReadOnly]; search_fields=["name","description"]; filterset_fields=["is_active"]
class RiskViewSet(viewsets.ModelViewSet):
    queryset=Risk.objects.none()
    serializer_class=RiskSerializer; filterset_fields=["office","category","status","inherent_risk_level","date_identified","likelihood","impact"]; search_fields=["risk_code","title","description","cause","potential_impact"]; ordering_fields=["risk_code","date_identified","review_date","inherent_risk_score","created_at"]
    def get_queryset(self):
        qs=Risk.objects.select_related("category","office","risk_owner","created_by")
        user=self.request.user
        if getattr(self,"swagger_fake_view",False) or not user.is_authenticated: return qs.none()
        if user.role=="RISK_OWNER" and user.office_id: qs=qs.filter(office=user.office)
        return qs
    def perform_create(self,serializer):
        obj=serializer.save(created_by=self.request.user); record_activity(actor=self.request.user,instance=obj,action="RISK_CREATED",description=f"Created {obj.risk_code} with score {obj.inherent_risk_score} ({obj.inherent_risk_level})",request=self.request)
    def perform_update(self,serializer):
        old={"score":serializer.instance.inherent_risk_score,"level":serializer.instance.inherent_risk_level}; obj=serializer.save(); record_activity(actor=self.request.user,instance=obj,action="RISK_UPDATED",description=f"Updated {obj.risk_code}",changes={"before":old,"after":{"score":obj.inherent_risk_score,"level":obj.inherent_risk_level}},request=self.request)
    @decorators.action(detail=False,methods=["get"],url_path="heat-map")
    def heat_map(self,request):
        qs=self.filter_queryset(self.get_queryset()); grouped={(row["likelihood"],row["impact"]):row["count"] for row in qs.values("likelihood","impact").annotate(count=Count("id"))}
        cells=[{"likelihood":l,"impact":i,"score":l*i,"count":grouped.get((l,i),0)} for l in range(1,6) for i in range(1,6)]
        return response.Response({"matrix_size":5,"cells":cells,"total":qs.count(),"legend":[{"level":"LOW","min":1,"max":4},{"level":"MODERATE","min":5,"max":9},{"level":"HIGH","min":10,"max":16},{"level":"CRITICAL","min":17,"max":25}]})
class RiskMitigationViewSet(viewsets.ModelViewSet):
    queryset=RiskMitigationAction.objects.select_related("risk","responsible_user","responsible_office"); serializer_class=RiskMitigationSerializer
    filterset_fields=["risk","status","responsible_office","responsible_user"]; search_fields=["action","remarks"]; ordering_fields=["target_date","created_at"]
class RiskIndicatorViewSet(viewsets.ModelViewSet):
    queryset=RiskIndicator.objects.select_related("risk"); serializer_class=RiskIndicatorSerializer
    filterset_fields=["risk","status"]; search_fields=["name","description"]; ordering_fields=["measurement_date","current_value"]


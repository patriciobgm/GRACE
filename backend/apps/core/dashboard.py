from datetime import timedelta
from django.db.models import Count
from django.utils import timezone
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework import serializers
from apps.ai_support.models import AIAnalysis
from apps.compliance.models import ComplianceObligation,ComplianceFinding,CorrectiveAction
from apps.governance.models import StrategicObjective,GovernanceKPI,GovernanceDecision
from apps.monitoring.models import MonitoringAlert
from apps.risks.models import Risk,RiskMitigationAction

class DashboardView(APIView):
    @extend_schema(responses=serializers.DictField())
    def get(self,request):
        today=timezone.localdate(); active_risks=Risk.objects.exclude(status="CLOSED")
        heat={(x["likelihood"],x["impact"]):x["count"] for x in active_risks.values("likelihood","impact").annotate(count=Count("id"))}
        data={
          "governance":{"active_objectives":StrategicObjective.objects.filter(status="ACTIVE").count(),"objectives_at_risk":StrategicObjective.objects.filter(status="AT_RISK").count(),"overdue_decisions":GovernanceDecision.objects.filter(deadline__lt=today).exclude(status__in=["COMPLETED","CANCELLED"]).count(),"kpi_status":list(GovernanceKPI.objects.values("status").annotate(count=Count("id")))},
          "risk":{"active_risks":active_risks.count(),"critical_risks":active_risks.filter(inherent_risk_level="CRITICAL").count(),"high_risks":active_risks.filter(inherent_risk_level="HIGH").count(),"overdue_mitigations":RiskMitigationAction.objects.filter(target_date__lt=today).exclude(status__in=["COMPLETED","CANCELLED"]).count(),"heat_map":[{"likelihood":l,"impact":i,"count":heat.get((l,i),0)} for l in range(1,6) for i in range(1,6)],"by_category":list(active_risks.values("category__name").annotate(count=Count("id"))),"by_office":list(active_risks.values("office__name").annotate(count=Count("id")))},
          "compliance":{"active_obligations":ComplianceObligation.objects.filter(status="ACTIVE").count(),"due_within_30_days":ComplianceObligation.objects.filter(due_date__range=(today,today+timedelta(days=30))).count(),"overdue_obligations":ComplianceObligation.objects.filter(due_date__lt=today).exclude(status__in=["COMPLETED","CANCELLED"]).count(),"open_findings":ComplianceFinding.objects.exclude(status="CLOSED").count(),"critical_findings":ComplianceFinding.objects.exclude(status="CLOSED").filter(severity="CRITICAL").count(),"overdue_corrective_actions":CorrectiveAction.objects.filter(target_date__lt=today).exclude(status__in=["COMPLETED","CANCELLED"]).count()},
          "monitoring":{"open_alerts":MonitoringAlert.objects.filter(status="OPEN").count(),"critical_alerts":MonitoringAlert.objects.filter(status="OPEN",severity="CRITICAL").count(),"recent_alerts":list(MonitoringAlert.objects.filter(status="OPEN").values("id","severity","title","generated_at")[:5])},
          "ai":{"recent_analyses":list(AIAnalysis.objects.values("id","analysis_type","human_review_status","requested_at")[:5]),"pending_human_review":AIAnalysis.objects.filter(human_review_status="PENDING_REVIEW").count()}}
        return Response(data)


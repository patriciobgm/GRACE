import csv
from django.http import HttpResponse
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import serializers
from drf_spectacular.utils import extend_schema
from apps.accounts.permissions import IsGRCAdministrator
from apps.compliance.models import ComplianceObligation,ComplianceFinding,CorrectiveAction
from apps.governance.models import StrategicObjective,GovernanceDecision
from apps.risks.models import Risk,RiskMitigationAction

REPORTS={
 "governance-performance":(StrategicObjective,["objective_code","title","status","priority","progress_percentage","target_date"]),
 "decision-accountability":(GovernanceDecision,["decision_number","subject","status","deadline","responsible_office__name"]),
 "institutional-risk-register":(Risk,["risk_code","title","inherent_risk_score","inherent_risk_level","status","office__name","review_date"]),
 "risk-mitigation-status":(RiskMitigationAction,["risk__risk_code","action","status","completion_percentage","target_date"]),
 "compliance-obligations":(ComplianceObligation,["obligation_code","title","status","risk_level","due_date","responsible_office__name"]),
 "compliance-findings":(ComplianceFinding,["finding_number","description","severity","status","due_date"]),
 "corrective-actions":(CorrectiveAction,["finding__finding_number","action","status","progress_percentage","target_date"]),
}
class ReportListView(APIView):
    @extend_schema(responses=serializers.ListField(child=serializers.DictField()))
    def get(self,request): return Response([{"slug":slug,"title":slug.replace("-"," ").title(),"formats":["json","csv","print"]} for slug in REPORTS])
class ReportExportView(APIView):
    permission_classes=[IsGRCAdministrator]
    @extend_schema(responses=serializers.DictField())
    def get(self,request,slug):
        if slug not in REPORTS: return Response({"detail":"Unknown report."},status=404)
        model,fields=REPORTS[slug]; rows=list(model.objects.values(*fields)); fmt=request.query_params.get("format","json")
        if fmt!="csv": return Response({"report":slug,"generated_for":"GRACE","results":rows})
        out=HttpResponse(content_type="text/csv"); out["Content-Disposition"]=f'attachment; filename="grace-{slug}.csv"'; writer=csv.DictWriter(out,fieldnames=fields); writer.writeheader(); writer.writerows(rows); return out


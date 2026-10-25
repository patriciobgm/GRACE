from datetime import timedelta
from decimal import Decimal
from django.core.management.base import BaseCommand
from django.utils import timezone
from apps.accounts.models import User
from apps.organization.models import Office
from apps.governance.models import StrategicObjective,GovernanceKPI,GovernanceDecision
from apps.governance.services import update_kpi_status
from apps.risks.models import RiskCategory,Risk,RiskMitigationAction,RiskIndicator
from apps.risks.services import assess_risk,update_kri_status
from apps.compliance.models import ComplianceObligation,ComplianceFinding,CorrectiveAction
from apps.monitoring.services import run_monitoring

class Command(BaseCommand):
    help="Create explicitly labeled GRACE DEMO / SAMPLE DATA"
    def handle(self,*args,**options):
        today=timezone.localdate(); password="GraceDemo2026!"
        offices=[]
        for code,name in [("DEMO-ADM","DEMO Administration Office"),("DEMO-GRC","DEMO Governance and Compliance Office"),("DEMO-ACA","DEMO Academic Affairs Office")]:
            office,_=Office.objects.get_or_create(code=code,defaults={"name":name,"description":"DEMO / SAMPLE DATA — not an actual LPC organizational record."}); offices.append(office)
        roles=[("sysadmin","SYSTEM_ADMIN",offices[0]),("grcadmin","GRC_ADMIN",offices[1]),("executive","EXECUTIVE",offices[0]),("compliance","COMPLIANCE_OFFICER",offices[1]),("riskowner","RISK_OWNER",offices[2]),("auditor","AUDITOR",offices[1])]
        users={}
        for username,role,office in roles:
            user,created=User.objects.get_or_create(username=username,defaults={"email":f"{username}@demo.grace.local","first_name":"DEMO","last_name":role.replace("_"," ").title(),"role":role,"office":office})
            if created: user.set_password(password); user.save()
            users[role]=user
        offices[0].office_head=users["EXECUTIVE"]; offices[0].save(); offices[1].office_head=users["GRC_ADMIN"]; offices[1].save(); offices[2].office_head=users["RISK_OWNER"]; offices[2].save()
        objective,_=StrategicObjective.objects.get_or_create(objective_code="DEMO-OBJ-2026-0001",defaults={"title":"Strengthen Institutional Compliance and Governance Monitoring (DEMO)","description":"DEMO / SAMPLE DATA for thesis defense.","responsible_office":offices[1],"start_date":today-timedelta(days=30),"target_date":today+timedelta(days=180),"status":"AT_RISK","priority":"HIGH","progress_percentage":42,"created_by":users["GRC_ADMIN"]})
        kpi,_=GovernanceKPI.objects.get_or_create(strategic_objective=objective,name="DEMO Timely GRC reviews",defaults={"description":"DEMO / SAMPLE KPI","unit_of_measure":"percent","baseline_value":40,"target_value":90,"current_value":55,"warning_threshold":70,"critical_threshold":50,"reporting_frequency":"Monthly"}); update_kpi_status(kpi)
        GovernanceDecision.objects.get_or_create(decision_number="DEMO-DEC-2026-0001",defaults={"source":"DEMO Executive Committee","meeting_reference":"DEMO-MTG-001","decision_date":today-timedelta(days=45),"subject":"Complete GRC control inventory (DEMO)","description":"DEMO / SAMPLE DATA","responsible_office":offices[1],"responsible_person":users["GRC_ADMIN"],"required_action":"Document sample controls for the thesis demonstration.","deadline":today-timedelta(days=5),"status":"IN_PROGRESS","created_by":users["GRC_ADMIN"]})
        category,_=RiskCategory.objects.get_or_create(name="DEMO Regulatory and Compliance",defaults={"description":"DEMO / SAMPLE risk category"})
        risk,created=Risk.objects.get_or_create(risk_code="DEMO-RSK-2026-0001",defaults={"title":"Delayed submission of regulatory compliance documents (DEMO)","description":"DEMO / SAMPLE DATA only.","category":category,"office":offices[2],"risk_owner":users["RISK_OWNER"],"date_identified":today-timedelta(days=60),"cause":"Sample coordination delays","potential_impact":"Sample missed institutional deadline","existing_controls":"Sample review calendar","likelihood":4,"impact":4,"residual_likelihood":3,"residual_impact":4,"review_date":today-timedelta(days=1),"status":"TREATING","created_by":users["RISK_OWNER"],"inherent_risk_score":16,"inherent_risk_level":"HIGH","residual_risk_score":12,"residual_risk_level":"HIGH"})
        if created: assess_risk(risk)
        RiskMitigationAction.objects.get_or_create(risk=risk,action="Complete sample submission checklist and management review.",defaults={"responsible_user":users["RISK_OWNER"],"responsible_office":offices[2],"target_date":today-timedelta(days=2),"status":"IN_PROGRESS","completion_percentage":60,"remarks":"DEMO / SAMPLE DATA"})
        kri,_=RiskIndicator.objects.get_or_create(risk=risk,name="Days remaining before sample deadline",defaults={"description":"DEMO / SAMPLE indicator","current_value":2,"warning_threshold":5,"critical_threshold":2,"unit":"days","measurement_date":today}); update_kri_status(kri)
        obligation,_=ComplianceObligation.objects.get_or_create(obligation_code="DEMO-CMP-2026-0001",defaults={"title":"DEMO annual institutional document review","description":"DEMO / SAMPLE DATA — not a real legal or LPC obligation.","source_type":"INTERNAL_STANDARD","source_reference":"DEMO-REF-001","regulatory_body":"DEMO only","responsible_office":offices[1],"responsible_person":users["COMPLIANCE_OFFICER"],"frequency":"Annual","effective_date":today-timedelta(days=90),"due_date":today-timedelta(days=3),"status":"ACTIVE","risk_level":"HIGH","requirements":"DEMO evidence checklist","notes":"Not an actual compliance determination.","created_by":users["COMPLIANCE_OFFICER"]})
        finding,_=ComplianceFinding.objects.get_or_create(finding_number="DEMO-FND-2026-0001",defaults={"obligation":obligation,"description":"DEMO evidence package requires human review.","severity":"HIGH","date_identified":today-timedelta(days=14),"identified_by":users["COMPLIANCE_OFFICER"],"responsible_office":offices[2],"due_date":today+timedelta(days=14),"status":"IN_PROGRESS"})
        CorrectiveAction.objects.get_or_create(finding=finding,action="Complete the DEMO evidence index.",defaults={"assigned_to":users["RISK_OWNER"],"responsible_office":offices[2],"target_date":today-timedelta(days=1),"progress_percentage":50,"status":"IN_PROGRESS","remarks":"DEMO / SAMPLE DATA"})
        run_monitoring()
        self.stdout.write(self.style.SUCCESS(f"GRACE DEMO / SAMPLE DATA ready. Accounts: sysadmin, grcadmin, executive, compliance, riskowner, auditor. Development password: {password}"))


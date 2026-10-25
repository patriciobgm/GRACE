from datetime import timedelta
from django.db import transaction
from django.db.models import Q
from django.utils import timezone
from apps.compliance.models import ComplianceObligation, ComplianceFinding, CorrectiveAction
from apps.governance.models import GovernanceDecision, GovernanceKPI
from apps.monitoring.models import MonitoringAlert
from apps.risks.models import Risk, RiskMitigationAction, RiskIndicator
from apps.core.services import record_activity
from .models import AIAnalysis
from .providers import get_provider

def executive_facts():
    today = timezone.localdate()
    return {"critical_risks": Risk.objects.exclude(status="CLOSED").filter(inherent_risk_level="CRITICAL").count(),
        "high_risks": Risk.objects.exclude(status="CLOSED").filter(inherent_risk_level="HIGH").count(),
        "overdue_mitigations": RiskMitigationAction.objects.filter(target_date__lt=today).exclude(status__in=["COMPLETED","CANCELLED"]).count(),
        "warning_critical_kris": RiskIndicator.objects.filter(status__in=["WARNING","CRITICAL"]).count(),
        "compliance_due_30_days": ComplianceObligation.objects.filter(due_date__gte=today, due_date__lte=today+timedelta(days=30)).count(),
        "overdue_obligations": ComplianceObligation.objects.filter(due_date__lt=today).exclude(status__in=["COMPLETED","CANCELLED"]).count(),
        "open_findings": ComplianceFinding.objects.exclude(status="CLOSED").count(),
        "overdue_corrective_actions": CorrectiveAction.objects.filter(target_date__lt=today).exclude(status__in=["COMPLETED","CANCELLED"]).count(),
        "kpis_at_risk": GovernanceKPI.objects.filter(status="AT_RISK").count(),
        "governance_actions_overdue": GovernanceDecision.objects.filter(deadline__lt=today).exclude(status__in=["COMPLETED","CANCELLED"]).count(),
        "critical_alerts": MonitoringAlert.objects.filter(status="OPEN", severity="CRITICAL").count()}

@transaction.atomic
def generate_analysis(*, user, analysis_type, entity=None, request=None):
    if analysis_type == "EXECUTIVE_BRIEF": facts, refs = executive_facts(), []
    elif analysis_type == "RISK" and isinstance(entity, Risk):
        facts = {"risk_code":entity.risk_code,"title":entity.title,"description":entity.description,"cause":entity.cause,"potential_impact":entity.potential_impact,"existing_controls":entity.existing_controls,"score":entity.inherent_risk_score,"level":entity.inherent_risk_level,"mitigations":list(entity.mitigations.values("action","status","target_date")),"indicators":list(entity.indicators.values("name","current_value","status"))}; refs=[entity.risk_code]
    elif analysis_type == "COMPLIANCE" and isinstance(entity, ComplianceObligation):
        facts={"obligation_code":entity.obligation_code,"title":entity.title,"description":entity.description,"requirements":entity.requirements,"due_date":entity.due_date,"status":entity.status,"evidence":list(entity.evidence.values("title","review_status")),"findings":list(entity.findings.values("finding_number","severity","status"))}; refs=[entity.obligation_code]
    else: raise ValueError("Analysis type and entity do not match")
    provider=get_provider(); output=provider.generate(analysis_type=analysis_type,facts=facts)
    analysis=AIAnalysis.objects.create(analysis_type=analysis_type,related_entity_type=entity.__class__.__name__ if entity else "",related_entity_id=str(entity.pk) if entity else "",requested_by=user,input_snapshot=facts,provider=provider.name,model_name=getattr(provider,"model_name", "mock-advisory-v1"),generated_response=output,evidence_references=refs)
    record_activity(actor=user,instance=analysis,action="AI_ANALYSIS_GENERATED",description=f"Generated {analysis_type} advisory analysis",request=request)
    return analysis

@transaction.atomic
def review_analysis(*, analysis, reviewer, status, comments, final_note="", request=None):
    if analysis.human_review_status != "PENDING_REVIEW": raise ValueError("This analysis has already been reviewed")
    if status not in ["ACCEPTED","ACCEPTED_WITH_MODIFICATION","REJECTED"]: raise ValueError("Invalid review transition")
    if status == "ACCEPTED_WITH_MODIFICATION" and not final_note.strip(): raise ValueError("A final management note is required")
    analysis.human_review_status=status; analysis.reviewed_by=reviewer; analysis.reviewed_at=timezone.now(); analysis.reviewer_comments=comments; analysis.final_management_note=final_note; analysis.save()
    record_activity(actor=reviewer,instance=analysis,action="AI_ANALYSIS_REVIEWED",description=f"AI advisory {status.lower().replace('_',' ')}",request=request)
    return analysis


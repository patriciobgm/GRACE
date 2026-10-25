from dataclasses import dataclass
from datetime import timedelta
from django.utils import timezone
from apps.governance.models import GovernanceDecision, GovernanceKPI
from apps.risks.models import Risk, RiskIndicator, RiskMitigationAction
from apps.compliance.models import ComplianceObligation, ComplianceFinding, CorrectiveAction

@dataclass
class AlertCondition:
    alert_type: str; severity: str; title: str; description: str; entity: object; office: object = None; due_date: object = None

class MonitoringRule:
    def evaluate(self): raise NotImplementedError

class CoreRules(MonitoringRule):
    def evaluate(self):
        today, conditions = timezone.localdate(), []
        for item in Risk.objects.filter(status__in=["OPEN","MONITORING","TREATING"], inherent_risk_level="CRITICAL"):
            conditions.append(AlertCondition("RISK_CRITICAL","CRITICAL","Critical risk requires review",f"{item.risk_code}: {item.title}",item,item.office,item.review_date))
        for item in Risk.objects.filter(status__in=["OPEN","MONITORING","TREATING"], review_date__lt=today):
            conditions.append(AlertCondition("RISK_REVIEW_OVERDUE","HIGH","Risk review overdue",f"Review is overdue for {item.risk_code}.",item,item.office,item.review_date))
        for item in RiskMitigationAction.objects.filter(target_date__lt=today).exclude(status__in=["COMPLETED","CANCELLED"]):
            conditions.append(AlertCondition("MITIGATION_OVERDUE","HIGH","Mitigation action is overdue",item.action,item,item.responsible_office,item.target_date))
        for item in RiskIndicator.objects.filter(status__in=["WARNING","CRITICAL"]):
            conditions.append(AlertCondition(f"KRI_{item.status}","CRITICAL" if item.status=="CRITICAL" else "WARNING",f"Risk indicator is {item.status.lower()}",item.name,item,item.risk.office,item.measurement_date))
        for item in GovernanceDecision.objects.filter(deadline__lt=today).exclude(status__in=["COMPLETED","CANCELLED"]):
            conditions.append(AlertCondition("GOVERNANCE_ACTION_OVERDUE","HIGH","Governance action overdue",item.subject,item,item.responsible_office,item.deadline))
        for item in GovernanceKPI.objects.filter(status="AT_RISK"):
            conditions.append(AlertCondition("KPI_AT_RISK","HIGH","KPI is at risk",item.name,item,item.strategic_objective.responsible_office))
        for item in ComplianceObligation.objects.filter(due_date__lt=today).exclude(status__in=["COMPLETED","CANCELLED"]):
            conditions.append(AlertCondition("COMPLIANCE_OVERDUE","CRITICAL","Compliance obligation overdue",item.title,item,item.responsible_office,item.due_date))
        for item in ComplianceObligation.objects.filter(due_date__range=(today,today+timedelta(days=30)),status="ACTIVE"):
            conditions.append(AlertCondition("COMPLIANCE_DUE_SOON","WARNING","Compliance obligation due soon",item.title,item,item.responsible_office,item.due_date))
        for item in ComplianceObligation.objects.filter(status="ACTIVE", evidence__isnull=True):
            conditions.append(AlertCondition("EVIDENCE_MISSING","WARNING","Compliance evidence missing",item.title,item,item.responsible_office,item.due_date))
        for item in CorrectiveAction.objects.filter(target_date__lt=today).exclude(status__in=["COMPLETED","CANCELLED"]):
            conditions.append(AlertCondition("CORRECTIVE_ACTION_OVERDUE","HIGH","Corrective action overdue",item.action,item,item.responsible_office,item.target_date))
        return conditions


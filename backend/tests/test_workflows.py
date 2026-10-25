from datetime import timedelta
import pytest
from django.utils import timezone
from rest_framework.test import APIClient
from apps.accounts.models import User
from apps.organization.models import Office
from apps.risks.models import RiskCategory,Risk,RiskMitigationAction
from apps.risks.services import assess_risk
from apps.monitoring.services import run_monitoring
from apps.monitoring.models import MonitoringAlert
from apps.ai_support.services import generate_analysis,review_analysis

@pytest.fixture
def setup_data(db):
    office=Office.objects.create(code="TEST",name="Test Office")
    user=User.objects.create_user(username="grc",email="grc@example.test",password="SecureTest123!",role="GRC_ADMIN",office=office)
    executive=User.objects.create_user(username="executive",email="executive@example.test",password="SecureTest123!",role="EXECUTIVE",office=office)
    category=RiskCategory.objects.create(name="Test Category")
    return office,user,executive,category

@pytest.mark.django_db
def test_login_and_current_user(setup_data):
    _,user,_,_=setup_data; client=APIClient(); token=client.post("/api/v1/auth/login/",{"username":"grc","password":"SecureTest123!"},format="json")
    assert token.status_code==200; client.credentials(HTTP_AUTHORIZATION=f"Bearer {token.data['access']}")
    assert client.get("/api/v1/auth/me/").data["id"]==str(user.id)

@pytest.mark.django_db
def test_risk_create_calculates_score(setup_data):
    office,user,_,category=setup_data; client=APIClient(); client.force_authenticate(user)
    result=client.post("/api/v1/risks/",{"risk_code":"RSK-TEST-1","title":"Test","description":"Test","category":str(category.id),"office":str(office.id),"risk_owner":str(user.id),"date_identified":str(timezone.localdate()),"cause":"Cause","potential_impact":"Impact","existing_controls":"Controls","likelihood":4,"impact":4,"residual_likelihood":3,"residual_impact":2,"status":"OPEN","review_date":str(timezone.localdate()+timedelta(days=30))},format="json")
    assert result.status_code==201; assert result.data["inherent_risk_score"]==16; assert result.data["inherent_risk_level"]=="HIGH"

@pytest.mark.django_db
def test_monitoring_deduplicates_active_alerts(setup_data):
    office,user,_,category=setup_data; risk=Risk.objects.create(risk_code="RSK-TEST-2",title="Critical",description="Test",category=category,office=office,risk_owner=user,date_identified=timezone.localdate(),cause="x",potential_impact="x",likelihood=5,impact=5,residual_likelihood=5,residual_impact=5,review_date=timezone.localdate()-timedelta(days=1),created_by=user,inherent_risk_score=25,inherent_risk_level="CRITICAL",residual_risk_score=25,residual_risk_level="CRITICAL")
    RiskMitigationAction.objects.create(risk=risk,action="Late",responsible_user=user,responsible_office=office,target_date=timezone.localdate()-timedelta(days=1))
    first=run_monitoring(); second=run_monitoring()
    assert first==3; assert second==0; assert MonitoringAlert.objects.count()==3

@pytest.mark.django_db
def test_ai_advisory_requires_single_human_review(setup_data):
    _,user,executive,_=setup_data; analysis=generate_analysis(user=user,analysis_type="EXECUTIVE_BRIEF")
    assert "requires human validation" in analysis.generated_response
    review_analysis(analysis=analysis,reviewer=executive,status="ACCEPTED",comments="Reviewed")
    with pytest.raises(ValueError): review_analysis(analysis=analysis,reviewer=executive,status="REJECTED",comments="Changed")


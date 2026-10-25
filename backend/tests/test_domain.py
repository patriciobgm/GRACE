from datetime import timedelta
from decimal import Decimal
import pytest
from django.utils import timezone
from apps.governance.services import calculate_kpi_status
from apps.risks.services import calculate_risk_score,determine_risk_level,calculate_kri_status

@pytest.mark.parametrize("likelihood,impact,score,level",[(1,1,1,"LOW"),(2,3,6,"MODERATE"),(4,4,16,"HIGH"),(5,5,25,"CRITICAL")])
def test_risk_matrix(likelihood,impact,score,level):
    assert calculate_risk_score(likelihood,impact)==score
    assert determine_risk_level(score)==level

def test_kpi_status_is_deterministic():
    assert calculate_kpi_status(95,90,70,50)=="ON_TRACK"
    assert calculate_kpi_status(75,90,70,50)=="WATCH"
    assert calculate_kpi_status(40,90,70,50)=="AT_RISK"

def test_kri_status_is_deterministic():
    assert calculate_kri_status(2,5,10)=="NORMAL"
    assert calculate_kri_status(7,5,10)=="WARNING"
    assert calculate_kri_status(11,5,10)=="CRITICAL"


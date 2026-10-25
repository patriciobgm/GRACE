from decimal import Decimal

def calculate_risk_score(likelihood, impact): return int(likelihood) * int(impact)
def determine_risk_level(score):
    if score <= 4: return "LOW"
    if score <= 9: return "MODERATE"
    if score <= 16: return "HIGH"
    return "CRITICAL"
def assess_risk(risk):
    risk.inherent_risk_score = calculate_risk_score(risk.likelihood, risk.impact)
    risk.inherent_risk_level = determine_risk_level(risk.inherent_risk_score)
    risk.residual_risk_score = calculate_risk_score(risk.residual_likelihood, risk.residual_impact)
    risk.residual_risk_level = determine_risk_level(risk.residual_risk_score)
    risk.save()
    return risk
def calculate_kri_status(current, warning, critical):
    current, warning, critical = map(Decimal, map(str, (current, warning, critical)))
    if warning <= critical:
        return "CRITICAL" if current >= critical else "WARNING" if current >= warning else "NORMAL"
    return "CRITICAL" if current <= critical else "WARNING" if current <= warning else "NORMAL"
def update_kri_status(indicator):
    indicator.status = calculate_kri_status(indicator.current_value, indicator.warning_threshold, indicator.critical_threshold)
    indicator.save()
    return indicator


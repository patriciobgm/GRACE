from decimal import Decimal

def calculate_kpi_status(current, target, warning, critical):
    current, target, warning, critical = map(Decimal, map(str, (current, target, warning, critical)))
    ascending = target >= warning >= critical
    if ascending:
        return "ON_TRACK" if current >= target else "WATCH" if current >= warning else "AT_RISK"
    return "ON_TRACK" if current <= target else "WATCH" if current <= warning else "AT_RISK"

def update_kpi_status(kpi):
    kpi.status = calculate_kpi_status(kpi.current_value, kpi.target_value, kpi.warning_threshold, kpi.critical_threshold)
    kpi.save(update_fields=["status", "last_updated_at", "updated_at"])
    return kpi


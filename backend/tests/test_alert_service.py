import pytest
from services.alert_service import evaluate_risks, get_alerts, acknowledge_alert, resolve_alert, ALERTS_DB
from datetime import datetime

@pytest.fixture(autouse=True)
def clear_db():
    ALERTS_DB.clear()
    yield
    ALERTS_DB.clear()

def test_risk_below_threshold():
    """1. Risk below threshold produces no alert."""
    risks = [{"zone_id": "gulberg", "risk_type": "Flood", "score_0_100": 60}]
    alerts = evaluate_risks(risks, [], [])
    assert len(alerts) == 0

def test_risk_above_warning_threshold():
    """2. Risk above configured threshold creates an alert."""
    risks = [{"zone_id": "gulberg", "risk_type": "Flood", "score_0_100": 70}]
    alerts = evaluate_risks(risks, [], [])
    assert len(alerts) == 1
    assert alerts[0].severity == "WARNING"

def test_critical_threshold():
    """3. Critical threshold gives the correct severity."""
    risks = [{"zone_id": "gulberg", "risk_type": "Flood", "score_0_100": 90}]
    alerts = evaluate_risks(risks, [], [])
    assert len(alerts) == 1
    assert alerts[0].severity == "CRITICAL"

def test_no_duplicate_spam():
    """4. Repeated evaluation does not generate duplicate active alerts."""
    risks = [{"zone_id": "gulberg", "risk_type": "Flood", "score_0_100": 90}]
    evaluate_risks(risks, [], [])
    evaluate_risks(risks, [], [])
    assert len(ALERTS_DB) == 1

def test_alert_includes_evidence_actions():
    """5. Alert includes evidence and recommended actions."""
    risks = [{"zone_id": "gulberg", "risk_type": "Flood", "score_0_100": 90, "evidence": ["Heavy rain"]}]
    decisions = [{"zone_id": "gulberg", "recommended_actions": ["Evacuate"]}]
    alerts = evaluate_risks(risks, decisions, [])
    assert "Heavy rain" in alerts[0].evidence
    assert "Evacuate" in alerts[0].recommended_actions

def test_acknowledge_alert():
    """6. acknowledge changes status and sets acknowledged_at."""
    risks = [{"zone_id": "gulberg", "risk_type": "Flood", "score_0_100": 90}]
    evaluate_risks(risks, [], [])
    alert_id = list(ALERTS_DB.keys())[0]
    
    ack = acknowledge_alert(alert_id)
    assert ack.status == "acknowledged"
    assert ack.acknowledged_at is not None

def test_resolve_alert():
    """7. resolve changes status and sets resolved_at."""
    risks = [{"zone_id": "gulberg", "risk_type": "Flood", "score_0_100": 90}]
    evaluate_risks(risks, [], [])
    alert_id = list(ALERTS_DB.keys())[0]
    
    res = resolve_alert(alert_id)
    assert res.status == "resolved"
    assert res.resolved_at is not None

def test_filters():
    """8. Filters work for severity/type/status."""
    evaluate_risks([{"zone_id": "z1", "risk_type": "Flood", "score_0_100": 70}], [], []) # Warning
    evaluate_risks([{"zone_id": "z2", "risk_type": "Air Quality", "score_0_100": 90}], [], []) # Critical
    
    assert len(get_alerts(severity="CRITICAL")) == 1
    assert len(get_alerts(type_="Flood")) == 1
    assert len(get_alerts(status="active")) == 2

def test_simulated_alerts():
    """9. Simulated risks produce alerts explicitly marked SIMULATED."""
    risks = [{"zone_id": "gulberg", "risk_type": "Flood", "score_0_100": 90}]
    alerts = evaluate_risks(risks, [], [], is_simulated=True)
    assert alerts[0].is_simulated is True
    assert "SIMULATED ALERT" in alerts[0].title

def test_missing_data_does_not_crash():
    """10. Missing confidence/evidence does not crash alert generation."""
    risks = [{"zone_id": "gulberg", "risk_type": "Flood", "score_0_100": 90}]
    alerts = evaluate_risks(risks, [], [])
    assert alerts[0].confidence == 0.0
    assert alerts[0].evidence == []

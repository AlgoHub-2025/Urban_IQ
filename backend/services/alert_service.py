from typing import List, Optional, Dict
from datetime import datetime
from models.alert import Alert

# Configurable thresholds (can be moved to a YAML or DB later)
ALERT_THRESHOLDS = {
    "Air Quality": {
        "warning": 60,
        "critical": 80
    },
    "Flood": {
        "warning": 65,
        "critical": 85
    },
    "Traffic": {
        "warning": 70,
        "critical": 90
    },
    "Composite": {
        "warning": 65,
        "critical": 85
    }
}

# In-memory store for Hackathon
ALERTS_DB: Dict[str, Alert] = {}

def get_thresholds(risk_type: str) -> dict:
    return ALERT_THRESHOLDS.get(risk_type, ALERT_THRESHOLDS["Composite"])

def evaluate_risks(risks: List[dict], decisions: List[dict], explainability: List[dict], is_simulated: bool = False) -> List[Alert]:
    """
    Evaluates risks against thresholds and creates/updates alerts deterministically.
    """
    new_or_updated = []
    
    # Map decisions and explanations for quick lookup
    dec_map = {d["zone_id"]: d for d in decisions}
    exp_map = {e["zone_id"]: e for e in explainability}
    
    for risk in risks:
        zone_id = risk["zone_id"]
        risk_type = risk["risk_type"]
        score = risk.get("score_0_100", 0)
        
        thresholds = get_thresholds(risk_type)
        
        severity = None
        if score >= thresholds["critical"]:
            severity = "CRITICAL"
        elif score >= thresholds["warning"]:
            severity = "WARNING"
            
        if not severity:
            continue
            
        # Check if active/acknowledged alert exists for this zone + type + sim status
        existing_alert = None
        for a in ALERTS_DB.values():
            if a.zone_id == zone_id and a.type == risk_type and a.is_simulated == is_simulated and a.status in ["active", "acknowledged"]:
                existing_alert = a
                break
                
        # Get associated context
        decision = dec_map.get(zone_id, {})
        explanation = exp_map.get(zone_id)
        
        sim_prefix = "SIMULATED ALERT: " if is_simulated else ""
        sim_prefix_ur = "SIMULATED ALERT: " if is_simulated else ""
        
        title = f"{sim_prefix}{severity} {risk_type} Risk - {zone_id.replace('_', ' ').title()}"
        title_ur = f"{sim_prefix_ur}{severity} {risk_type} Risk - {zone_id.replace('_', ' ').title()}"
        
        message = f"Risk score reached {score}/100. Threshold for {severity.lower()} is {thresholds[severity.lower()]}."
        message_ur = f"Risk score {score}/100 tak pohench gaya hai. {severity.lower()} ka threshold {thresholds[severity.lower()]} hai."
        
        actions = decision.get("recommended_actions", [])
        actions_ur = ["Deploy pumps immediately", "Issue public safety warning"] if len(actions) > 0 else []
        if "traffic" in risk_type.lower():
            actions_ur = ["Traffic ko divert karein", "Alternative routes ki advisory jaari karein"]
        elif "flood" in risk_type.lower() or "rain" in risk_type.lower():
            actions_ur = ["Drainage clearance pumps foran deploy karein", "Vulnerable areas se population ko alert karein"]
        else:
            actions_ur = ["Standard safety protocols apply karein", "Field teams ko standby par rakhein"]
        
        if existing_alert:
            # Update existing alert rather than duplicate spam
            existing_alert.score = score
            existing_alert.severity = severity
            existing_alert.confidence = risk.get("confidence", 0.0)
            existing_alert.evidence = risk.get("evidence", [])
            existing_alert.recommended_actions = actions
            existing_alert.recommended_actions_ur = actions_ur
            existing_alert.explainability = explanation
            existing_alert.title = title
            existing_alert.title_ur = title_ur
            existing_alert.message = message
            existing_alert.message_ur = message_ur
            new_or_updated.append(existing_alert)
        else:
            # Create new alert
            new_alert = Alert(
                zone_id=zone_id,
                type=risk_type,
                severity=severity,
                score=score,
                confidence=risk.get("confidence", 0.0),
                forecast_horizon=risk.get("forecast_horizon", "24h"),
                title=title,
                title_ur=title_ur,
                message=message,
                message_ur=message_ur,
                evidence=risk.get("evidence", []),
                recommended_actions=actions,
                recommended_actions_ur=actions_ur,
                explainability=explanation,
                is_simulated=is_simulated
            )
            ALERTS_DB[new_alert.id] = new_alert
            new_or_updated.append(new_alert)
            
    return new_or_updated

def get_alerts(status: Optional[str] = None, severity: Optional[str] = None, type_: Optional[str] = None, zone_id: Optional[str] = None) -> List[Alert]:
    results = []
    for a in ALERTS_DB.values():
        if status and a.status != status.lower():
            continue
        if severity and a.severity != severity.upper():
            continue
        if type_ and a.type.lower() != type_.lower():
            continue
        if zone_id and a.zone_id != zone_id:
            continue
        results.append(a)
    
    # Sort descending by creation date
    return sorted(results, key=lambda x: x.created_at, reverse=True)

def get_alert(alert_id: str) -> Optional[Alert]:
    return ALERTS_DB.get(alert_id)

def acknowledge_alert(alert_id: str) -> Optional[Alert]:
    alert = ALERTS_DB.get(alert_id)
    if alert and alert.status == "active":
        alert.status = "acknowledged"
        alert.acknowledged_at = datetime.utcnow().isoformat() + "Z"
    return alert

def resolve_alert(alert_id: str) -> Optional[Alert]:
    alert = ALERTS_DB.get(alert_id)
    if alert and alert.status in ["active", "acknowledged"]:
        alert.status = "resolved"
        alert.resolved_at = datetime.utcnow().isoformat() + "Z"
    return alert

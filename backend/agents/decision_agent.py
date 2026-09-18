from typing import Dict, Any, List
from state import AgentState

def get_recommended_actions(risk_level: str, risk_type: str) -> List[str]:
    actions = []
    if risk_type == "Flood":
        actions.extend(["Inspect drainage channels", "Monitor low-lying roads", "Prepare emergency response teams"])
    elif risk_type == "Air Pollution":
        actions.extend(["Issue air-quality health advisory", "Monitor sensitive populations", "Reduce unnecessary outdoor exposure"])
    elif risk_type == "Traffic":
        actions.extend(["Monitor congestion hotspots", "Optimize traffic signal timing", "Provide alternate route recommendations"])
    else:
        actions.append("Continue monitoring the area")

    if risk_level == "CRITICAL":
        actions.insert(0, "Activate immediate emergency response")
    elif risk_level == "HIGH":
        actions.insert(0, "Increase monitoring frequency")
    return actions

def decision_agent(state: AgentState) -> AgentState:
    risk_results = state.get("risks", [])
    
    if not risk_results:
        return {"decisions": [], "status_events": ["No risks to act upon..."]}
        
    decisions = []
    for r in risk_results:
        actions = get_recommended_actions(r["level"], r["risk_type"])
        decisions.append({
            "zone_id": r["zone_id"],
            "recommended_actions": actions,
            "priority": "HIGH" if r["level"] in ["CRITICAL", "HIGH"] else "NORMAL"
        })
        
    return {
        "decisions": decisions,
        "status_events": ["Generated operational recommendations..."]
    }
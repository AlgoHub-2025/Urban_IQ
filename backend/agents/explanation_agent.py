from typing import Dict, Any
from state import AgentState
from services.explainability_service import explain_risk

def explanation_agent(state: AgentState) -> AgentState:
    """
    Deterministically generates the natural language explanation and injects the XAI structure.
    """
    risks = state.get("risks", [])
    decisions = state.get("decisions", [])
    events = []
    
    if not risks:
        return {"response": "No risk data available to explain.", "status_events": ["Explanation: No data"]}
        
    # Generate XAI packet for ALL zones so Map has them
    xai_list = []
    for r in risks:
        xai_list.append(explain_risk(r))
        
    top_risk = risks[0]
    events.append(f"Generated XAI explanations for {len(risks)} zones")
    
    response_lines = []
    response_lines.append(f"Current highest risk is in {top_risk['zone_id']} with a score of {top_risk['score_0_100']} ({top_risk['level']}).")
    response_lines.append(f"Dominant risk type is {top_risk['risk_type']}.")
    
    if top_risk.get('evidence'):
        response_lines.append("Evidence:")
        for ev in top_risk['evidence']:
            response_lines.append(f"- {ev}")
            
    # Find matching decision
    top_decision = next((d for d in decisions if d["zone_id"] == top_risk["zone_id"]), None)
    if top_decision:
        response_lines.append("Recommended Actions:")
        for act in top_decision['recommended_actions']:
            response_lines.append(f"- {act}")

    return {
        "response": "\n".join(response_lines),
        "status_events": events,
        "explainability": xai_list
    }
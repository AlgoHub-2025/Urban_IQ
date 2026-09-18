from typing import Dict, Any
from state import AgentState

def intent_router(state: AgentState) -> AgentState:
    query = state.get("query", "").lower()
    
    intent = "current_status"
    if "what if" in query or "scenario" in query or "simulate" in query:
        intent = "scenario"
    elif "zone" in query and "attention" not in query:
        intent = "zone_analysis"
    elif "gulberg" in query or "dha" in query or "johar" in query:
        intent = "zone_analysis"
    elif "risk" in query or "attention" in query:
        intent = "risk_query"
    elif "forecast" in query or "predict" in query:
        intent = "forecast"
    
    return {
        "intent": intent,
        "status_events": ["Analyzing request intent..."]
    }

def route_after_intent(state: AgentState) -> str:
    if state.get("intent") == "scenario":
        return "scenario_tool"
    return "data_agent"

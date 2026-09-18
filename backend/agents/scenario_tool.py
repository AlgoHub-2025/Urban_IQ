from typing import Dict, Any
from state import AgentState

def scenario_tool(state: AgentState) -> AgentState:
    scenario = state.get("scenario", {})
    provider_data = state.get("provider_data", {})
    events = []
    
    if scenario and scenario.get("is_active"):
        events.append(f"Applying scenario override: {scenario.get('current_scenario', {}).get('description')}")
        overrides = scenario.get("current_scenario", {}).get("overrides", {})
        provider_data.update(overrides)

    return {
        "provider_data": provider_data,
        "status_events": events if events else ["Applying scenario what-if conditions..."]
    }

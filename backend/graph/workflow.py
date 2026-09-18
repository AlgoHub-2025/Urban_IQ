# graph/workflow.py

from langgraph.graph import StateGraph, START, END

from state import AgentState

from agents.intent_router import intent_router, route_after_intent
from agents.scenario_tool import scenario_tool
from agents.data_agent import data_agent
from agents.prediction_agent import prediction_agent
from agents.risk_agent import risk_agent
from agents.decision_agent import decision_agent
from agents.explanation_agent import explanation_agent


def build_workflow():
    """
    Build the complete Agentic AI workflow for Phase 6.
    """
    workflow = StateGraph(AgentState)

    workflow.add_node("intent_router", intent_router)
    workflow.add_node("scenario_tool", scenario_tool)
    workflow.add_node("data_agent", data_agent)
    workflow.add_node("prediction_agent", prediction_agent)
    workflow.add_node("risk_agent", risk_agent)
    workflow.add_node("decision_agent", decision_agent)
    workflow.add_node("explanation_agent", explanation_agent)

    # Connect
    workflow.add_edge(START, "intent_router")
    
    # We always fetch data first now to ensure live base is available for scenarios
    workflow.add_edge("intent_router", "data_agent")
    
    # Then apply scenario overrides if present
    workflow.add_edge("data_agent", "scenario_tool")
    
    workflow.add_edge("scenario_tool", "prediction_agent")
    
    workflow.add_edge("prediction_agent", "risk_agent")
    workflow.add_edge("risk_agent", "decision_agent")
    workflow.add_edge("decision_agent", "explanation_agent")
    workflow.add_edge("explanation_agent", END)

    return workflow.compile()


app = build_workflow()
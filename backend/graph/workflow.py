# graph/workflow.py

from langgraph.graph import StateGraph, START, END

from state import AgentState

from agents.data_agent import data_agent
from agents.risk_agent import risk_agent
from agents.decision_agent import decision_agent
from agents.explanation_agent import explanation_agent


def build_workflow():
    """
    Build the complete Agentic AI workflow.
    """

    workflow = StateGraph(AgentState)

    # --------------------------------------------------
    # ADD AGENTS
    # --------------------------------------------------

    workflow.add_node(
        "data_agent",
        data_agent
    )

    workflow.add_node(
        "risk_agent",
        risk_agent
    )

    workflow.add_node(
        "decision_agent",
        decision_agent
    )

    workflow.add_node(
        "explanation_agent",
        explanation_agent
    )

    # --------------------------------------------------
    # CONNECT AGENTS
    # --------------------------------------------------

    workflow.add_edge(
        START,
        "data_agent"
    )

    workflow.add_edge(
        "data_agent",
        "risk_agent"
    )

    workflow.add_edge(
        "risk_agent",
        "decision_agent"
    )

    workflow.add_edge(
        "decision_agent",
        "explanation_agent"
    )

    workflow.add_edge(
        "explanation_agent",
        END
    )

    # --------------------------------------------------
    # COMPILE
    # --------------------------------------------------

    return workflow.compile()


# Create compiled application
app = build_workflow()
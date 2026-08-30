# state.py

from typing import TypedDict, List, Dict, Any, Optional


class AgentState(TypedDict, total=False):
    """
    Shared state for the complete Agentic AI workflow.

    Flow:

    Data Agent
        ↓
    Risk Agent
        ↓
    Decision Agent
        ↓
    Explanation Agent
    """

    # Original user request
    user_query: str

    # Location requested by user
    location: str

    # Raw data collected by Data Agent
    raw_data: Dict[str, Any]

    # Cleaned and validated data
    validated_data: Dict[str, Any]

    # Engineered features
    features: Dict[str, Any]

    # Risk analysis
    risk_results: List[Dict[str, Any]]

    # Decision intelligence
    decisions: Dict[str, Any]

    # Final explanation
    explanation: str

    # Final structured response
    final_response: Dict[str, Any]

    # Error information
    error: Optional[str]
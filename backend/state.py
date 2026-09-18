import operator
from typing import TypedDict, List, Dict, Any, Optional, Annotated

class AgentState(TypedDict):
    query: str
    intent: str

    location: str
    zone_id: Optional[str]

    provider_data: Dict[str, Any]
    predictions: Dict[str, Any]
    risks: Annotated[list, operator.add]
    decisions: Annotated[list, operator.add]

    scenario: Optional[Dict[str, Any]]

    evidence: Annotated[List[str], operator.add]
    provenance: Annotated[List[str], operator.add]

    response: str
    explainability: Annotated[list, operator.add] # Phase 10 XAI outputs

    status_events: Annotated[List[str], operator.add]
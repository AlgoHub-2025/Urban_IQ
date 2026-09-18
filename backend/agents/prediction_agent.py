from typing import Dict, Any
from state import AgentState
from services.model_registry import registry as model_registry

ZONES = [
    {"zone_id": "central_lahore", "lat": 31.5497, "lon": 74.3436},
    {"zone_id": "gulberg", "lat": 31.5167, "lon": 74.3436},
    {"zone_id": "johar_town", "lat": 31.4697, "lon": 74.2728},
    {"zone_id": "dha_lahore", "lat": 31.4805, "lon": 74.4206},
    {"zone_id": "ravi_zone", "lat": 31.5833, "lon": 74.3167},
]

def prediction_agent(state: AgentState) -> AgentState:
    predictions = {}
    events = ["Running ML prediction models..."]
    provenance = []

    for z in ZONES:
        pop_res = model_registry.predict_population_density(z["lat"], z["lon"])
        if pop_res["status"] == "success":
            if z["zone_id"] not in predictions:
                predictions[z["zone_id"]] = {}
            predictions[z["zone_id"]]["population_density"] = pop_res
            provenance.append(f"ML Pop Density ({z['zone_id']}): {pop_res['prediction']:.0f} (conf: {pop_res['confidence']:.2f})")

    return {
        "predictions": predictions,
        "status_events": events,
        "provenance": provenance
    }

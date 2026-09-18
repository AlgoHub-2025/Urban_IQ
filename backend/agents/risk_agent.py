from typing import Dict, Any, List, Optional
from pydantic import BaseModel
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from services.model_registry import registry as model_registry

from datetime import datetime

class RiskThresholds(BaseModel):
    low: float = 40.0
    moderate: float = 70.0
    high: float = 85.0

class MLPrediction(BaseModel):
    value: float
    confidence: float
    model_version: str

class TopFactor(BaseModel):
    name: str
    contribution: float

class RiskResult(BaseModel):
    zone_id: str
    risk_type: str
    score_0_100: float
    level: str
    confidence: float
    forecast_horizon: str
    top_factors: List[TopFactor]
    factor_breakdown: List[Dict[str, Any]] = [] # For Explainability
    evidence: List[str]
    data_freshness: str
    generated_at: str
    ml_predictions: Optional[Dict[str, MLPrediction]] = None

def calculate_base_risk(features: Dict[str, Any]) -> float:
    rainfall = features.get("rainfall_feature", 0)
    aqi = features.get("aqi_feature", 0)
    traffic = features.get("traffic_feature", 0)
    exposure = features.get("exposure_feature", 0)
    historical = features.get("historical_feature", 0)
    trend = features.get("trend_feature", 0)

    score = (
        rainfall * 20
        + aqi * 20
        + traffic * 15
        + exposure * 15
        + historical * 20
        + trend * 10
    )
    return score

def classify_risk(score: float, thresholds: RiskThresholds) -> str:
    if score < thresholds.low: return "LOW"
    if score < thresholds.moderate: return "MODERATE"
    if score < thresholds.high: return "HIGH"
    return "CRITICAL"

def identify_risk_type(features: Dict[str, Any]) -> str:
    risks = {
        "Flood": features.get("rainfall_feature", 0),
        "Air Pollution": features.get("aqi_feature", 0),
        "Traffic": features.get("traffic_feature", 0),
        "Population Exposure": features.get("exposure_feature", 0),
        "Historical Risk": features.get("historical_feature", 0),
    }
    return max(risks, key=risks.get) if risks else "Unknown"

ZONES = [
    {"zone_id": "central_lahore", "name": "Central Lahore", "lat": 31.5497, "lon": 74.3436, "rain_f": 1.05, "traffic_f": 1.10},
    {"zone_id": "gulberg", "name": "Gulberg", "lat": 31.5167, "lon": 74.3436, "rain_f": 0.90, "traffic_f": 1.15},
    {"zone_id": "johar_town", "name": "Johar Town", "lat": 31.4697, "lon": 74.2728, "rain_f": 1.00, "traffic_f": 0.95},
    {"zone_id": "dha_lahore", "name": "DHA Lahore", "lat": 31.4805, "lon": 74.4206, "rain_f": 0.80, "traffic_f": 0.85},
    {"zone_id": "ravi_zone", "name": "Ravi Zone", "lat": 31.5833, "lon": 74.3167, "rain_f": 1.20, "traffic_f": 0.85},
]

def calculate_zone_risks(features: Dict[str, Any], predictions: Dict[str, Any], thresholds: RiskThresholds) -> List[Dict[str, Any]]:
    results = []
    base_score = calculate_base_risk(features)

    for z in ZONES:
        pop_res = predictions.get(z["zone_id"], {}).get("population_density")
        
        ml_predictions = {}
        ml_exposure_factor = features.get("exposure_feature", 0)
        pop_confidence = 0.5
        
        if pop_res and pop_res["status"] == "success":
            ml_exposure_factor = pop_res["prediction"] / 50000.0
            ml_exposure_factor = min(max(ml_exposure_factor, 0), 1.0)
            pop_confidence = pop_res["confidence"]
            ml_predictions["population_density"] = MLPrediction(
                value=pop_res["prediction"],
                confidence=pop_res["confidence"],
                model_version=pop_res["model_version"]
            )
            
        rain_f_mult = features.get("rain_f_multiplier", 1.0)
        traffic_f_mult = features.get("traffic_f_multiplier", 1.0)
        
        # AQI override affects base score
        if "aqi_override" in features:
            base_score = features["aqi_override"] / 5.0 # Max 500 AQI = 100 base score
        
        rain_contrib = base_score * (z["rain_f"] * rain_f_mult) * 0.25
        traffic_contrib = base_score * (z["traffic_f"] * traffic_f_mult) * 0.20
        exposure_contrib = base_score * ml_exposure_factor * 0.20
        base_contrib = base_score * 0.35

        adjusted_score = rain_contrib + traffic_contrib + exposure_contrib + base_contrib
        adjusted_score = round(min(max(adjusted_score, 0), 100), 2)
        
        # Calculate top factors
        factors = [
            {"name": "Rain/Flood", "val": rain_contrib},
            {"name": "Traffic", "val": traffic_contrib},
            {"name": "Population Exposure", "val": exposure_contrib},
            {"name": "Base Air/History", "val": base_contrib}
        ]
        factors.sort(key=lambda x: x["val"], reverse=True)
        top_factors = [TopFactor(name=f["name"], contribution=round(f["val"], 2)) for f in factors[:2]]

        # Override risk type if rain is the highest factor
        inferred_risk_type = identify_risk_type(features)
        if factors[0]["name"] == "Rain/Flood" and adjusted_score > 60:
            inferred_risk_type = "Flood"

        # Determine Exposed Facilities (dummy deterministic logic for demo based on score & zone)
        exposed_facilities = int((adjusted_score / 10.0) * (len(z["name"]) / 2.0))
        if "population_density" in ml_predictions:
            ml_predictions["population_density"].value = ml_predictions["population_density"].value * (1.0 + (adjusted_score/100.0) * 0.5)

        evidence = [
            f"Rainfall factor scaled by {z['rain_f']}x for {z['name']}",
            f"Traffic volume evaluated against primary arteries in {z['name']}"
        ]
        if rain_f_mult > 1.0:
            evidence.append(f"Severe Rain simulation multiplier active ({rain_f_mult}x)")
            
        if "population_density" in ml_predictions:
            evidence.append(f"ML Population Density estimated at {round(ml_predictions['population_density'].value)} per sqkm")
        
        risk_result = RiskResult(
            zone_id=z["zone_id"],
            risk_type=inferred_risk_type,
            score_0_100=adjusted_score,
            level=classify_risk(adjusted_score, thresholds),
            confidence=round(pop_confidence * 0.9, 2), # Aggregate confidence
            forecast_horizon="24h",
            top_factors=top_factors,
            factor_breakdown=factors,
            evidence=evidence,
            data_freshness="live" if pop_res and pop_res["status"] == "success" else "fallback",
            generated_at=datetime.utcnow().isoformat() + "Z",
            ml_predictions=ml_predictions
        )
        
        # Inject exposed facilities directly into the result dump
        dumped = risk_result.model_dump()
        dumped["exposed_facilities"] = exposed_facilities
        results.append(dumped)

    return sorted(results, key=lambda x: x["score_0_100"], reverse=True)

from state import AgentState

def risk_agent(state: AgentState) -> AgentState:
    features = state.get("provider_data", {})
    predictions = state.get("predictions", {})

    thresholds = RiskThresholds() 
    risk_results = calculate_zone_risks(features, predictions, thresholds)

    return {
        "risks": risk_results,
        "status_events": ["Calculated zone risk indices..."]
    }
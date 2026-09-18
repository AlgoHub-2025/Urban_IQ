from typing import Dict, Any
from agents.risk_agent import calculate_zone_risks, RiskThresholds, ZONES

def evaluate_response_action(zone_id: str, action: str, current_features: Dict[str, Any], current_predictions: Dict[str, Any]) -> Dict[str, Any]:
    """
    Phase 14 (Repurposed): Urban Response Twin
    Simulates the impact of an emergency response action on a zone's risk profile.
    """
    # Run Baseline
    thresholds = RiskThresholds()
    baseline_risks = calculate_zone_risks(current_features, current_predictions, thresholds)
    baseline_zone = next((r for r in baseline_risks if r["zone_id"] == zone_id), None)
    
    if not baseline_zone:
        return {"status": "error", "message": "Zone not found in baseline calculations."}
        
    baseline_score = baseline_zone["score_0_100"]
    
    # Clone features for modification
    modified_features = current_features.copy()
    
    explanation = ""
    explanation_ur = ""
    affected_factors = []
    
    if action == "traffic_diversion":
        # Traffic diversion reduces traffic multiplier by 80%
        modified_features["traffic_f_multiplier"] = modified_features.get("traffic_f_multiplier", 1.0) * 0.2
        explanation = "Traffic diversion heavily reduces the traffic congestion factor along major arteries, clearing bottlenecks for emergency services and lowering the composite risk."
        explanation_ur = "Traffic diversion se major arteries par traffic congestion factor kaafi kam ho jata hai, jisse emergency services ke liye bottlenecks clear hote hain aur composite risk lower hota hai."
        affected_factors = ["Traffic", "Population Exposure"]
        
    elif action == "drainage_clearance":
        # Drainage clearance lowers the effective rainfall / flood multiplier by 60%
        modified_features["rain_f_multiplier"] = modified_features.get("rain_f_multiplier", 1.0) * 0.4
        explanation = "Pre-emptive drainage clearance increases stormwater capacity, significantly mitigating the flood exposure factor and protecting critical facilities."
        explanation_ur = "Drainage clearance simulated scenario mein stormwater capacity barhata hai, jis se flood exposure factor numaya taur par kam hota hai aur critical facilities protect hoti hain."
        affected_factors = ["Rain/Flood", "Base Air/History"]
        
    elif action == "resource_pre_deployment":
        # Pre-deploying resources mitigates exposure risks by 50%
        modified_features["exposure_feature"] = modified_features.get("exposure_feature", 1.0) * 0.5
        explanation = "Pre-deploying medical and rescue units directly reduces the population vulnerability index, improving emergency response times in high-exposure areas."
        explanation_ur = "Medical aur rescue units ko pre-deploy karne se population vulnerability index directly kam hota hai, aur high-exposure areas mein emergency response times behtar hotay hain."
        affected_factors = ["Population Exposure"]
        
    else:
        return {"status": "error", "message": "Unknown action type."}

    # Run Simulated
    simulated_risks = calculate_zone_risks(modified_features, current_predictions, thresholds)
    simulated_zone = next((r for r in simulated_risks if r["zone_id"] == zone_id), None)
    simulated_score = simulated_zone["score_0_100"]
    
    delta = round(simulated_score - baseline_score, 2)
    
    return {
        "status": "success",
        "zone_id": zone_id,
        "action": action,
        "simulation_status": "simulated",
        "baseline_risk": baseline_score,
        "after_action_risk": simulated_score,
        "risk_delta": delta,
        "affected_factors": affected_factors,
        "expected_impact": f"{delta} Risk Points",
        "explanation": explanation,
        "explanation_ur": explanation_ur
    }

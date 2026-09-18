from typing import Dict, Any

def explain_risk(risk_result: dict) -> dict:
    """
    Phase 10: Deterministic Explainable AI Service
    Converts a raw RiskResult into a structured, source-aware explanation.
    """
    
    # 1. Map raw factors to an explicit contribution list
    factors = []
    
    for f in risk_result.get("factor_breakdown", []):
        name = f["name"]
        val = f["val"]
        
        # Determine source and quality based on the factor logic
        source = "rule_engine"
        quality = "medium"
        direction = "increases_risk" if val > 0 else "neutral"
        
        if name == "Rain/Flood":
            source = "Open-Meteo"
            quality = "live_sensor"
        elif name == "Traffic":
            source = "Punjab_Traffic"
            quality = "historical_aggregate"
        elif name == "Population Exposure":
            source = "population_density_model"
            quality = "ml_prediction"
        elif name == "Base Air/History":
            source = "AQICN + Punjab_BOS"
            quality = "live_sensor"
            
        factors.append({
            "factor": name,
            "value": round(val, 2), # Raw score contribution
            "normalized_contribution": round((val / max(1, risk_result.get("score_0_100", 1))) * 100, 1), # Percentage of total
            "direction": direction,
            "source": source,
            "quality": quality
        })
        
    factors.sort(key=lambda x: x["value"], reverse=True)
    
    return {
        "zone_id": risk_result.get("zone_id", "unknown"),
        "risk_type": risk_result.get("risk_type", "Unknown"),
        "score": risk_result.get("score_0_100", 0),
        "top_factors": factors,
        "evidence": risk_result.get("evidence", []),
        "confidence": risk_result.get("confidence", 0.0),
        "data_freshness": risk_result.get("data_freshness", "unknown"),
        "generated_at": risk_result.get("generated_at", ""),
        "explanation_type": "rule_based + ml"
    }

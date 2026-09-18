import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.risk_agent import risk_agent, calculate_zone_risks, RiskThresholds

def test_risk_agent_missing_features():
    res = risk_agent({"features": {}})
    assert "error" in res

def test_risk_agent_extreme_values():
    # Features with values > 1.0 (which shouldn't happen but testing limits)
    features = {
        "rainfall_feature": 1.5,
        "aqi_feature": 2.0,
        "traffic_feature": -0.5,
        "exposure_feature": 1.0,
        "historical_feature": 0.5,
        "trend_feature": 0.0
    }
    
    thresholds = RiskThresholds()
    results = calculate_zone_risks(features, thresholds)
    
    for r in results:
        # Score must be bounded 0-100
        assert 0 <= r["score_0_100"] <= 100
        assert r["zone_id"] in ["central_lahore", "gulberg", "johar_town", "dha_lahore", "ravi_zone"]
        
        # Check structured schema
        assert "level" in r
        assert "risk_type" in r
        assert "top_factors" in r
        assert "evidence" in r
        assert "ml_predictions" in r
        assert "data_freshness" in r

def test_risk_agent_normal_flow():
    features = {
        "rainfall_feature": 0.8,
        "aqi_feature": 0.6,
        "traffic_feature": 0.7,
        "exposure_feature": 0.8,
        "historical_feature": 0.5,
        "trend_feature": 0.2
    }
    state = {"features": features}
    res = risk_agent(state)
    assert "risk_results" in res
    assert len(res["risk_results"]) == 5
    
    # Check if ML was joined
    central = next(x for x in res["risk_results"] if x["zone_id"] == "central_lahore")
    if "population_density" in central["ml_predictions"]:
        assert central["ml_predictions"]["population_density"]["confidence"] > 0

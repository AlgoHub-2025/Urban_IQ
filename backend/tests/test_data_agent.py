import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from agents.data_agent import data_agent

def test_data_agent_pipeline():
    state = {"location": "Lahore"}
    result = data_agent(state)
    
    assert "raw_data" in result
    assert "validated_data" in result
    assert "features" in result
    
    # Check that providers return standard schema
    weather = result["raw_data"]["weather"]
    assert "source" in weather
    assert "fetched_at" in weather
    assert "freshness_seconds" in weather
    assert "status" in weather
    assert "location" in weather
    assert "normalized_fields" in weather
    
    assert weather["status"] in ["live", "fallback", "unavailable", "cached"]
    assert "temperature_c" in weather["normalized_fields"]
    
    # Check features were engineered properly
    assert "rainfall_feature" in result["features"]

def test_osm_provider_fallback():
    from providers.osm_provider import OSMProvider
    provider = OSMProvider()
    
    # This should fail validation and use fallback
    res = provider.get_data(location="Karachi")
    assert res["status"] == "fallback"
    assert res["location"] == "Karachi"
    assert "road_density" in res["normalized_fields"]
    
    # This should hit cache on second try
    res1 = provider.get_data(location="Lahore")
    res2 = provider.get_data(location="Lahore")
    assert res2["status"] == "cached"


import pytest
from services.resource_intelligence import evaluate_resources, haversine

def test_haversine_distance():
    """2. Distances are calculated from valid coordinates."""
    # Test valid coords
    dist = haversine(31.52, 74.34, 31.55, 74.33)
    assert 3.0 < dist < 4.0 # roughly 3.4km
    
    # 5. Missing coordinates do not crash the service.
    dist_none = haversine(None, None, None, None)
    assert dist_none == 999.0

def test_high_risk_zone_returns_resources():
    """1. High-risk zone returns nearby hospitals."""
    res = evaluate_resources("gulberg", "Flood", 85)
    assert len(res["resources"]) > 0
    assert res["resources"][0]["type"] == "hospital"

def test_nearest_resource_ranks_appropriately():
    """3. Nearest resource ranks appropriately."""
    res = evaluate_resources("gulberg", "Flood", 50)
    top_resource = res["resources"][0]
    assert top_resource["priority_level"] in ["high", "medium"]

def test_exposure_penalty():
    """4. Resource inside the affected zone receives an exposure penalty."""
    res = evaluate_resources("johar_town", "Flood", 90)
    # Find a hospital that is penalized
    elevated_hospitals = [h for h in res["resources"] if h["exposure_status"] == "elevated"]
    if elevated_hospitals:
        assert any("Inside flood exposure area" in r for r in elevated_hospitals[0]["reason"])

def test_unknown_capacity():
    """6. Unknown facility capacity is shown as unknown, not invented."""
    res = evaluate_resources("gulberg", "Flood", 85)
    assert res["resources"][0]["capacity_status"] == "unknown"

def test_routing_unavailable():
    """7. Routing is unavailable when road-state data is insufficient."""
    res = evaluate_resources("gulberg", "Flood", 85)
    assert res["routing_status"] == "unavailable"
    assert "No validated live road-state data" in res["limitations"]

def test_simulated_scenario_label():
    """8. Simulated scenario resources remain labeled within the simulated context."""
    res = evaluate_resources("gulberg", "Flood", 85, is_simulated=True)
    assert "[SIMULATED]" in res["resources"][0]["name"]

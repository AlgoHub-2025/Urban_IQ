import math
import json
import os
from typing import List, Dict, Any

# Canonical mappings for Lahore zones to approximate centroids for Hackathon demo
ZONE_CENTROIDS = {
    "ravi_zone": {"lat": 31.62, "lon": 74.30},
    "central_lahore": {"lat": 31.55, "lon": 74.33},
    "gulberg": {"lat": 31.52, "lon": 74.34},
    "defense": {"lat": 31.48, "lon": 74.40},
    "model_town": {"lat": 31.48, "lon": 74.32},
    "johar_town": {"lat": 31.46, "lon": 74.27},
    "iqbal_town": {"lat": 31.51, "lon": 74.28},
}

# Cache for resources
_HOSPITALS_CACHE = None

def get_hospitals() -> List[Dict]:
    global _HOSPITALS_CACHE
    if _HOSPITALS_CACHE is None:
        try:
            path = os.path.join(os.path.dirname(__file__), "..", "hospitals_predictions.json")
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                _HOSPITALS_CACHE = data.get("predictions", [])
        except Exception:
            _HOSPITALS_CACHE = []
    return _HOSPITALS_CACHE

def haversine(lat1, lon1, lat2, lon2) -> float:
    """Calculate the great circle distance in kilometers between two points on the earth."""
    if any(x is None for x in [lat1, lon1, lat2, lon2]):
        return 999.0
        
    R = 6371.0 # Radius of earth in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c

def evaluate_resources(zone_id: str, risk_type: str, risk_score: float, is_simulated: bool = False) -> Dict[str, Any]:
    """
    Phase 9: Emergency Resource Intelligence
    Identifies and prioritizes nearby emergency resources.
    """
    
    zone_centroid = ZONE_CENTROIDS.get(zone_id.lower(), ZONE_CENTROIDS["central_lahore"])
    hospitals = get_hospitals()
    
    evaluated_resources = []
    
    for h in hospitals:
        # We only treat hospitals (not clinics) as major emergency response centers for this phase
        if h.get("predicted_type") != "hospital" and h.get("actual_type") != "hospital":
            continue
            
        name = h.get("name", "Unknown Hospital")
        if name == "Unknown":
            name = "Unnamed Medical Facility"
            
        lat = h.get("lat")
        lon = h.get("lon")
        
        # Calculate Haversine distance
        dist_km = haversine(zone_centroid["lat"], zone_centroid["lon"], lat, lon)
        if dist_km > 15.0: # Filter out hospitals too far away
            continue
            
        # Transparent Priority Scoring
        # Start with a base score of 100
        priority = 100
        reasons = []
        
        # Proximity factor
        if dist_km < 3.0:
            priority += 20
            reasons.append("Immediate proximity (< 3km)")
        elif dist_km < 7.0:
            priority += 10
        else:
            priority -= int(dist_km * 2)
            
        # Exposure safety
        exposure_status = "safe"
        if dist_km < 2.0 and risk_score > 75:
            # If the hospital is right inside the high-risk zone, it is exposed
            priority -= 30
            exposure_status = "elevated"
            reasons.append(f"Inside {risk_type.lower()} exposure area")
        else:
            reasons.append("Outside active exposure area")
            
        priority_level = "high"
        if priority < 60:
            priority_level = "low"
        elif priority < 90:
            priority_level = "medium"
            
        if is_simulated:
            name = f"[SIMULATED] {name}"
            
        evaluated_resources.append({
            "name": name,
            "type": "hospital",
            "latitude": lat,
            "longitude": lon,
            "distance_km": round(dist_km, 1),
            "priority_score": priority,
            "priority_level": priority_level,
            "exposure_status": exposure_status,
            "capacity_status": "unknown", # Transparent about missing real-time capacity
            "reason": reasons
        })
        
    # Sort by priority descending
    evaluated_resources.sort(key=lambda x: x["priority_score"], reverse=True)
    
    # Return Top 5
    return {
        "zone_id": zone_id,
        "risk_type": risk_type,
        "risk_score": risk_score,
        "resources": evaluated_resources[:5],
        "routing_status": "unavailable",
        "limitations": "No validated live road-state data available. Route viability not guaranteed."
    }

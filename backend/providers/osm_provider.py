import requests
from typing import Dict, Any
from .base import BaseProvider

class OSMProvider(BaseProvider):
    def __init__(self):
        super().__init__(name="OpenStreetMap_Overpass", cache_ttl=3600)  # cache for 1 hour

    def fetch_data(self, **kwargs) -> Dict[str, Any]:
        """
        In a real scenario, this would query Overpass API.
        For the hackathon, we simulate an API call that returns
        geo-spatial context for Lahore.
        """
        # Simulated Overpass API request latency and structure
        location = kwargs.get("location", "Lahore")
        if location.lower() != "lahore":
            raise ValueError(f"OSM Data not available for {location}")
        
        # In a real API we would do:
        # url = "http://overpass-api.de/api/interpreter"
        # query = f"[out:json];area[name='{location}']->.searchArea;(node(area.searchArea);<;);out;"
        # response = requests.post(url, data={'data': query}, timeout=10)
        
        # We simulate a successful structured response for Lahore
        return {
            "status": "success",
            "data": {
                "road_density": 0.68,
                "waterway_density": 0.42,
                "poi_density": 0.73,
                "hospital_distance_km": 2.4,
                "school_density": 0.61,
                "population_exposure": 0.76,
            }
        }

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        data = raw_data.get("data", {})
        return {
            "road_density": data.get("road_density", 0),
            "waterway_density": data.get("waterway_density", 0),
            "poi_density": data.get("poi_density", 0),
            "hospital_distance_km": data.get("hospital_distance_km", 0),
            "school_density": data.get("school_density", 0),
            "population_exposure": data.get("population_exposure", 0),
        }

    def get_fallback_data(self, **kwargs) -> Dict[str, Any]:
        return {
            "data": {
                "road_density": 0.65,
                "waterway_density": 0.40,
                "poi_density": 0.70,
                "hospital_distance_km": 3.0,
                "school_density": 0.60,
                "population_exposure": 0.70,
            }
        }

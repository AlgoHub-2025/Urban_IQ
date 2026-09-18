from typing import Dict, Any
from .base import BaseProvider

class LocalProvider(BaseProvider):
    def __init__(self, name: str, dataset_type: str):
        super().__init__(name=name)
        self.dataset_type = dataset_type

    def fetch_data(self, **kwargs) -> Dict[str, Any]:
        return self.get_fallback_data(**kwargs)

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        return raw_data

    def get_fallback_data(self, **kwargs) -> Dict[str, Any]:
        if self.dataset_type == "traffic":
            return {
                "traffic_level": "HIGH",
                "traffic_index": 78,
                "average_speed_kmh": 24,
                "congestion": 0.78,
            }
        elif self.dataset_type == "spatial":
            return {
                "road_density": 0.68,
                "waterway_density": 0.42,
                "poi_density": 0.73,
                "hospital_distance_km": 2.4,
                "school_density": 0.61,
                "population_exposure": 0.76,
            }
        elif self.dataset_type == "historical":
            return {
                "historical_flood_risk": 0.64,
                "historical_traffic_risk": 0.71,
                "historical_air_pollution_risk": 0.69,
                "recent_risk_trend": 0.74,
            }
        return {}

import requests
from typing import Dict, Any
from .base import BaseProvider
from config import Config

class AQIProvider(BaseProvider):
    def __init__(self):
        super().__init__(name="AQICN")
        self.token = Config.AQICN_TOKEN

    def fetch_data(self, **kwargs) -> Dict[str, Any]:
        if not self.token:
            raise ValueError("AQICN_TOKEN not configured")
        
        url = "https://api.waqi.info/feed/lahore/"
        params = {"token": self.token}
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        
        if data.get("status") != "ok":
            raise ValueError(f"AQICN API returned error: {data.get('data')}")
            
        return data["data"]

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        iaqi = raw_data.get("iaqi", {})
        return {
            "aqi": raw_data.get("aqi", 0),
            "pm25": iaqi.get("pm25", {}).get("v", 0),
            "pm10": iaqi.get("pm10", {}).get("v", 0),
            "co": iaqi.get("co", {}).get("v", 0),
            "no2": iaqi.get("no2", {}).get("v", 0),
            "o3": iaqi.get("o3", {}).get("v", 0),
            "so2": iaqi.get("so2", {}).get("v", 0)
        }

    def get_fallback_data(self, **kwargs) -> Dict[str, Any]:
        # Fallback payload mimicking AQICN structure
        return {
            "aqi": 168,
            "iaqi": {
                "pm25": {"v": 92.0},
                "pm10": {"v": 145.0},
                "no2": {"v": 42.0},
                "so2": {"v": 11.0},
                "co": {"v": 1.8},
                "o3": {"v": 38.0}
            }
        }

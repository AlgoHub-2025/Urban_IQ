import requests
from typing import Dict, Any
from .base import BaseProvider

class WeatherProvider(BaseProvider):
    def __init__(self):
        super().__init__(name="Open-Meteo")

    def fetch_data(self, **kwargs) -> Dict[str, Any]:
        url = "https://api.open-meteo.com/v1/forecast"
        # Coordinates for Lahore
        params = {
            "latitude": 31.5204,
            "longitude": 74.3587,
            "current": "temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m",
            "timezone": "Asia/Karachi"
        }
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        return response.json()

    def normalize(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        current = raw_data.get("current", {})
        return {
            "temperature_c": current.get("temperature_2m", 0),
            "feels_like_c": current.get("apparent_temperature", 0),
            "humidity_percent": current.get("relative_humidity_2m", 0),
            "precipitation_mm": current.get("precipitation", 0),
            "wind_speed_kmh": current.get("wind_speed_10m", 0),
            "weather_code": current.get("weather_code", 0)
        }

    def get_fallback_data(self, **kwargs) -> Dict[str, Any]:
        # Fallback payload mimicking Open-Meteo structure
        return {
            "current": {
                "temperature_2m": 31.5,
                "apparent_temperature": 34.2,
                "relative_humidity_2m": 72,
                "precipitation": 0.0,
                "wind_speed_10m": 12.5,
                "weather_code": 1
            }
        }

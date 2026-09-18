from typing import Dict, Any
from datetime import datetime

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from state import AgentState
from providers.weather_provider import WeatherProvider
from providers.aqi_provider import AQIProvider
from providers.local_provider import LocalProvider
from providers.osm_provider import OSMProvider

def get_weather(location: str) -> Dict[str, Any]:
    provider = WeatherProvider()
    return provider.get_data(location=location)

def get_air_quality(location: str) -> Dict[str, Any]:
    provider = AQIProvider()
    return provider.get_data(location=location)

def get_traffic(location: str) -> Dict[str, Any]:
    provider = LocalProvider("Punjab_Traffic", "traffic")
    return provider.get_data(location=location)

def get_spatial_data(location: str) -> Dict[str, Any]:
    provider = OSMProvider()
    return provider.get_data(location=location)


def get_historical_data(location: str) -> Dict[str, Any]:
    provider = LocalProvider("Punjab_BOS", "historical")
    return provider.get_data(location=location)


def validate_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Basic data validation on normalized_fields.
    """
    weather = data["weather"].get("normalized_fields", {})
    air_quality = data["air_quality"].get("normalized_fields", {})
    traffic = data["traffic"].get("normalized_fields", {})
    
    # Validation logic with default fallbacks if missing
    weather["temperature_c"] = max(-50, min(weather.get("temperature_c", 0), 60))
    weather["humidity_percent"] = max(0, min(weather.get("humidity_percent", 0), 100))
    weather["precipitation_mm"] = max(0, weather.get("precipitation_mm", 0))
    
    air_quality["aqi"] = max(0, air_quality.get("aqi", 0))
    air_quality["pm25"] = max(0, air_quality.get("pm25", 0))
    air_quality["pm10"] = max(0, air_quality.get("pm10", 0))

    traffic["traffic_index"] = max(0, min(traffic.get("traffic_index", 0), 100))

    return data


def feature_engineering(data: Dict[str, Any]) -> Dict[str, Any]:
    weather = data["weather"]["normalized_fields"]
    air = data["air_quality"]["normalized_fields"]
    traffic = data["traffic"]["normalized_fields"]
    spatial = data["spatial"]["normalized_fields"]
    historical = data["historical"]["normalized_fields"]

    rainfall_feature = min(weather.get("precipitation_mm", 0) / 100, 1.0)
    aqi_feature = min(air.get("aqi", 0) / 300, 1.0)
    traffic_feature = traffic.get("traffic_index", 0) / 100
    exposure_feature = spatial.get("population_exposure", 0)
    
    historical_feature = (
        historical.get("historical_flood_risk", 0)
        + historical.get("historical_traffic_risk", 0)
        + historical.get("historical_air_pollution_risk", 0)
    ) / 3
    trend_feature = historical.get("recent_risk_trend", 0)

    return {
        "rainfall_feature": round(rainfall_feature, 3),
        "aqi_feature": round(aqi_feature, 3),
        "traffic_feature": round(traffic_feature, 3),
        "exposure_feature": round(exposure_feature, 3),
        "historical_feature": round(historical_feature, 3),
        "trend_feature": round(trend_feature, 3),

        "temperature": weather.get("temperature_c", 0),
        "humidity": weather.get("humidity_percent", 0),
        "wind_speed": weather.get("wind_speed_kmh", 0),
        "precipitation_mm": weather.get("precipitation_mm", 0),

        "aqi": air.get("aqi", 0),
        "pm25": air.get("pm25", 0),
        "pm10": air.get("pm10", 0),

        "traffic_level": traffic.get("traffic_level", "UNKNOWN"),
        "traffic_index": traffic.get("traffic_index", 0),

        "road_density": spatial.get("road_density", 0),
        "waterway_density": spatial.get("waterway_density", 0),
        "poi_density": spatial.get("poi_density", 0),
        "population_exposure": spatial.get("population_exposure", 0),
    }


def data_agent(state: AgentState) -> AgentState:
    location = state.get("location", "Lahore")

    raw_data = {
        "timestamp": datetime.now().isoformat(),
        "location": location,
        "weather": get_weather(location),
        "air_quality": get_air_quality(location),
        "traffic": get_traffic(location),
        "spatial": get_spatial_data(location),
        "historical": get_historical_data(location),
    }

    validated_data = validate_data(raw_data)
    features = feature_engineering(validated_data)

    events = [f"Fetching {location} live provider data..."]
    provenance = []
    
    for key in ["weather", "air_quality", "traffic", "spatial", "historical"]:
        source = raw_data[key].get("source", "Unknown")
        status = raw_data[key].get("status", "unavailable")
        provenance.append(f"{key.capitalize()}: {source} [{status.upper()}]")

    return {
        "provider_data": features, # We store the engineered features here for now
        "status_events": events,
        "provenance": provenance
    }
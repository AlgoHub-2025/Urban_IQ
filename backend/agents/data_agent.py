# agents/data_agent.py

from typing import Dict, Any
from datetime import datetime


def get_mock_weather() -> Dict[str, Any]:
    """
    Simulated weather data.

    Later:
    Replace this with Open-Meteo API.
    """

    return {
        "temperature": 31.5,
        "humidity": 72,
        "rainfall_1h": 8.5,
        "rainfall_6h": 24.0,
        "rainfall_24h": 48.0,
        "wind_speed": 12.5,
        "wind_direction": "NW",
    }


def get_mock_air_quality() -> Dict[str, Any]:
    """
    Simulated air quality data.

    Later:
    Replace this with OpenAQ API.
    """

    return {
        "aqi": 168,
        "pm25": 92.0,
        "pm10": 145.0,
        "no2": 42.0,
        "so2": 11.0,
        "co": 1.8,
        "o3": 38.0,
    }


def get_mock_traffic() -> Dict[str, Any]:
    """
    Simulated traffic information.

    Later:
    Replace this with a real traffic API.
    """

    return {
        "traffic_level": "HIGH",
        "traffic_index": 78,
        "average_speed_kmh": 24,
        "congestion": 0.78,
    }


def get_mock_spatial_data() -> Dict[str, Any]:
    """
    Simulated spatial/geographical information.

    Later:
    Replace with PostGIS + OSM processing.
    """

    return {
        "road_density": 0.68,
        "waterway_density": 0.42,
        "poi_density": 0.73,
        "hospital_distance_km": 2.4,
        "school_density": 0.61,
        "population_exposure": 0.76,
    }


def get_mock_historical_data() -> Dict[str, Any]:
    """
    Simulated historical risk information.

    Later:
    Replace with historical datasets from Punjab BOS,
    PBS, HDX and other datasets.
    """

    return {
        "historical_flood_risk": 0.64,
        "historical_traffic_risk": 0.71,
        "historical_air_pollution_risk": 0.69,
        "recent_risk_trend": 0.74,
    }


def validate_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Basic data validation.

    Removes obviously invalid values and ensures
    required fields exist.
    """

    weather = data["weather"]
    air_quality = data["air_quality"]
    traffic = data["traffic"]
    spatial = data["spatial"]
    historical = data["historical"]

    # Basic validation
    weather["temperature"] = max(-50, min(weather["temperature"], 60))
    weather["humidity"] = max(0, min(weather["humidity"], 100))

    weather["rainfall_1h"] = max(0, weather["rainfall_1h"])
    weather["rainfall_6h"] = max(0, weather["rainfall_6h"])
    weather["rainfall_24h"] = max(0, weather["rainfall_24h"])

    air_quality["aqi"] = max(0, air_quality["aqi"])
    air_quality["pm25"] = max(0, air_quality["pm25"])
    air_quality["pm10"] = max(0, air_quality["pm10"])

    traffic["traffic_index"] = max(
        0,
        min(traffic["traffic_index"], 100)
    )

    return data


def feature_engineering(data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Converts raw data into normalized features.

    These features are later consumed by the Risk Agent.
    """

    weather = data["weather"]
    air = data["air_quality"]
    traffic = data["traffic"]
    spatial = data["spatial"]
    historical = data["historical"]

    # Rainfall feature
    rainfall_feature = min(
        weather["rainfall_24h"] / 100,
        1.0
    )

    # AQI feature
    aqi_feature = min(
        air["aqi"] / 300,
        1.0
    )

    # Traffic feature
    traffic_feature = traffic["traffic_index"] / 100

    # Population exposure
    exposure_feature = spatial["population_exposure"]

    # Historical risk
    historical_feature = (
        historical["historical_flood_risk"]
        + historical["historical_traffic_risk"]
        + historical["historical_air_pollution_risk"]
    ) / 3

    # Recent trend
    trend_feature = historical["recent_risk_trend"]

    return {
        "rainfall_feature": round(rainfall_feature, 3),
        "aqi_feature": round(aqi_feature, 3),
        "traffic_feature": round(traffic_feature, 3),
        "exposure_feature": round(exposure_feature, 3),
        "historical_feature": round(historical_feature, 3),
        "trend_feature": round(trend_feature, 3),

        "temperature": weather["temperature"],
        "humidity": weather["humidity"],
        "wind_speed": weather["wind_speed"],

        "aqi": air["aqi"],
        "pm25": air["pm25"],
        "pm10": air["pm10"],

        "traffic_level": traffic["traffic_level"],
        "traffic_index": traffic["traffic_index"],

        "road_density": spatial["road_density"],
        "waterway_density": spatial["waterway_density"],
        "poi_density": spatial["poi_density"],
        "population_exposure": spatial["population_exposure"],
    }


def data_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main Data Intelligence Agent.

    Responsibilities:

    1. Collect data
    2. Validate data
    3. Normalize data
    4. Perform feature engineering
    """

    print("\n" + "=" * 70)
    print("📊 DATA INTELLIGENCE AGENT")
    print("=" * 70)

    location = state.get("location", "Lahore")

    print(f"📍 Location: {location}")
    print("🔄 Collecting city intelligence data...")

    raw_data = {
        "timestamp": datetime.now().isoformat(),
        "location": location,

        "weather": get_mock_weather(),

        "air_quality": get_mock_air_quality(),

        "traffic": get_mock_traffic(),

        "spatial": get_mock_spatial_data(),

        "historical": get_mock_historical_data(),
    }

    print("✅ Weather data collected")
    print("✅ Air quality data collected")
    print("✅ Traffic data collected")
    print("✅ Spatial data collected")
    print("✅ Historical data collected")

    print("\n🔍 Validating data...")

    validated_data = validate_data(raw_data)

    print("✅ Data validation completed")

    print("\n⚙️ Performing feature engineering...")

    features = feature_engineering(validated_data)

    print("✅ Feature engineering completed")

    return {
        "raw_data": raw_data,
        "validated_data": validated_data,
        "features": features,
    }
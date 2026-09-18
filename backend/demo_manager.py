DEMO_STATE = {
    "is_active": False,
    "current_scenario": None
}

HEAVY_RAIN_SCENARIO = {
    "scenario_id": "lahore_heavy_rain_demo",
    "mode": "demo",
    "rainfall_mm": 70,
    "label": "SIMULATED",
    "description": "Hackathon deterministic heavy-rain scenario",
    "overrides": {
        "rain_f_multiplier": 3.5,
        "exposure_feature": 40000, # Max out exposure artificially
        "weather_status": "severe_rain"
    }
}

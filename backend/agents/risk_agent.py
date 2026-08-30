# agents/risk_agent.py

from typing import Dict, Any, List


def calculate_risk_score(features: Dict[str, Any]) -> float:
    """
    Calculate overall risk score.

    Current version:
    Weighted intelligence/risk engine.

    Later:
    Replace or augment this with trained ML models such as:

    - Logistic Regression
    - Random Forest
    - Gradient Boosting
    - XGBoost
    - LightGBM
    - Ensemble Models
    """

    rainfall = features["rainfall_feature"]
    aqi = features["aqi_feature"]
    traffic = features["traffic_feature"]
    exposure = features["exposure_feature"]
    historical = features["historical_feature"]
    trend = features["trend_feature"]

    # Weighted risk model
    score = (
        rainfall * 20
        + aqi * 20
        + traffic * 15
        + exposure * 15
        + historical * 20
        + trend * 10
    )

    return round(min(max(score, 0), 100), 2)


def classify_risk(score: float) -> str:
    """
    Risk classification.

    0 - 39   LOW
    40 - 69  MODERATE
    70 - 84  HIGH
    85 - 100 CRITICAL
    """

    if score < 40:
        return "LOW"

    if score < 70:
        return "MODERATE"

    if score < 85:
        return "HIGH"

    return "CRITICAL"


def identify_risk_type(features: Dict[str, Any]) -> str:
    """
    Identify the dominant risk type.
    """

    risks = {
        "Flood": features["rainfall_feature"],
        "Air Pollution": features["aqi_feature"],
        "Traffic": features["traffic_feature"],
        "Population Exposure": features["exposure_feature"],
        "Historical Risk": features["historical_feature"],
    }

    return max(risks, key=risks.get)


def calculate_zone_risks(features: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generate risk estimates for major Lahore zones.

    In the production version, these will be generated
    using actual spatial/grid-level data.
    """

    zones = [
        {
            "zone": "Central Lahore",
            "rain_factor": 1.05,
            "traffic_factor": 1.10,
            "exposure_factor": 1.10,
        },
        {
            "zone": "Gulberg",
            "rain_factor": 0.90,
            "traffic_factor": 1.15,
            "exposure_factor": 0.95,
        },
        {
            "zone": "Johar Town",
            "rain_factor": 1.00,
            "traffic_factor": 0.95,
            "exposure_factor": 1.05,
        },
        {
            "zone": "DHA Lahore",
            "rain_factor": 0.80,
            "traffic_factor": 0.85,
            "exposure_factor": 0.75,
        },
        {
            "zone": "Ravi Zone",
            "rain_factor": 1.20,
            "traffic_factor": 0.85,
            "exposure_factor": 1.20,
        },
    ]

    results = []

    base_score = calculate_risk_score(features)

    for zone in zones:

        adjusted_score = (
            base_score
            * 0.35
            + base_score * zone["rain_factor"] * 0.25
            + base_score * zone["traffic_factor"] * 0.20
            + base_score * zone["exposure_factor"] * 0.20
        )

        adjusted_score = round(
            min(max(adjusted_score, 0), 100),
            2
        )

        risk_level = classify_risk(adjusted_score)

        risk_type = identify_risk_type(features)

        results.append(
            {
                "zone": zone["zone"],
                "risk_score": adjusted_score,
                "risk_level": risk_level,
                "risk_type": risk_type,
                "factors": {
                    "rainfall": features["rainfall_feature"],
                    "air_quality": features["aqi_feature"],
                    "traffic": features["traffic_feature"],
                    "population_exposure": features["exposure_feature"],
                    "historical_risk": features["historical_feature"],
                    "recent_trend": features["trend_feature"],
                },
            }
        )

    return sorted(
        results,
        key=lambda x: x["risk_score"],
        reverse=True
    )


def risk_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main Risk Intelligence Agent.
    """

    print("\n" + "=" * 70)
    print("⚠️ RISK INTELLIGENCE AGENT")
    print("=" * 70)

    features = state.get("features", {})

    if not features:
        return {
            "error": "No features available for risk analysis."
        }

    risk_results = calculate_zone_risks(features)

    print("\n🚨 Risk analysis completed:\n")

    for result in risk_results:
        print(
            f"{result['zone']:20} "
            f"{result['risk_score']:>6} "
            f"{result['risk_level']}"
        )

    return {
        "risk_results": risk_results
    }
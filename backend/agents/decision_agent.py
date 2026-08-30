# agents/decision_agent.py

from typing import Dict, Any, List


def get_recommended_actions(
    risk_level: str,
    risk_type: str
) -> List[str]:
    """
    Generate recommended actions based on
    risk level and risk type.
    """

    actions = []

    if risk_type == "Flood":
        actions.extend(
            [
                "Inspect drainage channels",
                "Monitor low-lying roads",
                "Prepare emergency response teams",
                "Issue warnings for vulnerable areas",
            ]
        )

    elif risk_type == "Air Pollution":
        actions.extend(
            [
                "Issue air-quality health advisory",
                "Monitor sensitive populations",
                "Reduce unnecessary outdoor exposure",
                "Increase pollution monitoring",
            ]
        )

    elif risk_type == "Traffic":
        actions.extend(
            [
                "Monitor congestion hotspots",
                "Optimize traffic signal timing",
                "Deploy traffic management teams",
                "Provide alternate route recommendations",
            ]
        )

    elif risk_type == "Population Exposure":
        actions.extend(
            [
                "Prioritize high-population areas",
                "Prepare emergency communication",
                "Increase public awareness",
            ]
        )

    else:
        actions.append(
            "Continue monitoring the area"
        )

    if risk_level == "CRITICAL":
        actions.insert(
            0,
            "Activate immediate emergency response"
        )

    elif risk_level == "HIGH":
        actions.insert(
            0,
            "Increase monitoring frequency"
        )

    elif risk_level == "MODERATE":
        actions.insert(
            0,
            "Maintain active monitoring"
        )

    return actions


def determine_priority(risk_score: float) -> str:

    if risk_score >= 85:
        return "IMMEDIATE"

    if risk_score >= 70:
        return "HIGH"

    if risk_score >= 40:
        return "MEDIUM"

    return "LOW"


def decision_agent(state: Dict[str, Any]) -> Dict[str, Any]:
    """
    Main Decision Intelligence Agent.
    """

    print("\n" + "=" * 70)
    print("🧠 DECISION INTELLIGENCE AGENT")
    print("=" * 70)

    risk_results = state.get("risk_results", [])

    if not risk_results:
        return {
            "error": "No risk results available."
        }

    decisions = []

    for result in risk_results:

        zone = result["zone"]
        score = result["risk_score"]
        level = result["risk_level"]
        risk_type = result["risk_type"]

        factors = result["factors"]

        # Sort factors by contribution
        sorted_factors = sorted(
            factors.items(),
            key=lambda item: item[1],
            reverse=True
        )

        top_factors = [
            factor[0]
            for factor in sorted_factors[:3]
        ]

        actions = get_recommended_actions(
            level,
            risk_type
        )

        decision = {
            "zone": zone,

            "risk_score": score,

            "risk_level": level,

            "risk_type": risk_type,

            "priority": determine_priority(score),

            "top_contributing_factors": top_factors,

            "trend": (
                "INCREASING"
                if factors["recent_trend"] >= 0.65
                else "STABLE"
            ),

            "risk_horizon": (
                "Immediate"
                if score >= 85
                else "Next 6-24 hours"
                if score >= 70
                else "Next 24-48 hours"
            ),

            "recommended_actions": actions,
        }

        decisions.append(decision)

    # Highest priority zone
    highest_priority = decisions[0]

    summary = {
        "highest_priority_zone":
            highest_priority["zone"],

        "highest_risk_score":
            highest_priority["risk_score"],

        "highest_risk_level":
            highest_priority["risk_level"],

        "total_zones_analyzed":
            len(decisions),

        "critical_zones":
            [
                d["zone"]
                for d in decisions
                if d["risk_level"] == "CRITICAL"
            ],

        "high_risk_zones":
            [
                d["zone"]
                for d in decisions
                if d["risk_level"] == "HIGH"
            ],
    }

    print(
        f"\n🎯 Highest priority zone: "
        f"{highest_priority['zone']}"
    )

    print(
        f"📊 Risk score: "
        f"{highest_priority['risk_score']}"
    )

    print(
        f"🚦 Risk level: "
        f"{highest_priority['risk_level']}"
    )

    return {
        "decisions": {
            "zone_decisions": decisions,
            "summary": summary,
        }
    }
# agents/explanation_agent.py

from typing import Dict, Any


def build_zone_explanation(decision: Dict[str, Any]) -> str:
    """
    Generate human-readable explanation for a zone.
    """

    zone = decision["zone"]
    score = decision["risk_score"]
    level = decision["risk_level"]
    risk_type = decision["risk_type"]

    factors = decision["top_contributing_factors"]

    trend = decision["trend"]

    horizon = decision["risk_horizon"]

    actions = decision["recommended_actions"]

    factor_text = ", ".join(
        factor.replace("_", " ")
        for factor in factors
    )

    action_text = "; ".join(actions)

    explanation = (
        f"{zone} currently has a {level.lower()} risk level "
        f"with a risk score of {score}/100. "
        f"The dominant risk is {risk_type.lower()}. "
        f"The main contributing factors are {factor_text}. "
        f"The recent risk trend is {trend.lower()}, "
        f"with the expected risk horizon being {horizon.lower()}. "
        f"Recommended actions include: {action_text}."
    )

    return explanation


def explanation_agent(
    state: Dict[str, Any]
) -> Dict[str, Any]:
    """
    Main Explanation Intelligence Agent.

    Converts structured decisions into
    human-readable intelligence.
    """

    print("\n" + "=" * 70)
    print("🤖 AI / LLM EXPLANATION AGENT")
    print("=" * 70)

    decisions = state.get("decisions", {})

    zone_decisions = decisions.get(
        "zone_decisions",
        []
    )

    if not zone_decisions:
        return {
            "error": "No decisions available."
        }

    explanations = []

    for decision in zone_decisions:

        explanation = build_zone_explanation(
            decision
        )

        explanations.append(
            {
                "zone": decision["zone"],
                "explanation": explanation,
            }
        )

    summary = decisions.get(
        "summary",
        {}
    )

    highest_zone = summary.get(
        "highest_priority_zone",
        "Unknown"
    )

    highest_score = summary.get(
        "highest_risk_score",
        0
    )

    highest_level = summary.get(
        "highest_risk_level",
        "UNKNOWN"
    )

    final_explanation = (
        f"Lahore City Intelligence Analysis: "
        f"{highest_zone} currently requires the "
        f"highest attention with a risk score of "
        f"{highest_score}/100 ({highest_level}). "
        f"The system recommends prioritizing this area "
        f"for monitoring and response while continuing "
        f"to monitor other identified risk zones."
    )

    # Print result
    print("\n📋 HUMAN-READABLE ANALYSIS:\n")

    print(final_explanation)

    print("\n📍 Zone explanations:\n")

    for item in explanations:

        print(
            f"\n{item['zone']}:"
        )

        print(
            item["explanation"]
        )

    # Structured final response
    final_response = {
        "platform": "Lahore City Intelligence Platform",

        "mission":
            "Predicting Problems Before They Happen",

        "location":
            state.get("location", "Lahore"),

        "summary":
            final_explanation,

        "priority_zone":
            highest_zone,

        "priority_score":
            highest_score,

        "priority_level":
            highest_level,

        "zone_analysis":
            explanations,

        "decisions":
            zone_decisions,
    }

    return {
        "explanation": final_explanation,
        "final_response": final_response,
    }
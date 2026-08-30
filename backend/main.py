# main.py

from graph.workflow import app


def print_final_result(result):
    """
    Print the final structured intelligence.
    """

    print("\n")
    print("=" * 80)
    print("🏙️ LAHORE CITY INTELLIGENCE PLATFORM")
    print("=" * 80)

    final_response = result.get(
        "final_response",
        {}
    )

    print("\n🎯 PROJECT MISSION")
    print("------------------")

    print(
        "Predicting Problems Before They Happen"
    )

    print("\n📍 LOCATION")
    print("-----------")

    print(
        final_response.get(
            "location",
            "Lahore"
        )
    )

    print("\n🚨 PRIORITY ZONE")
    print("----------------")

    print(
        final_response.get(
            "priority_zone",
            "Unknown"
        )
    )

    print("\n📊 RISK SCORE")
    print("-------------")

    print(
        f"{final_response.get('priority_score', 0)}/100"
    )

    print("\n⚠️ RISK LEVEL")
    print("-------------")

    print(
        final_response.get(
            "priority_level",
            "UNKNOWN"
        )
    )

    print("\n🧠 AI EXPLANATION")
    print("-----------------")

    print(
        final_response.get(
            "summary",
            "No explanation available."
        )
    )

    print("\n📋 ALL ZONE ANALYSIS")
    print("--------------------")

    for zone in final_response.get(
        "zone_analysis",
        []
    ):

        print(
            f"\n📍 {zone['zone']}"
        )

        print(
            zone["explanation"]
        )

    print("\n")
    print("=" * 80)
    print("✅ WORKFLOW COMPLETED")
    print("=" * 80)


def main():

    print("\n")
    print("🏙️ ALGO TITANS")
    print("LAHORE CITY INTELLIGENCE PLATFORM")
    print("=" * 80)

    user_query = input(
        "\nAsk the City Intelligence System something "
        "(press Enter for default analysis): "
    ).strip()

    if not user_query:
        user_query = (
            "Analyze current environmental, traffic "
            "and city risks in Lahore."
        )

    # Initial state
    initial_state = {
        "user_query": user_query,
        "location": "Lahore",
    }

    print("\n")
    print("🚀 Starting Agentic AI workflow...")
    print("=" * 80)

    try:

        # Run LangGraph
        result = app.invoke(
            initial_state
        )

        # Display result
        print_final_result(
            result
        )

    except Exception as e:

        print("\n❌ WORKFLOW ERROR")
        print("----------------")

        print(str(e))


if __name__ == "__main__":
    main()
"""
lahore_city_specialist_agent.py

AGENT 2 — Lahore City Intelligence Specialist

Purpose:
    Complete text-to-text conversational agent for the
    Lahore City Intelligence Platform.

The user can ask questions about:

- Risk
- Floods
- Air quality
- AQI
- Traffic
- Weather
- Population exposure
- Spatial intelligence
- ML predictions
- Risk scores
- Risk factors
- Prevention
- Recommendations
- Emergency preparedness
- City intelligence
- Platform architecture
- Data sources
- Machine learning
- AI system
- Decision intelligence
- Prediction explanations
- Dashboard
- Mobile application
- General Lahore city intelligence questions

This agent does NOT invent real-time information.
"""


import os
import json
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


# ============================================================
# ENVIRONMENT
# ============================================================

load_dotenv()

GEMINI_API_KEY = os.getenv(
    "GEMINI_API_KEY"
)

LLM_MODEL = os.getenv(
    "LLM_MODEL",
    "gemini-2.5-flash"
)


# ============================================================
# SPECIALIST SYSTEM PROMPT
# ============================================================

SPECIALIST_SYSTEM_PROMPT = """

You are the Lahore City Intelligence Specialist AI.

You are the main conversational intelligence assistant
for the:

"Lahore City Intelligence Platform"

PROJECT MISSION:

"Predicting Problems Before They Happen."

============================================================
YOUR ROLE
============================================================

You are a specialized text-to-text conversational AI.

Users can ask you almost any question related to the
Lahore City Intelligence Platform and its intelligence
domains.

You should understand the user's intent and provide
the most useful answer.

============================================================
DOMAIN 1 — WEATHER INTELLIGENCE
============================================================

You understand:

- Temperature
- Rainfall
- Rainfall trends
- 1-hour rainfall
- 6-hour rainfall
- 24-hour rainfall
- Humidity
- Wind speed
- Wind direction
- Weather-related risk
- Extreme weather
- Weather impact on Lahore

============================================================
DOMAIN 2 — FLOOD INTELLIGENCE
============================================================

You understand:

- Urban flooding
- Heavy rainfall
- Drainage problems
- Low-lying areas
- Water accumulation
- Flood exposure
- Historical flood risk
- Flood prevention
- Flood preparedness
- Flood response
- Infrastructure vulnerability

============================================================
DOMAIN 3 — AIR QUALITY
============================================================

You understand:

- AQI
- PM2.5
- PM10
- NO2
- SO2
- CO
- O3
- Air pollution
- Pollution trends
- Health implications
- Pollution mitigation
- Air-quality alerts

============================================================
DOMAIN 4 — TRAFFIC INTELLIGENCE
============================================================

You understand:

- Traffic congestion
- Traffic index
- Average speed
- Road density
- Traffic hotspots
- Congestion trends
- Traffic risk
- Transportation planning
- Traffic management
- Alternate routes

============================================================
DOMAIN 5 — SPATIAL INTELLIGENCE
============================================================

You understand:

- Lahore zones
- Administrative areas
- Roads
- Buildings
- Schools
- Hospitals
- POIs
- Road density
- Waterways
- Population exposure
- Geographic risk
- Spatial risk
- Risk maps
- GIS
- PostGIS

============================================================
DOMAIN 6 — RISK INTELLIGENCE
============================================================

Risk score:

0-39   = LOW
40-69  = MODERATE
70-84  = HIGH
85-100 = CRITICAL

You can explain:

- Risk score
- Risk level
- Risk type
- Risk factors
- Risk trends
- Historical risk
- Exposure
- Risk horizon
- High-risk zones
- Critical zones

============================================================
DOMAIN 7 — MACHINE LEARNING
============================================================

The platform can use ML models such as:

- Logistic Regression
- Random Forest
- Gradient Boosting
- XGBoost
- LightGBM
- Ensemble Models

You can explain:

- Features
- Training
- Prediction
- Probability
- Classification
- Regression
- Feature engineering
- Model evaluation
- Precision
- Recall
- F1
- Accuracy
- Feature importance
- Model registry

============================================================
DOMAIN 8 — DECISION INTELLIGENCE
============================================================

You can answer:

- Which areas need attention first?
- Why is an area risky?
- Which factors contribute most?
- What actions should be taken?
- What should authorities prioritize?
- What should citizens do?
- What is the expected risk horizon?
- How can risk be reduced?
- Which zone has the highest priority?

============================================================
DOMAIN 9 — AI / LLM
============================================================

You understand:

- LLMs
- Generative AI
- AI agents
- Agentic AI
- LLM explanations
- Text-to-text systems
- Prompt engineering
- Context
- Structured JSON
- ML + LLM architecture

IMPORTANT:

The ML model makes predictions.

The LLM explains and communicates predictions.

Never claim that the LLM itself generated the
ML prediction unless explicitly told that it did.

============================================================
DOMAIN 10 — PLATFORM ARCHITECTURE
============================================================

Understand this architecture:

Data Sources
      ↓
Data Ingestion
      ↓
Data Validation
      ↓
Normalization
      ↓
Data Storage
      ↓
Spatial Processing
      ↓
Feature Engineering
      ↓
ML Engine
      ↓
Risk Engine
      ↓
Decision Intelligence
      ↓
LLM Explanation
      ↓
Alerts
      ↓
Structured Output
      ↓
Web Dashboard / Mobile App

Potential data sources include:

- Weather APIs
- Air quality APIs
- OpenStreetMap
- Traffic APIs
- Punjab statistics
- Population datasets
- Humanitarian datasets
- Historical risk datasets

============================================================
CURRENT DATA RULE
============================================================

You MUST NOT pretend that you have live/current data.

If current live data has not been supplied to you,
say:

"I don't currently have live data for that."

Then explain what data would be needed.

Do not invent:

- Current AQI
- Current weather
- Current traffic
- Current flood status
- Current emergency status
- Current risk scores

============================================================
PREDICTION CONTEXT
============================================================

Sometimes the system will provide an ML prediction.

Example:

{
    "risk_score": 81.43,
    "risk_level": "HIGH",
    "risk_type": "Flood"
}

When this context is provided:

- Use it.
- Explain it.
- Do not modify it.
- Do not invent another score.
- Treat it as the trusted ML result.

============================================================
CONVERSATION
============================================================

Maintain the context provided in conversation history.

If the user asks:

"Why?"

Understand what "why" refers to from the previous
conversation.

If the user asks:

"Explain this."

Use the supplied prediction/data context.

============================================================
ANSWER STYLE
============================================================

Your answers should be:

- Clear
- Helpful
- Accurate
- Practical
- Natural
- Easy to understand

For technical questions:

Explain technically but avoid unnecessary complexity.

For general users:

Use simple language.

For decision makers:

Focus on:

- Priority
- Risk
- Impact
- Action
- Recommendation

============================================================
SAFETY
============================================================

Do not provide fabricated emergency information.

Do not claim a location is currently dangerous
without current supporting data.

For real emergencies, recommend contacting the
appropriate local emergency authorities.

============================================================
FINAL RULE
============================================================

You are the conversational intelligence layer.

ML = prediction.

Data = evidence.

LLM = explanation, reasoning over supplied context,
conversation and recommendations.

Never confuse these roles.

"""


# ============================================================
# AGENT CLASS
# ============================================================

class LahoreCitySpecialistAgent:
    """
    Complete text-to-text conversational specialist.

    Input:
        User question
        Optional prediction
        Optional city data
        Optional conversation history

    Output:
        UI-ready JSON
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        model: Optional[str] = None
    ):

        self.api_key = (
            api_key
            or GEMINI_API_KEY
        )

        self.model_name = (
            model
            or LLM_MODEL
        )

        if not self.api_key:

            raise ValueError(
                "GEMINI_API_KEY is missing. "
                "Add it to your .env file."
            )

        self.llm = ChatGoogleGenerativeAI(

            model=self.model_name,

            google_api_key=self.api_key,

            temperature=0.3,

            max_output_tokens=1500,
        )

    # ========================================================
    # BUILD CONTEXT
    # ========================================================

    @staticmethod
    def _build_context(
        location: str,
        prediction_context: Optional[Dict[str, Any]],
        city_data: Optional[Dict[str, Any]]
    ) -> str:

        context = {

            "location":
                location,

            "prediction_context":
                prediction_context
                or {},

            "city_data":
                city_data
                or {}
        }

        return json.dumps(
            context,
            indent=2,
            ensure_ascii=False
        )

    # ========================================================
    # BUILD CONVERSATION
    # ========================================================

    @staticmethod
    def _build_history(
        conversation_history:
            Optional[List[Dict[str, str]]]
    ) -> str:

        if not conversation_history:

            return (
                "No previous conversation."
            )

        history_text = []

        for message in conversation_history:

            role = message.get(
                "role",
                "user"
            )

            content = message.get(
                "content",
                ""
            )

            history_text.append(
                f"{role.upper()}: {content}"
            )

        return "\n".join(
            history_text
        )

    # ========================================================
    # GENERATE RESPONSE
    # ========================================================

    def generate_response(
        self,
        user_query: str,
        location: str,
        prediction_context:
            Optional[Dict[str, Any]] = None,
        city_data:
            Optional[Dict[str, Any]] = None,
        conversation_history:
            Optional[List[Dict[str, str]]] = None
    ) -> str:
        """
        Send user query + available context to LLM.
        """

        context = self._build_context(

            location=location,

            prediction_context=
                prediction_context,

            city_data=
                city_data
        )

        history = self._build_history(
            conversation_history
        )

        prompt = f"""
LOCATION:

{location}


AVAILABLE SYSTEM CONTEXT:

{context}


PREVIOUS CONVERSATION:

{history}


USER QUESTION:

{user_query}


Answer the user as the Lahore City Intelligence
Specialist.

Use the available context when relevant.

If the user asks for current/live information and
no current data is supplied, clearly state that
live data is unavailable.

If an ML prediction is supplied, explain that
prediction without changing it.

Give a direct answer first, then useful explanation
or recommendations where appropriate.
"""

        response = self.llm.invoke(

            [
                (
                    "system",
                    SPECIALIST_SYSTEM_PROMPT
                ),

                (
                    "human",
                    prompt
                )
            ]
        )

        content = response.content

        # Handle structured response blocks
        if isinstance(
            content,
            list
        ):

            parts = []

            for item in content:

                if isinstance(
                    item,
                    dict
                ):

                    text = item.get(
                        "text"
                    )

                    if text:
                        parts.append(text)

                elif isinstance(
                    item,
                    str
                ):

                    parts.append(item)

            content = "\n".join(parts)

        return str(content).strip()

    # ========================================================
    # MAIN AGENT
    # ========================================================

    def run(
        self,
        user_query: str,
        location: str = "Lahore",
        prediction_context:
            Optional[Dict[str, Any]] = None,
        city_data:
            Optional[Dict[str, Any]] = None,
        conversation_history:
            Optional[List[Dict[str, str]]] = None
    ) -> Dict[str, Any]:
        """
        Main text-to-text agent function.

        Returns JSON suitable for your UI.
        """

        try:

            if not user_query.strip():

                return {

                    "success": False,

                    "agent":
                        "lahore_city_specialist",

                    "error":
                        "User query cannot be empty."
                }

            response = (
                self.generate_response(

                    user_query=
                        user_query,

                    location=
                        location,

                    prediction_context=
                        prediction_context,

                    city_data=
                        city_data,

                    conversation_history=
                        conversation_history
                )
            )

            return {

                "success": True,

                "agent":
                    "lahore_city_specialist",

                "location":
                    location,

                "query":
                    user_query,

                "response":
                    response,

                "context_used": {

                    "prediction":
                        bool(
                            prediction_context
                        ),

                    "city_data":
                        bool(
                            city_data
                        ),

                    "conversation_history":
                        bool(
                            conversation_history
                        )
                }
            }

        except Exception as e:

            return {

                "success": False,

                "agent":
                    "lahore_city_specialist",

                "error":
                    str(e)
            }


# ============================================================
# GLOBAL AGENT
# ============================================================

lahore_city_specialist_agent = (
    LahoreCitySpecialistAgent()
)


# ============================================================
# SIMPLE FUNCTION FOR FASTAPI / FLASK / UI
# ============================================================

def chat_with_city_specialist(
    user_query: str,
    location: str = "Lahore",
    prediction_context:
        Optional[Dict[str, Any]] = None,
    city_data:
        Optional[Dict[str, Any]] = None,
    conversation_history:
        Optional[List[Dict[str, str]]] = None
) -> Dict[str, Any]:
    """
    Simple function your API/UI can call.
    """

    return (
        lahore_city_specialist_agent.run(

            user_query=user_query,

            location=location,

            prediction_context=
                prediction_context,

            city_data=
                city_data,

            conversation_history=
                conversation_history
        )
    )


# ============================================================
# LOCAL TEST
# ============================================================

if __name__ == "__main__":

    print(
        "\n🏙️ Lahore City Intelligence Specialist"
    )

    print(
        "Type 'exit' to stop.\n"
    )

    history = []

    while True:

        question = input(
            "You: "
        ).strip()

        if question.lower() in [
            "exit",
            "quit"
        ]:

            break

        result = (
            chat_with_city_specialist(

                user_query=
                    question,

                location=
                    "Lahore",

                conversation_history=
                    history
            )
        )

        print(
            "\nAI:"
        )

        print(
            result.get(
                "response",
                result.get(
                    "error",
                    "No response."
                )
            )
        )

        # Save conversation
        if result.get("success"):

            history.append(
                {
                    "role": "user",
                    "content": question
                }
            )

            history.append(
                {
                    "role": "assistant",
                    "content":
                        result["response"]
                }
            )

        print()
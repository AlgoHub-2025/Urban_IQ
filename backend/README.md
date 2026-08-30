# Lahore City Intelligence Platform

A city intelligence and risk monitoring platform for Lahore, Pakistan. The system combines an agent-based workflow, geospatial and environmental datasets, and ML models to analyze risks such as air pollution, traffic congestion, flooding, and urban exposure.

This project is designed to simulate an intelligent city operations system that can:

- collect city data,
- validate and engineer features,
- assess risk by zone,
- recommend actions,
- and explain the analysis in a human-readable format.

---

## Project Goal

The project aims to build an AI-driven city intelligence platform that helps predict and prioritize critical urban risks before they escalate. It focuses on Lahore and integrates:

- weather data,
- air quality metrics,
- traffic risk indicators,
- spatial and population exposure features,
- historical risk signals,
- and trained machine learning models.

---

## Project Architecture

The project is organized into the following parts:

### 1. Agent Workflow
The core agent orchestration is defined in:

- `graph/workflow.py`
- `state.py`

The workflow follows this chain:

- Data Agent
- Risk Agent
- Decision Agent
- Explanation Agent

This is implemented using a LangGraph state graph.

### 2. AI Agents
Each agent handles a specific responsibility:

- `agents/data_agent.py` – collects and validates data, creates engineered features
- `agents/risk_agent.py` – computes risk scores and risk categories by zone
- `agents/decision_agent.py` – decides priority and recommended actions
- `agents/explanation_agent.py` – transforms the structured decision output into readable analysis

### 3. ML Models
Model training scripts are stored under:

- `ml-notebooks/`

These scripts train models for:

- air quality forecasting,
- hospital classification,
- population density regression,
- road type classification,
- school classification,
- waterway classification,
- weather forecasting.

### 4. Data Processing
The data pipeline scripts are in:

- `Data/`

These scripts handle the extraction, transformation, and merging of city datasets.

### 5. Dataset Storage
The datasets are stored in:

- `datasets/`

### 6. Model Artifacts and Outputs
Generated trained models and outputs are stored in:

- `models/`
- `outputs/`
- `reports/`

---

## Folder Structure

```text
Lahore city intelligence platform/
├── agents/
│   ├── data_agent.py
│   ├── decision_agent.py
│   ├── explanation_agent.py
│   └── risk_agent.py
├── Data/
│   ├── extract_osm_data.py
│   ├── fetch_air_quality_aqicn.py
│   ├── fetch_weather.py
│   ├── merge_data.py
│   ├── process_population.py
│   └── ...
├── datasets/
│   ├── air_quality_data.csv
│   ├── air_quality_forecast.csv
│   ├── hospitals_lahore.csv
│   ├── population_data.csv
│   ├── roads_lahore.csv
│   ├── schools_lahore.csv
│   ├── waterways_lahore.csv
│   └── weather_data.csv
├── graph/
│   └── workflow.py
├── ml-notebooks/
│   ├── air_quality_forecast_model.py
│   ├── hospital_classifier.py
│   ├── population_density_regression.py
│   ├── road_type_classifier.py
│   ├── school_classifier.py
│   ├── waterway_type_classifier.py
│   └── weather_forecast_model.py
├── models/
├── outputs/
├── reports/
├── .venv/
├── main.py
├── state.py
├── README.md
├── datasets.zip
└── ...
```

---

## Environment Setup

### Prerequisites

You need:

- Python 3.10+
- pip
- virtual environment support

### Create and activate virtual environment

On Windows:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

On macOS/Linux:

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies

```bash
pip install -r requirements.txt
```

If there is no `requirements.txt` file, install the common dependencies manually:

```bash
pip install langgraph pandas numpy scikit-learn xgboost joblib matplotlib seaborn
```

---

## Running the Project

### Start the city intelligence workflow

From the project root:

```bash
python main.py
```

This interactive app asks:

- a city analysis question,
- then runs the agent workflow,
- and prints a risk summary with priority zone and recommendations.

### Example input

```text
Analyze current environmental, traffic and city risks in Lahore.
```

The output includes:

- priority zone,
- risk score,
- risk level,
- AI summary,
- zone-wise analysis,
- recommended actions.

---

## How the Workflow Works

### Step 1: Data Agent
The system collects the following simulated data:

- weather
- air quality
- traffic
- spatial metrics
- historical risk indicators

Then it validates the values and performs feature engineering.

### Step 2: Risk Agent
The risk engine calculates:

- rainfall feature,
- AQI feature,
- traffic feature,
- exposure feature,
- historical risk,
- and recent trend.

It produces a zone-level risk score for Lahore areas such as:

- Central Lahore
- Gulberg
- Johar Town
- DHA Lahore
- Ravi Zone

### Step 3: Decision Agent
The decision agent chooses:

- highest priority zone,
- risk horizons,
- recommended actions,
- and top contributing factors.

### Step 4: Explanation Agent
This module converts technical outputs into human-readable city intelligence summaries.

---

## ML Notebook Workflow

The training pipeline is separated into model scripts under `ml-notebooks/`.

### Run each model manually

From the project root:

```bash
python ml-notebooks/air_quality_forecast_model.py --input datasets/air_quality_data.csv --output outputs/air_quality_forecast.json --model-dir models/air_quality
```

```bash
python ml-notebooks/hospital_classifier.py --input datasets/hospitals_lahore.csv --output outputs/hospitals_predictions.json --model-dir models/hospitals
```

```bash
python ml-notebooks/population_density_regression.py --input datasets/population_data.csv --output outputs/population_density_predictions.json --model-dir models/population
```

```bash
python ml-notebooks/road_type_classifier.py --input datasets/roads_lahore.csv --output outputs/roads_predictions.json --model-dir models/roads
```

```bash
python ml-notebooks/school_classifier.py --input datasets/schools_lahore.csv --output outputs/schools_predictions.json --model-dir models/schools
```

```bash
python ml-notebooks/waterway_type_classifier.py --input datasets/waterways_lahore.csv --output outputs/waterways_predictions.json --model-dir models/waterways
```

```bash
python ml-notebooks/weather_forecast_model.py --input datasets/weather_data.csv --output outputs/weather_forecast.json --model-dir models/weather
```

### Model outputs
Each script saves:

- trained model file(s) in `models/...`
- prediction results in `outputs/...`
- test-set evaluation outputs in files ending with `_test_predictions.json`

---

## Data Sources and Processing

The platform uses a combination of generated and structured city data.

### Data scripts
The following scripts are used to collect and merge city-level data:

- `Data/fetch_weather.py`
- `Data/fetch_air_quality_aqicn.py`
- `Data/extract_osm_data.py`
- `Data/process_population.py`
- `Data/merge_data.py`

These scripts prepare the foundation for city-scale forecasting and risk analysis.

---

## Risk Scoring Logic

The system uses a weighted risk formula in the `risk_agent.py` logic.

Example concept:

```python
score = (
    rainfall * 20
    + aqi * 20
    + traffic * 15
    + exposure * 15
    + historical * 20
    + trend * 10
)
```

Risk classification:

- 0-39: LOW
- 40-69: MODERATE
- 70-84: HIGH
- 85-100: CRITICAL

---

## Example Use Cases

This project can be used for:

- early identification of flood-prone zones,
- air-quality health alerts,
- traffic hotspot monitoring,
- institution placement analysis,
- emergency prioritization,
- city planning and infrastructure intelligence.

---

## Current Status

The project is currently built as a hybrid system combining:

- an agentic workflow,
- synthetic/structured city intelligence data,
- and trained ML models for forecasting and classification.

The platform successfully demonstrates an end-to-end AI city monitoring workflow for Lahore.

---

## Notes for Future Improvement

The current version uses mock data in the agent workflow. The following upgrades are recommended:

1. Replace mock weather and AQI data with real APIs.
2. Add real GIS/OSM spatial layers.
3. Connect to a PostgreSQL/PostGIS database.
4. Use actual Lahore zoning data instead of synthetic zones.
5. Integrate model predictions directly into agent decision logic.
6. Add a web dashboard or REST API.
7. Add an authentication and user management layer.

---

## Quick Start Summary

1. Create the virtual environment.
2. Install dependencies.
3. Run:

```bash
python main.py
```

4. Ask a query such as:

```text
Analyze current environmental, traffic and city risks in Lahore.
```

5. Train the ML models using the scripts in `ml-notebooks/`.
6. Review the generated outputs in `outputs/` and `models/`.

---

## License

This project is intended for research, experimentation, and demonstration purposes for Lahore urban intelligence and city monitoring.

---

## Contributors

This project was developed as a city intelligence and AI prototype for Lahore based on urban risk analysis and decision support workflows.

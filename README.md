<div align="center">
  <img src="docs/images/hero.png" alt="Lahore Nexus Logo" width="200" />
  
  # Lahore Nexus (Urban_IQ) 🏙️ 
  
  **Intelligent Urban Decision-Support & Response Twin for Lahore**

  > *"Prediction tells us what may happen, Response Twin helps us test what we can do about it, and Citizen Intelligence connects ground reality with verified evidence."*

  [![React](https://img.shields.io/badge/React-20232A?style=for-the-badge&logo=react&logoColor=61DAFB)](https://reactjs.org/)
  [![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)](https://fastapi.tiangolo.com/)
  [![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-38B2AC?style=for-the-badge&logo=tailwind-css&logoColor=white)](https://tailwindcss.com/)
  [![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org/)
</div>

---

## 🌟 About The Project

**Lahore Nexus** (developed under `AlgoHub-2025/Urban_IQ`) transforms fragmented city data into a unified, intelligent decision-support system. Designed for city administrators and emergency responders, it doesn't just monitor urban issues—it predicts risks, explains the reasoning behind them, and allows operators to simulate interventions in real-time.

Instead of operating as a black-box AI, Lahore Nexus is built on **Explainable AI (XAI)**, strict **Role-Based Access Control (RBAC)**, and **Human-in-the-Loop** verification, ensuring that no AI-generated signal becomes "ground truth" without human validation.

---

## 📸 Dashboard & Core Features

### 1. City Overview & Map Command
The centralized nerve center. View city-wide metrics, live alerts, hospital capacities, and active field operations across Lahore's zones (e.g., Gulberg, DHA, Johar Town).
<p align="center">
  <img src="docs/images/map-command.png" alt="Map Command Center" width="800" />
  <br/><i>Navigate geo-spatial intelligence dynamically with live layers for hospitals, roads, and verified citizen reports.</i>
</p>

### 2. Predictive Risk Engine (Heavy Rain Scenario)
Machine learning models predict how upcoming weather events (like heavy rainfall) will impact specific zones, calculating risks like waterlogging, traffic bottlenecks, and population exposure.
<p align="center">
  <img src="docs/images/predictive-risk.png" alt="Predictive Risk Dashboard" width="800" />
  <br/><i>Trigger a "Heavy Rain" scenario and watch the risk scores autonomously adapt based on live environmental variables.</i>
</p>

### 3. Urban Response Twin (What-If Simulator)
The **Golden Feature**. Don't just predict the disaster—simulate the solution. Operators can toggle interventions (e.g., "Drainage Clearance", "Traffic Diversion") and instantly see the projected drop in the Risk Score.
<p align="center">
  <img src="docs/images/response-twin.png" alt="Response Twin Simulator" width="800" />
  <br/><i>Simulate "Drainage Clearance" and watch the zone Risk Score drop from 82 to 61 in real-time.</i>
</p>

### 4. AI Incident Commander & Data Trust
An autonomous chat agent that can interrogate the underlying graphs and metrics. Features a **Data Trust Layer** that exposes the AI's exact thought process (Intent, Confidence, Grounded Evidence).
<p align="center">
  <img src="docs/images/explainable-ai.png" alt="Explainable AI Commander" width="800" />
  <br/><i>See exactly WHY the AI made a recommendation through the transparent Data Provenance sidebar.</i>
</p>

### 5. Citizen Intelligence (Human-in-the-Loop)
Citizens report issues via image uploads with geographic coordinates. To maintain absolute data integrity, the system flags these as `Pending`. Only after a human Operator clicks "Verify" does the incident appear on the live Map Command.
<p align="center">
  <img src="docs/images/citizen-intelligence.png" alt="Citizen Intelligence Module" width="800" />
  <br/><i>Strict verification workflow. Features Lahore-bound coordinate validation (31.3-31.7 N) and path-traversal security.</i>
</p>

---

## 🔐 Security & Architecture

* **Role-Based Access Control (RBAC)**: Switch between `Admin`, `Operator`, and `Viewer`. Viewers have strictly read-only access (mutating endpoints block them at the API layer).
* **Strict Geo-Fencing**: Citizen reports are cryptographically hashed and rejected if their GPS coordinates fall outside Lahore boundaries (31.3–31.7°N, 74.1–74.5°E).
* **Transparent Execution**: AI outputs never manipulate the core Risk Engine directly without passing through operator oversight.

---

## 🛠️ Tech Stack

### Frontend
- **React.js (Vite)**
- **Tailwind CSS** (for highly interactive, glassmorphism-based UI)
- **Lucide React** (Icons)
- **React-Leaflet** (Geo-Spatial mapping)

### Backend
- **FastAPI** (Python 3)
- **Scikit-learn** (Risk prediction modeling)
- **LangGraph** (Agentic AI Workflow)
- **Pytest** (Automated Security Testing)

---

## 🚀 Getting Started

Follow these steps to run the Lahore Nexus system locally.

### 1. Clone the Repository
```bash
git clone https://github.com/AlgoHub-2025/Urban_IQ.git
cd Urban_IQ
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv
source venv/bin/activate  # (On Windows use: venv\Scripts\activate)
pip install -r requirements.txt

# Start the API server
uvicorn api:app --reload --port 8009
```
*The backend will be running at `http://localhost:8009`.*

### 3. Frontend Setup
Open a new terminal window:
```bash
cd frontend
npm install

# Start the Vite development server
npm run dev
```
*The application will be accessible at `http://localhost:5173` (or the port specified by Vite).*

---

## 🎯 The Golden Demo Script

If you are presenting this project, follow this exact sequence:

1. **Opening**: Open Map Command. *"Lahore Nexus fragmented city data ko ek intelligent decision-support system mein convert karta hai."*
2. **Predict**: Trigger **Heavy Rain Scenario**. *"Machine Learning hume batata hai ke conditions worsen hon to risk kis direction mein ja sakta hai."*
3. **Explain**: Show the **AI Commander / Data Trust** pane. *"Hum black-box AI use nahi karte. Har risk ki logic transparent hai."*
4. **Simulate (Hero Moment)**: Open **Response Twin**, apply *Drainage Clearance*. Note the Risk Score drop (82 → 61). Pause. *"Prediction tells us what may happen. Response Twin helps us test what we can do about it."*
5. **Verify**: Show **Citizen Intelligence**. Upload a report -> Verify it -> Show it magically appear on the main map. *"Citizen signal receive hota hai, lekin human verification ke baghair system usay ground truth nahi maanta."*
6. **Closing**: *"From predicting the problem to testing the solution."*

---

<div align="center">
  Built with ❤️ for Lahore by <b>AlgoHub 2025</b>
</div>

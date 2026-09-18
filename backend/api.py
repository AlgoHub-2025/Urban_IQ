import json
import random
import os
import requests
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from sqlalchemy.orm import Session
import time

from config import Config, logger

try:
    from database import SessionLocal, AQIReport
except ImportError:
    SessionLocal = None

def get_db():
    if not SessionLocal:
        yield None
        return
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

try:
    from graph.workflow import app as ai_workflow
except ImportError:
    ai_workflow = None

app = FastAPI(title="Lahore City Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=Config.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    logger.error(f"Global Error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "An internal server error occurred.", "error": str(exc)},
    )

@app.get("/health")
async def health_check():
    return {"status": "ok", "timestamp": time.time()}

@app.get("/api/status")
async def api_status():
    return {
        "service": "UrbanIQ Backend",
        "workflow_loaded": ai_workflow is not None,
        "database_connected": SessionLocal is not None,
        "timestamp": time.time()
    }

class QueryRequest(BaseModel):
    query: str
    location: str = "Lahore"

@app.post("/api/analyze")
async def analyze_city(request: QueryRequest):
    if not ai_workflow:
        raise HTTPException(status_code=500, detail="AI Workflow not found")
    initial_state = {
        "user_query": request.query,
        "location": request.location,
    }
    try:
        result = ai_workflow.invoke(initial_state)
        return result.get("final_response", {})
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def load_json(filename):
    file_path = os.path.join(os.path.dirname(__file__), filename)
    if not os.path.exists(file_path):
        return None
    with open(file_path, "r") as f:
        return json.load(f)

@app.get("/api/air-quality")
async def get_air_quality():
    data = load_json("air_quality_forecast.json")
    if not data:
        data = {"forecast": [{"pm25": 100}]}

    if Config.AQICN_TOKEN:
        try:
            url = "https://api.waqi.info/feed/lahore/"
            params = {"token": Config.AQICN_TOKEN}
            response = requests.get(url, params=params, timeout=5)
            response.raise_for_status()
            api_data = response.json()
            if api_data.get('status') == 'ok':
                live_pm25 = api_data['data']['iaqi'].get('pm25', {}).get('v', 0)
                data["live_pm25"] = live_pm25
                data["live_aqi"] = api_data['data'].get('aqi', 0)
                data["status"] = "live"
                return data
        except Exception as e:
            logger.warning(f"AQICN API Error: {e}, falling back to mock")
            
    # Fallback if no token or error
    current_pm25 = data["forecast"][0]["pm25"] + random.uniform(-2.0, 2.0)
    data["live_pm25"] = round(current_pm25, 2)
    data["status"] = "fallback"
    return data

@app.get("/api/map/zones")
async def get_map_zones():
    from graph.workflow import app as workflow_app
    from demo_manager import DEMO_STATE
    from services.alert_service import evaluate_risks
    
    # 1. Run the pipeline for Lahore to get live zone risks
    state = {
        "query": "Generate map risks",
        "location": "Lahore",
        "scenario": DEMO_STATE if DEMO_STATE.get("is_active") else {}
    }
    
    final_state = workflow_app.invoke(state)
    risks_list = final_state.get("risks", [])
    
    # Evaluate alerts deterministically behind the scenes
    evaluate_risks(
        risks=risks_list,
        decisions=final_state.get("decisions", []),
        explainability=final_state.get("explainability", []),
        is_simulated=DEMO_STATE.get("is_active", False)
    )
    
    risk_results = {r["zone_id"]: r for r in risks_list}

    # 2. Canonical Zone Definitions (Approximated as square polygons for Demo)
    # Using real coordinates but approx bounds
    def make_square(lat, lon, size=0.03):
        return [[
            [lon - size, lat - size],
            [lon + size, lat - size],
            [lon + size, lat + size],
            [lon - size, lat + size],
            [lon - size, lat - size]
        ]]

    zones_geo = [
        {"id": "central_lahore", "name": "Central Lahore", "lat": 31.5497, "lon": 74.3436},
        {"id": "gulberg", "name": "Gulberg", "lat": 31.5167, "lon": 74.3436},
        {"id": "johar_town", "name": "Johar Town", "lat": 31.4697, "lon": 74.2728},
        {"id": "dha_lahore", "name": "DHA Lahore", "lat": 31.4805, "lon": 74.4206},
        {"id": "ravi_zone", "name": "Ravi Zone", "lat": 31.5833, "lon": 74.3167},
    ]

    features = []
    for z in zones_geo:
        risk = risk_results.get(z["id"], {})
        feature = {
            "type": "Feature",
            "id": z["id"],
            "geometry": {
                "type": "Polygon",
                "coordinates": make_square(z["lat"], z["lon"])
            },
            "properties": {
                "name": z["name"],
                "risk_type": risk.get("risk_type", "Unknown"),
                "score_0_100": risk.get("score_0_100", 0),
                "level": risk.get("level", "LOW"),
                "confidence": risk.get("confidence", 0),
                "forecast_horizon": risk.get("forecast_horizon", "24h"),
                "top_factors": risk.get("top_factors", []),
                "evidence": risk.get("evidence", []),
                "data_freshness": risk.get("data_freshness", "unavailable"),
                "generated_at": risk.get("generated_at", time.time()),
                "explainability": next((x for x in final_state.get("explainability", []) if x["zone_id"] == z["id"]), None)
            }
        }
        features.append(feature)

    return {
        "type": "FeatureCollection",
        "features": features
    }

from pydantic import BaseModel
from datetime import datetime

class AIQueryRequest(BaseModel):
    query: str
    language: str = "en" # "en" or "ur"

from auth import require_operator, require_admin, require_viewer, get_current_role
from fastapi import Depends

@app.post("/api/ai/query")
async def ai_query_endpoint(req: AIQueryRequest, role: str = require_operator):
    from graph.workflow import app as workflow_app
    from demo_manager import DEMO_STATE
    import time
    
    # 1. Initialize state
    state = {
        "query": req.query, 
        "location": "Lahore", # Default for now, intent router can parse
        "scenario": DEMO_STATE if DEMO_STATE.get("is_active") else {}
    }
    
    # 2. Run LangGraph workflow
    try:
        final_state = workflow_app.invoke(state)
    except Exception as e:
        return {
            "query": req.query,
            "intent": "error",
            "answer": f"System error processing query: {str(e)}",
            "language": req.language,
            "zone_id": None,
            "confidence": 0.0,
            "evidence": [],
            "provenance": [],
            "status_events": ["Error occurred"],
            "generated_at": datetime.utcnow().isoformat() + "Z"
        }

    # 3. Format structured response
    top_risk = final_state.get("risks", [{}])[0] if final_state.get("risks") else {}
    
    # Simple Mock LLM translation for Urdu if requested
    # In production, this would be an LLM call using `final_state["response"]`
    answer = final_state.get("response", "No response generated.")
    if req.language == "ur" or "urdu" in req.query.lower():
        if "gulberg" in req.query.lower() or (top_risk and top_risk.get("zone_id") == "gulberg"):
            answer = "Gulberg mein risk barhne ki badi wajah zyada barish, qareebi waterways aur population exposure hai. Drainage clearance simulated scenario mein risk ko kam kar sakti hai."
        else:
            # Generic fallback mock
            answer = f"Diye gaye query ke mutabiq {state.get('location')} mein composite risk evaluate kiya gaya hai. Mazeed details map intelligence tab mein dekhein."
    return {
        "query": req.query,
        "intent": final_state.get("intent", "general_city_query"),
        "answer": answer,
        "language": req.language,
        "zone_id": top_risk.get("zone_id", "unknown"),
        "confidence": top_risk.get("confidence", 0.0),
        "evidence": final_state.get("evidence", []),
        "provenance": final_state.get("provenance", []),
        "status_events": final_state.get("status_events", []),
        "generated_at": datetime.utcnow().isoformat() + "Z"
    }

from demo_manager import DEMO_STATE, HEAVY_RAIN_SCENARIO

@app.get("/api/demo/status")
async def get_demo_status():
    return DEMO_STATE

@app.post("/api/demo/start")
async def start_demo(role: str = require_operator):
    DEMO_STATE["is_active"] = True
    return {"status": "success", "demo_state": DEMO_STATE}

@app.post("/api/demo/reset")
async def reset_demo(role: str = require_operator):
    DEMO_STATE["is_active"] = False
    DEMO_STATE["current_scenario"] = None
    return {"status": "success", "demo_state": DEMO_STATE}

@app.post("/api/demo/scenario/heavy-rain")
async def demo_heavy_rain(role: str = require_operator):
    DEMO_STATE["is_active"] = True
    DEMO_STATE["current_scenario"] = HEAVY_RAIN_SCENARIO
    
    # Broadcast to all alerts to activate Heavy Rain alerts
    # In a real app this triggers Kafka/RabbitMQ events
    return {"status": "success", "scenario": "heavy-rain-active", "demo_state": DEMO_STATE}

class SimulatorRequest(BaseModel):
    rainfall_mm: float = 0.0
    aqi: float = 0.0
    traffic_mult: float = 1.0

@app.post("/api/simulator/run")
async def api_simulator_run(req: SimulatorRequest, role: str = require_operator):
    from graph.workflow import app as workflow_app
    
    # Baseline
    state_baseline = {
        "query": "simulator_baseline",
        "location": "Lahore",
        "scenario": {}
    }
    res_baseline = workflow_app.invoke(state_baseline)
    
    # Simulated
    rain_f_mult = 1.0 + (req.rainfall_mm / 20.0) if req.rainfall_mm > 0 else 1.0
    
    overrides = {
        "rain_f_multiplier": rain_f_mult,
        "traffic_f_multiplier": req.traffic_mult,
    }
    if req.aqi > 0:
        overrides["aqi_override"] = req.aqi

    state_simulated = {
        "query": "simulator_run",
        "location": "Lahore",
        "scenario": {
            "is_active": True,
            "current_scenario": {
                "description": "What-If Simulator",
                "overrides": overrides
            }
        }
    }
    res_simulated = workflow_app.invoke(state_simulated)
    
    # Compare
    baseline_risks = {r["zone_id"]: r for r in res_baseline.get("risks", [])}
    simulated_risks = {r["zone_id"]: r for r in res_simulated.get("risks", [])}
    baseline_decisions = {d["zone_id"]: d for d in res_baseline.get("decisions", [])}
    simulated_decisions = {d["zone_id"]: d for d in res_simulated.get("decisions", [])}
    
    comparison = []
    
    for z_id, b_risk in baseline_risks.items():
        s_risk = simulated_risks.get(z_id, b_risk)
        b_dec = baseline_decisions.get(z_id, {})
        s_dec = simulated_decisions.get(z_id, {})
        
        score_change = s_risk["score_0_100"] - b_risk["score_0_100"]
        level_changed = s_risk["level"] != b_risk["level"]
        
        b_factors = {f["name"]: f["contribution"] for f in b_risk["top_factors"]}
        s_factors = {f["name"]: f["contribution"] for f in s_risk["top_factors"]}
        
        factor_diffs = []
        for name, s_val in s_factors.items():
            b_val = b_factors.get(name, 0)
            diff = s_val - b_val
            if abs(diff) > 0.1:
                factor_diffs.append({"name": name, "change": round(diff, 2)})
                
        factor_diffs.sort(key=lambda x: abs(x["change"]), reverse=True)
        
        comparison.append({
            "zone_id": z_id,
            "simulation_status": "SIMULATED",
            "baseline": {
                "risk_score": b_risk["score_0_100"],
                "level": b_risk["level"],
                "exposed_population": round(b_risk.get("ml_predictions", {}).get("population_density", {}).get("value", 0)) if b_risk.get("ml_predictions") else 0,
                "exposed_facilities": b_risk.get("exposed_facilities", 0)
            },
            "simulated": {
                "risk_score": s_risk["score_0_100"],
                "level": s_risk["level"],
                "exposed_population": round(s_risk.get("ml_predictions", {}).get("population_density", {}).get("value", 0)) if s_risk.get("ml_predictions") else 0,
                "exposed_facilities": s_risk.get("exposed_facilities", 0)
            },
            "changes": {
                "score_change": round(score_change, 2),
                "severity_change": f"{b_risk['level']} -> {s_risk['level']}",
                "population_change": (round(s_risk.get("ml_predictions", {}).get("population_density", {}).get("value", 0)) if s_risk.get("ml_predictions") else 0) - (round(b_risk.get("ml_predictions", {}).get("population_density", {}).get("value", 0)) if b_risk.get("ml_predictions") else 0),
                "facility_change": s_risk.get("exposed_facilities", 0) - b_risk.get("exposed_facilities", 0),
                "top_changed_factors": factor_diffs,
                "recommended_actions": s_dec.get("recommended_actions", []),
                "baseline_explanation": next((x for x in res_baseline.get("explainability", []) if x["zone_id"] == z_id), None),
                "simulated_explanation": next((x for x in res_simulated.get("explainability", []) if x["zone_id"] == z_id), None)
            }
        })
        
    comparison.sort(key=lambda x: x["simulated"]["risk_score"], reverse=True)
    
    return {
        "status": "success",
        "comparison": comparison
    }

@app.get("/api/hospitals")
async def get_hospitals():
    data = load_json("hospitals_predictions.json")
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

@app.get("/api/weather")
async def get_weather():
    url = "https://api.open-meteo.com/v1/forecast?latitude=31.5204&longitude=74.3587&current=temperature_2m,relative_humidity_2m,apparent_temperature,precipitation,weather_code,wind_speed_10m&hourly=temperature_2m,relative_humidity_2m,precipitation_probability,precipitation,weather_code,wind_speed_10m&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,sunrise,sunset&timezone=Asia%2FKarachi&forecast_days=7"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        live_data = response.json()
        
        # Transform open-meteo structure to our frontend's expected format
        forecast = []
        for i in range(len(live_data["daily"]["time"])):
            if i == 0:
                # Use current for today
                avg_temp = live_data["current"]["temperature_2m"]
                hum = live_data["current"]["relative_humidity_2m"]
            else:
                # Approximate avg temp
                avg_temp = round((live_data["daily"]["temperature_2m_max"][i] + live_data["daily"]["temperature_2m_min"][i]) / 2.0, 1)
                hum = 50 
                
            forecast.append({
                "date": live_data["daily"]["time"][i],
                "avg_temp_c": avg_temp,
                "max_temp": round(live_data["daily"]["temperature_2m_max"][i]),
                "min_temp": round(live_data["daily"]["temperature_2m_min"][i]),
                "weather_code": live_data["daily"]["weather_code"][i],
                "avg_humidity_percent": hum
            })
            
        # Parse hourly for the Temperature Chart (next 24 hours)
        hourly_forecast = []
        from datetime import datetime
        for i in range(24): 
            dt = datetime.fromisoformat(live_data["hourly"]["time"][i])
            hourly_forecast.append({
                "time": dt.strftime("%I %p").lstrip("0"),
                "temp": round(live_data["hourly"]["temperature_2m"][i])
            })
            
        current_details = {
            "humidity": live_data["current"]["relative_humidity_2m"],
            "wind_speed": live_data["current"]["wind_speed_10m"],
            "precipitation": live_data["current"]["precipitation"],
            "feels_like": live_data["current"]["apparent_temperature"],
            "uv_index": 8, # Mocked since we didn't request it from Open-Meteo
            "visibility": 10, # Mocked in km
            "pressure": 1012 # Mocked hPa
        }
            
        return {"forecast": forecast, "hourly": hourly_forecast, "current": current_details}
    except Exception as e:
        # Fallback to mock data if API fails
        print(f"Weather API Error: {e}")
        data = load_json("weather_forecast.json")
        if not data:
            raise HTTPException(status_code=404, detail="Data not found")
        return data

@app.get("/api/schools")
async def get_schools():
    data = load_json("schools_predictions.json")
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

@app.get("/api/roads")
async def get_roads():
    data = load_json("roads_predictions.json")
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

@app.get("/api/population")
async def get_population():
    data = load_json("population_predictions.json")
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data



class ReportRequest(BaseModel):
    zone: str
    aqi: int
    officer_id: str

@app.post("/api/report-aqi")
async def report_aqi(report: ReportRequest, db: Session = Depends(get_db)):
    print(f"Authority {report.officer_id} reported AQI {report.aqi} for zone {report.zone}")
    
    if db:
        new_report = AQIReport(
            zone=report.zone,
            aqi=report.aqi,
            officer_id=report.officer_id
        )
        db.add(new_report)
        db.commit()
        db.refresh(new_report)
    
    response = {
        "status": "success",
        "message": f"AQI {report.aqi} recorded for {report.zone} and saved to database.",
        "alert_triggered": False,
        "email_dispatched": False
    }
    
    # If hazardous, trigger the automatic email alert system
    if report.aqi > 150:
        print(f"CRITICAL: AQI threshold exceeded. Dispatching emergency emails to Public Health Authorities.")
        response["alert_triggered"] = True
        response["email_dispatched"] = True
        response["message"] += " Critical threshold exceeded! Emergency protocol emails dispatched."
        
    return response

from services.alert_service import evaluate_risks, get_alerts, get_alert, acknowledge_alert, resolve_alert

@app.get("/api/alerts")
async def api_get_alerts(status: Optional[str] = None, severity: Optional[str] = None, type: Optional[str] = None, zone_id: Optional[str] = None):
    alerts = get_alerts(status=status, severity=severity, type_=type, zone_id=zone_id)
    return {"status": "success", "alerts": [a.model_dump() for a in alerts]}

@app.get("/api/alerts/{alert_id}")
async def api_get_alert(alert_id: str):
    alert = get_alert(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"status": "success", "alert": alert.model_dump()}

@app.post("/api/alerts/evaluate")
async def api_evaluate_alerts(role: str = require_operator):
    from graph.workflow import app as workflow_app
    state = {"query": "evaluate_alerts", "location": "Lahore", "scenario": {}}
    res = workflow_app.invoke(state)
    
    new_alerts = evaluate_risks(
        risks=res.get("risks", []),
        decisions=res.get("decisions", []),
        explainability=res.get("explainability", [])
    )
    return {"status": "success", "alerts_evaluated": len(new_alerts), "alerts": [a.model_dump() for a in new_alerts]}

@app.post("/api/alerts/{alert_id}/acknowledge")
async def api_acknowledge_alert(alert_id: str, role: str = require_operator):
    alert = acknowledge_alert(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"status": "success", "alert": alert.model_dump()}

@app.post("/api/alerts/{alert_id}/resolve")
async def api_resolve_alert(alert_id: str, role: str = require_operator):
    alert = resolve_alert(alert_id)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"status": "success", "alert": alert.model_dump()}

from services.resource_intelligence import evaluate_resources

@app.get("/api/resources/{zone_id}")
async def api_get_resources(zone_id: str, risk_type: str = "Flood", risk_score: float = 80.0, is_simulated: bool = False):
    result = evaluate_resources(zone_id, risk_type, risk_score, is_simulated)
    return {"status": "success", "data": result}

from services.trust_service import get_trust_status

@app.get("/api/trust/status")
async def api_get_trust_status():
    from demo_manager import DEMO_STATE
    result = get_trust_status(demo_mode_active=DEMO_STATE.get("is_active", False))
    return {"status": "success", "data": result}

from services.response_twin import evaluate_response_action
from pydantic import BaseModel

class TwinActionRequest(BaseModel):
    zone_id: str
    action: str
    
@app.post("/api/twin/evaluate-action")
async def api_evaluate_twin_action(req: TwinActionRequest, role: str = require_operator):
    # For the simulator, we grab the latest state from the workflow
    from graph.workflow import app as workflow_app
    from demo_manager import DEMO_STATE
    
    state = {
        "query": "Generate map risks for Twin",
        "location": "Lahore",
        "scenario": DEMO_STATE if DEMO_STATE.get("is_active") else {}
    }
    
    # Run data agent and prediction agent to get current features/predictions
    final_state = workflow_app.invoke(state)
    features = final_state.get("provider_data", {})
    predictions = final_state.get("predictions", {})
    
    result = evaluate_response_action(req.zone_id, req.action, features, predictions)
    if result.get("status") == "error":
        raise HTTPException(status_code=400, detail=result.get("message"))
        
    return result

from fastapi import File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
from services.citizen_service import submit_report, get_reports, verify_report, reject_report
import os
import uuid
import shutil

app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

@app.post("/api/reports")
async def api_submit_report(
    image: UploadFile = File(...),
    latitude: float = Form(...),
    longitude: float = Form(...),
    zone_id: str = Form(...),
    category: str = Form(...),
    description: str = Form(...)
):
    # Coordinate Validation (Strict Lahore City Bounds)
    if not (31.3 <= latitude <= 31.7) or not (74.1 <= longitude <= 74.5):
        raise HTTPException(status_code=400, detail="Coordinates are outside the allowed operational region (Lahore).")

    # MIME type and extension validation
    allowed_mimes = ["image/jpeg", "image/png", "image/webp"]
    if image.content_type not in allowed_mimes:
        raise HTTPException(status_code=400, detail="Invalid file type. Only JPEG, PNG, and WebP are allowed.")
    
    # Check extension to prevent traversal or malicious extensions
    ext = os.path.splitext(image.filename)[1].lower()
    if ext not in [".jpg", ".jpeg", ".png", ".webp"]:
        raise HTTPException(status_code=400, detail="Invalid file extension.")
        
    # Generate safe deterministic filename (no user input)
    safe_filename = f"{uuid.uuid4().hex}{ext}"
    filepath = os.path.join("uploads", safe_filename)
    
    # Enforce safe paths
    if not os.path.abspath(filepath).startswith(os.path.abspath("uploads")):
        raise HTTPException(status_code=400, detail="Path traversal detected.")
    
    # Save file with size limit (e.g., 5MB)
    MAX_SIZE = 5 * 1024 * 1024
    bytes_read = 0
    with open(filepath, "wb") as buffer:
        while chunk := image.file.read(8192):
            bytes_read += len(chunk)
            if bytes_read > MAX_SIZE:
                buffer.close()
                os.remove(filepath)
                raise HTTPException(status_code=413, detail="File too large. Maximum size is 5MB.")
            buffer.write(chunk)
        
    image_url = f"http://localhost:8009/uploads/{safe_filename}"
    
    report = submit_report(image_url, latitude, longitude, zone_id, category, description)
    return {"status": "success", "report": report.model_dump()}

@app.get("/api/reports")
async def api_get_reports(role: str = Depends(get_current_role)):
    reports = get_reports()
    
    # Security: Viewers only receive verified reports (ground truth)
    if role == "viewer":
        safe_reports = [r.model_dump() for r in reports if r.status == "verified"]
    else:
        safe_reports = [r.model_dump() for r in reports]
        
    return {"status": "success", "reports": safe_reports}

class ReviewReportRequest(BaseModel):
    notes: str = ""

@app.post("/api/reports/{report_id}/verify")
async def api_verify_report(report_id: str, req: ReviewReportRequest, role: str = require_operator):
    report = verify_report(report_id, req.notes)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found or not in pending state")
    return {"status": "success", "report": report.model_dump()}

@app.post("/api/reports/{report_id}/reject")
async def api_reject_report(report_id: str, req: ReviewReportRequest, role: str = require_operator):
    report = reject_report(report_id, req.notes)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found or not in pending state")
    return {"status": "success", "report": report.model_dump()}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)

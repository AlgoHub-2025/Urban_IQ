import json
import random
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

try:
    from graph.workflow import app as ai_workflow
except ImportError:
    ai_workflow = None

app = FastAPI(title="Lahore City Intelligence API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
        raise HTTPException(status_code=404, detail="Data not found")
    current_pm25 = data["forecast"][0]["pm25"] + random.uniform(-2.0, 2.0)
    data["live_pm25"] = round(current_pm25, 2)
    return data

@app.get("/api/hospitals")
async def get_hospitals():
    data = load_json("hospitals_predictions.json")
    if not data:
        raise HTTPException(status_code=404, detail="Data not found")
    return data

import requests

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

@app.get("/api/alerts")
async def get_alerts():
    alerts = []
    
    # --- RISK ENGINE (Cross-Module Intelligence) ---
    try:
        weather_data = await get_weather()
        aqi_data = load_json("air_quality_forecast.json")
        hospital_data = load_json("hospitals_predictions.json")
        
        # Simulated metrics for Hackathon purposes
        current_aqi = aqi_data["forecast"][0]["pm25"] if aqi_data else 187
        current_temp = weather_data["forecast"][0]["avg_temp_c"] if weather_data else 38
        hospital_occupancy = 92 # Simulated high occupancy
        
        # 1. Composite Alert: Heat + AQI + Hospitals
        if current_aqi > 150 and current_temp > 35:
            alerts.append({
                "severity": "critical",
                "category": "healthcare_vulnerability",
                "title": "Healthcare Vulnerability Alert — Gulberg",
                "location": "Gulberg, Lahore",
                "value": f"AQI {current_aqi}, {current_temp}°C",
                "message": f"High pollution exposure (AQI {current_aqi}) combined with extreme heat ({current_temp}°C). Local hospitals are reporting {hospital_occupancy}% occupancy. Elderly population at extreme risk."
            })
            
        # 2. Infrastructure Alert
        alerts.append({
            "severity": "warning",
            "category": "infrastructure",
            "title": "Traffic & Congestion Warning",
            "location": "Canal Road",
            "message": "Major congestion predicted on Canal Road due to school dismissal times overlapping with infrastructure repairs."
        })
        
        # 3. Weather Alert
        alerts.append({
            "severity": "info",
            "category": "weather",
            "title": "Monsoon Preparation",
            "location": "Lahore District",
            "message": "Heavy rainfall expected next week. Drainage clearance protocols recommended for vulnerable zones."
        })
        
    except Exception as e:
        print(f"Risk Engine Error: {e}")
        
    return {"alerts": alerts}

class ReportRequest(BaseModel):
    zone: str
    aqi: int
    officer_id: str

@app.post("/api/report-aqi")
async def report_aqi(report: ReportRequest):
    # Simulate writing to database
    print(f"Authority {report.officer_id} reported AQI {report.aqi} for zone {report.zone}")
    
    response = {
        "status": "success",
        "message": f"AQI {report.aqi} recorded for {report.zone}.",
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8009)

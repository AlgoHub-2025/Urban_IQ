from typing import List, Optional
from models.citizen_report import CitizenReport
from datetime import datetime
import os
import shutil

REPORTS_DB = {}

# No validated vision model is present in the repository.
# Strict requirement: Do NOT fake computer vision.
def get_vision_assessment(category: str, description: str) -> dict:
    return {
        "classification": "AI assessment unavailable — Human Review Required.", 
        "confidence": None, 
        "status": "pending"
    }

def submit_report(image_url: str, lat: float, lon: float, zone_id: str, category: str, description: str) -> CitizenReport:
    assessment = get_vision_assessment(category, description)
    
    report = CitizenReport(
        image_url=image_url,
        latitude=lat,
        longitude=lon,
        zone_id=zone_id,
        category=category,
        description=description,
        ai_classification=assessment["classification"],
        ai_confidence=assessment.get("confidence"),
        status=assessment["status"]
    )
    REPORTS_DB[report.id] = report
    return report

def get_reports() -> List[CitizenReport]:
    return sorted(list(REPORTS_DB.values()), key=lambda x: x.submitted_at, reverse=True)

def verify_report(report_id: str, notes: str = None) -> Optional[CitizenReport]:
    report = REPORTS_DB.get(report_id)
    if report and report.status in ["pending", "ai-assessed"]:
        report.status = "verified"
        report.reviewer_notes = notes
        report.verified_at = datetime.utcnow().isoformat() + "Z"
    return report

def reject_report(report_id: str, notes: str = None) -> Optional[CitizenReport]:
    report = REPORTS_DB.get(report_id)
    if report and report.status in ["pending", "ai-assessed"]:
        report.status = "rejected"
        report.reviewer_notes = notes
        report.verified_at = datetime.utcnow().isoformat() + "Z"
    return report

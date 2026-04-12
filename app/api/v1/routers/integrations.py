from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.models import UserRole

router = APIRouter(prefix="/api/v1/integrations", tags=["integrations"])


@router.post("/hospital/admission")
async def send_hospital_admission(
    patient_data: dict,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Send admission request to hospital system."""
    if current_user["role"] != UserRole.EXTERNAL:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    # Mock API call to hospital system
    response = {
        "success": True,
        "message": "Admission request sent to hospital",
        "patient_id": patient_data.get("patient_id"),
        "hospital_name": "Central Medical Hospital",
        "reference_number": f"ADM-{patient_data.get('patient_id')}-{int(__import__('time').time())}",
        "status": "pending"
    }
    
    return response


@router.post("/police/incident-report")
async def send_police_incident_report(
    incident_data: dict,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Send incident report to police department."""
    if current_user["role"] != UserRole.EXTERNAL:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    # Mock API call to police system
    response = {
        "success": True,
        "message": "Incident report sent to police department",
        "incident_type": incident_data.get("incident_type"),
        "police_unit": "Unit 42",
        "case_number": f"POL-{incident_data.get('incident_id')}-{int(__import__('time').time())}",
        "eta_minutes": 5
    }
    
    return response


@router.post("/fire-department/request")
async def send_fire_department_request(
    request_data: dict,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Send request to fire department."""
    if current_user["role"] != UserRole.EXTERNAL:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    # Mock API call to fire department system
    response = {
        "success": True,
        "message": "Request sent to fire department",
        "incident_type": request_data.get("incident_type"),
        "station": "Station 3",
        "request_id": f"FIRE-{request_data.get('incident_id')}-{int(__import__('time').time())}",
        "units_dispatched": 2,
        "estimated_arrival": "8 minutes"
    }
    
    return response


@router.get("/hospital/status/{case_id}")
async def get_hospital_status(
    case_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get status from hospital system."""
    # Mock API response
    response = {
        "case_id": case_id,
        "hospital_name": "Central Medical Hospital",
        "patient_status": "admitted",
        "bed_number": "ICU-5",
        "last_update": "2024-04-03T15:30:00Z"
    }
    
    return response


@router.get("/police/status/{case_number}")
async def get_police_status(
    case_number: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get status from police department system."""
    # Mock API response
    response = {
        "case_number": case_number,
        "police_unit": "Unit 42",
        "status": "responding",
        "current_location": "Main Street",
        "last_update": "2024-04-03T15:30:00Z"
    }
    
    return response


@router.get("/fire-department/status/{request_id}")
async def get_fire_status(
    request_id: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get status from fire department system."""
    # Mock API response
    response = {
        "request_id": request_id,
        "station": "Station 3",
        "status": "en_route",
        "units_count": 2,
        "last_update": "2024-04-03T15:30:00Z"
    }
    
    return response

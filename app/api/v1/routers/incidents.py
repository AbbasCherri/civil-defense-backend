from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.core.security import get_current_user
from app.schemas import IncidentCreate, IncidentUpdate, IncidentResponse, IncidentDetailResponse
from app.services import IncidentService, TeamService
from app.repositories import IncidentRepository, TeamAssignmentRepository, AuditLogRepository
from app.models import IncidentStatus, UserRole
from datetime import datetime

router = APIRouter(prefix="/api/v1/incidents", tags=["incidents"])


@router.post("/", response_model=IncidentResponse)
async def create_incident(
    incident: IncidentCreate,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Create a new incident (Citizen endpoint)."""
    if current_user["role"] != UserRole.CITIZEN and current_user["role"] != UserRole.DISPATCHER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    service = IncidentService(db)
    result = await service.create_incident(
        citizen_id=int(current_user["user_id"]),
        category=incident.category,
        priority=incident.priority,
        latitude=incident.latitude,
        longitude=incident.longitude,
        description=incident.description
    )
    
    return result


@router.get("/{incident_id}", response_model=IncidentDetailResponse)
async def get_incident(
    incident_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get incident details."""
    service = IncidentService(db)
    incident_repo = IncidentRepository(db)
    incident = await incident_repo.get_by_id(incident_id)
    
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    
    return incident


@router.get("/", response_model=List[IncidentResponse])
async def list_incidents(
    skip: int = 0,
    limit: int = 100,
    status_filter: str = None,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """List all incidents with optional status filter."""
    service = IncidentService(db)
    
    if status_filter:
        try:
            status_enum = IncidentStatus(status_filter)
            incidents = await service.incident_repo.get_by_status(status_enum)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid status")
    else:
        incidents = await service.incident_repo.get_all(skip, limit)
    
    return incidents


@router.patch("/{incident_id}/status", response_model=IncidentResponse)
async def update_incident_status(
    incident_id: int,
    status_update: dict,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Update incident status (Dispatcher/Admin only)."""
    if current_user["role"] not in [UserRole.DISPATCHER, UserRole.ADMIN]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    service = IncidentService(db)
    new_status = IncidentStatus(status_update.get("status"))
    result = await service.update_incident_status(incident_id, new_status, user_id=int(current_user["user_id"]))
    
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    
    return result


@router.post("/{incident_id}/assign-team")
async def assign_team_to_incident(
    incident_id: int,
    team_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Assign a team to an incident (Dispatcher only)."""
    if current_user["role"] != UserRole.DISPATCHER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    incident_repo = IncidentRepository(db)
    team_repo = TeamService(db)
    assignment_repo = TeamAssignmentRepository(db)
    
    incident = await incident_repo.get_by_id(incident_id)
    if not incident:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Incident not found")
    
    # Update incident status to Active
    await incident_repo.update_status(incident_id, IncidentStatus.ACTIVE)
    
    # Assign team
    await team_repo.assign_team_to_incident(team_id, incident_id, int(current_user["user_id"]))
    
    # Create team assignment record
    assignment = await assignment_repo.create(team_id, incident_id)
    await db.commit()
    
    return {"message": "Team assigned to incident", "assignment_id": assignment.id}


@router.get("/available-teams")
async def get_available_teams(
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get list of available teams (Dispatcher only)."""
    if current_user["role"] != UserRole.DISPATCHER:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    service = TeamService(db)
    teams = await service.get_available_teams()
    return {"available_teams": teams}


@router.get("/date-range", response_model=List[IncidentResponse])
async def get_incidents_by_date_range(
    start_date: str,
    end_date: str,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get incidents within a date range."""
    try:
        start = datetime.fromisoformat(start_date)
        end = datetime.fromisoformat(end_date)
    except ValueError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid date format")
    
    service = IncidentService(db)
    incidents = await service.get_incidents_by_date_range(start, end)
    return incidents

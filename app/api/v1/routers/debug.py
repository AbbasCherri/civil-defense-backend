"""
Debug router for testing and viewing all database tables.
⚠️ WARNING: This router has NO authentication. Use only for testing!
"""
from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.models import (
    User, Incident, Media, Resource, Team, TeamAssignment, Message, AuditLog
)
from app.schemas import (
    UserResponse, IncidentResponse, MediaResponse, ResourceResponse,
    TeamResponse, TeamAssignmentResponse, MessageResponse, AuditLogResponse
)

router = APIRouter(prefix="/api/v1/debug", tags=["debug - testing only"])


# ==================== USER TABLE ====================
@router.get("/users", response_model=List[UserResponse])
async def get_all_users(db: AsyncSession = Depends(get_db)):
    """Get all users. NO AUTHENTICATION - FOR TESTING ONLY."""
    result = await db.execute(select(User))
    users = result.scalars().all()
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific user by ID. NO AUTHENTICATION - FOR TESTING ONLY."""
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    return user


# ==================== INCIDENT TABLE ====================
@router.get("/incidents", response_model=List[IncidentResponse])
async def get_all_incidents(db: AsyncSession = Depends(get_db)):
    """Get all incidents. NO AUTHENTICATION - FOR TESTING ONLY."""
    result = await db.execute(select(Incident))
    incidents = result.scalars().all()
    return incidents


@router.get("/incidents/{incident_id}", response_model=IncidentResponse)
async def get_incident(incident_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific incident by ID. NO AUTHENTICATION - FOR TESTING ONLY."""
    result = await db.execute(select(Incident).where(Incident.id == incident_id))
    incident = result.scalars().first()
    return incident


# ==================== MEDIA TABLE ====================
@router.get("/media", response_model=List[MediaResponse])
async def get_all_media(db: AsyncSession = Depends(get_db)):
    """Get all media. NO AUTHENTICATION - FOR TESTING ONLY."""
    result = await db.execute(select(Media))
    media_list = result.scalars().all()
    return media_list


@router.get("/media/{media_id}", response_model=MediaResponse)
async def get_media(media_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific media by ID. NO AUTHENTICATION - FOR TESTING ONLY."""
    result = await db.execute(select(Media).where(Media.id == media_id))
    media = result.scalars().first()
    return media


# ==================== RESOURCE TABLE ====================
@router.get("/resources", response_model=List[ResourceResponse])
async def get_all_resources(db: AsyncSession = Depends(get_db)):
    """Get all resources. NO AUTHENTICATION - FOR TESTING ONLY."""
    result = await db.execute(select(Resource))
    resources = result.scalars().all()
    return resources


@router.get("/resources/{resource_id}", response_model=ResourceResponse)
async def get_resource(resource_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific resource by ID. NO AUTHENTICATION - FOR TESTING ONLY."""
    result = await db.execute(select(Resource).where(Resource.id == resource_id))
    resource = result.scalars().first()
    return resource


# ==================== TEAM TABLE ====================
@router.get("/teams", response_model=List[TeamResponse])
async def get_all_teams(db: AsyncSession = Depends(get_db)):
    """Get all teams. NO AUTHENTICATION - FOR TESTING ONLY."""
    result = await db.execute(select(Team))
    teams = result.scalars().all()
    return teams


@router.get("/teams/{team_id}", response_model=TeamResponse)
async def get_team(team_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific team by ID. NO AUTHENTICATION - FOR TESTING ONLY."""
    result = await db.execute(select(Team).where(Team.id == team_id))
    team = result.scalars().first()
    return team


# ==================== TEAM ASSIGNMENT TABLE ====================
@router.get("/team-assignments", response_model=List[TeamAssignmentResponse])
async def get_all_team_assignments(db: AsyncSession = Depends(get_db)):
    """Get all team assignments. NO AUTHENTICATION - FOR TESTING ONLY."""
    result = await db.execute(select(TeamAssignment))
    assignments = result.scalars().all()
    return assignments


@router.get("/team-assignments/{assignment_id}", response_model=TeamAssignmentResponse)
async def get_team_assignment(assignment_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific team assignment by ID. NO AUTHENTICATION - FOR TESTING ONLY."""
    result = await db.execute(select(TeamAssignment).where(TeamAssignment.id == assignment_id))
    assignment = result.scalars().first()
    return assignment


# ==================== MESSAGE TABLE ====================
@router.get("/messages", response_model=List[MessageResponse])
async def get_all_messages(db: AsyncSession = Depends(get_db)):
    """Get all messages. NO AUTHENTICATION - FOR TESTING ONLY."""
    result = await db.execute(select(Message))
    messages = result.scalars().all()
    return messages


@router.get("/messages/{message_id}", response_model=MessageResponse)
async def get_message(message_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific message by ID. NO AUTHENTICATION - FOR TESTING ONLY."""
    result = await db.execute(select(Message).where(Message.id == message_id))
    message = result.scalars().first()
    return message


# ==================== AUDIT LOG TABLE ====================
@router.get("/audit-logs", response_model=List[AuditLogResponse])
async def get_all_audit_logs(db: AsyncSession = Depends(get_db)):
    """Get all audit logs. NO AUTHENTICATION - FOR TESTING ONLY."""
    result = await db.execute(select(AuditLog))
    audit_logs = result.scalars().all()
    return audit_logs


@router.get("/audit-logs/{log_id}", response_model=AuditLogResponse)
async def get_audit_log(log_id: int, db: AsyncSession = Depends(get_db)):
    """Get a specific audit log by ID. NO AUTHENTICATION - FOR TESTING ONLY."""
    result = await db.execute(select(AuditLog).where(AuditLog.id == log_id))
    audit_log = result.scalars().first()
    return audit_log


# ==================== DATABASE STATS ====================
@router.get("/stats")
async def get_database_stats(db: AsyncSession = Depends(get_db)):
    """Get statistics about all tables. NO AUTHENTICATION - FOR TESTING ONLY."""
    users_count = await db.scalar(select(func.count()).select_from(User)) or 0
    incidents_count = await db.scalar(select(func.count()).select_from(Incident)) or 0
    media_count = await db.scalar(select(func.count()).select_from(Media)) or 0
    resources_count = await db.scalar(select(func.count()).select_from(Resource)) or 0
    teams_count = await db.scalar(select(func.count()).select_from(Team)) or 0
    assignments_count = await db.scalar(select(func.count()).select_from(TeamAssignment)) or 0
    messages_count = await db.scalar(select(func.count()).select_from(Message)) or 0
    audit_logs_count = await db.scalar(select(func.count()).select_from(AuditLog)) or 0
    
    return {
        "users": users_count,
        "incidents": incidents_count,
        "media": media_count,
        "resources": resources_count,
        "teams": teams_count,
        "team_assignments": assignments_count,
        "messages": messages_count,
        "audit_logs": audit_logs_count,
    }

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List
from datetime import datetime

from app.repositories import IncidentRepository, AuditLogRepository
from app.models import IncidentStatus, IncidentCategory, IncidentPriority


class IncidentService:
    def __init__(self, db: AsyncSession):
        self.incident_repo = IncidentRepository(db)
        self.audit_repo = AuditLogRepository(db)
        self.db = db
    
    async def create_incident(self, citizen_id: int, category: IncidentCategory, priority: IncidentPriority,
                             latitude: float, longitude: float, description: str) -> dict:
        incident = await self.incident_repo.create(citizen_id, category, priority, latitude, longitude, description)
        
        # Create audit log
        await self.audit_repo.create(
            user_id=citizen_id,
            action="INCIDENT_CREATED",
            target_entity="Incident",
            target_entity_id=incident.id,
            incident_id=incident.id
        )
        
        await self.db.commit()
        return {
            "id": incident.id,
            "citizen_id": incident.citizen_id,
            "category": incident.category,
            "priority": incident.priority,
            "status": incident.status,
            "latitude": incident.latitude,
            "longitude": incident.longitude,
            "description": incident.description,
            "created_at": incident.created_at
        }
    
    async def get_incident(self, incident_id: int) -> Optional[dict]:
        incident = await self.incident_repo.get_by_id(incident_id)
        if not incident:
            return None
        
        return {
            "id": incident.id,
            "citizen_id": incident.citizen_id,
            "category": incident.category,
            "priority": incident.priority,
            "status": incident.status,
            "latitude": incident.latitude,
            "longitude": incident.longitude,
            "description": incident.description,
            "created_at": incident.created_at,
            "closed_at": incident.closed_at
        }
    
    async def get_all_incidents(self, skip: int = 0, limit: int = 100) -> List[dict]:
        incidents = await self.incident_repo.get_all(skip, limit)
        return [
            {
                "id": i.id,
                "citizen_id": i.citizen_id,
                "category": i.category,
                "priority": i.priority,
                "status": i.status,
                "latitude": i.latitude,
                "longitude": i.longitude,
                "description": i.description,
                "created_at": i.created_at
            }
            for i in incidents
        ]
    
    async def update_incident_status(self, incident_id: int, status: IncidentStatus, user_id: int = None) -> Optional[dict]:
        incident = await self.incident_repo.update_status(incident_id, status)
        if not incident:
            return None
        
        # Create audit log
        if user_id:
            await self.audit_repo.create(
                user_id=user_id,
                action=f"INCIDENT_STATUS_CHANGED",
                target_entity="Incident",
                target_entity_id=incident.id,
                incident_id=incident.id,
                details=f"Status changed to {status.value}"
            )
        
        await self.db.commit()
        return {
            "id": incident.id,
            "status": incident.status,
            "closed_at": incident.closed_at
        }
    
    async def get_incidents_by_date_range(self, start_date: datetime, end_date: datetime) -> List[dict]:
        incidents = await self.incident_repo.get_by_date_range(start_date, end_date)
        return [
            {
                "id": i.id,
                "citizen_id": i.citizen_id,
                "category": i.category,
                "priority": i.priority,
                "status": i.status,
                "latitude": i.latitude,
                "longitude": i.longitude,
                "description": i.description,
                "created_at": i.created_at,
                "closed_at": i.closed_at
            }
            for i in incidents
        ]
    
    async def get_incidents_by_status(self, status: IncidentStatus) -> List[dict]:
        incidents = await self.incident_repo.get_by_status(status)
        return [
            {
                "id": i.id,
                "citizen_id": i.citizen_id,
                "category": i.category,
                "priority": i.priority,
                "status": i.status,
                "latitude": i.latitude,
                "longitude": i.longitude,
                "description": i.description,
                "created_at": i.created_at
            }
            for i in incidents
        ]

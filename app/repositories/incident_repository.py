from sqlalchemy import select, and_, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta
from typing import List, Optional

from app.models import Incident, IncidentStatus, IncidentCategory, IncidentPriority


class IncidentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, citizen_id: int, category: IncidentCategory, priority: IncidentPriority, 
                     latitude: float, longitude: float, description: str) -> Incident:
        incident = Incident(
            citizen_id=citizen_id,
            category=category,
            priority=priority,
            latitude=latitude,
            longitude=longitude,
            description=description,
            status=IncidentStatus.WAITING
        )
        self.db.add(incident)
        await self.db.flush()
        return incident
    
    async def get_by_id(self, incident_id: int) -> Optional[Incident]:
        result = await self.db.execute(
            select(Incident)
            .where(Incident.id == incident_id)
            .options(selectinload(Incident.citizen), selectinload(Incident.media), selectinload(Incident.messages))
        )
        return result.scalars().first()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Incident]:
        query = select(Incident).offset(skip).limit(limit).order_by(desc(Incident.created_at))
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_by_status(self, status: IncidentStatus) -> List[Incident]:
        query = select(Incident).where(Incident.status == status).order_by(desc(Incident.created_at))
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_by_citizen(self, citizen_id: int) -> List[Incident]:
        query = select(Incident).where(Incident.citizen_id == citizen_id).order_by(desc(Incident.created_at))
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_by_date_range(self, start_date: datetime, end_date: datetime) -> List[Incident]:
        query = select(Incident).where(
            and_(Incident.created_at >= start_date, Incident.created_at <= end_date)
        ).order_by(desc(Incident.created_at))
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update_status(self, incident_id: int, status: IncidentStatus) -> Optional[Incident]:
        incident = await self.get_by_id(incident_id)
        if incident:
            incident.status = status
            if status == IncidentStatus.CLOSED:
                incident.closed_at = datetime.utcnow()
            await self.db.flush()
        return incident
    
    async def update(self, incident_id: int, **kwargs) -> Optional[Incident]:
        incident = await self.get_by_id(incident_id)
        if incident:
            for key, value in kwargs.items():
                if hasattr(incident, key) and value is not None:
                    setattr(incident, key, value)
            await self.db.flush()
        return incident
    
    async def delete(self, incident_id: int) -> bool:
        incident = await self.get_by_id(incident_id)
        if incident:
            await self.db.delete(incident)
            return True
        return False

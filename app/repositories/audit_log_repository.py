from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.models import AuditLog


class AuditLogRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, user_id: int, action: str, target_entity: str, 
                     target_entity_id: int = None, incident_id: int = None, details: str = None) -> AuditLog:
        audit_log = AuditLog(
            user_id=user_id,
            action=action,
            target_entity=target_entity,
            target_entity_id=target_entity_id,
            incident_id=incident_id,
            details=details
        )
        self.db.add(audit_log)
        await self.db.flush()
        return audit_log
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[AuditLog]:
        query = select(AuditLog).offset(skip).limit(limit).order_by(desc(AuditLog.timestamp))
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_by_user(self, user_id: int) -> List[AuditLog]:
        query = select(AuditLog).where(AuditLog.user_id == user_id).order_by(desc(AuditLog.timestamp))
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_by_incident(self, incident_id: int) -> List[AuditLog]:
        query = select(AuditLog).where(AuditLog.incident_id == incident_id).order_by(desc(AuditLog.timestamp))
        result = await self.db.execute(query)
        return result.scalars().all()

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.models import TeamAssignment


class TeamAssignmentRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, team_id: int, incident_id: int) -> TeamAssignment:
        assignment = TeamAssignment(
            team_id=team_id,
            incident_id=incident_id
        )
        self.db.add(assignment)
        await self.db.flush()
        return assignment
    
    async def get_by_id(self, assignment_id: int) -> Optional[TeamAssignment]:
        result = await self.db.execute(select(TeamAssignment).where(TeamAssignment.id == assignment_id))
        return result.scalars().first()
    
    async def get_by_incident(self, incident_id: int) -> List[TeamAssignment]:
        query = select(TeamAssignment).where(TeamAssignment.incident_id == incident_id)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_by_team(self, team_id: int) -> List[TeamAssignment]:
        query = select(TeamAssignment).where(TeamAssignment.team_id == team_id)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def delete(self, assignment_id: int) -> bool:
        assignment = await self.get_by_id(assignment_id)
        if assignment:
            await self.db.delete(assignment)
            return True
        return False

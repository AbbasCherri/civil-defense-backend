from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.models import Team, TeamStatus, Resource, team_members


class TeamRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, vehicle_id: Optional[int] = None, status: TeamStatus = TeamStatus.AVAILABLE) -> Team:
        team = Team(
            vehicle_id=vehicle_id,
            status=status
        )
        self.db.add(team)
        await self.db.flush()
        return team
    
    async def get_by_id(self, team_id: int) -> Optional[Team]:
        result = await self.db.execute(
            select(Team)
            .where(Team.id == team_id)
            .options(selectinload(Team.members), selectinload(Team.vehicle))
        )
        return result.scalars().first()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Team]:
        query = select(Team).offset(skip).limit(limit).options(selectinload(Team.members), selectinload(Team.vehicle))
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_by_status(self, status: TeamStatus) -> List[Team]:
        query = select(Team).where(Team.status == status).options(selectinload(Team.members), selectinload(Team.vehicle))
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_available_teams(self) -> List[Team]:
        query = select(Team).where(Team.status == TeamStatus.AVAILABLE).options(selectinload(Team.members), selectinload(Team.vehicle))
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def add_member(self, team_id: int, user_id: int) -> Optional[Team]:
        team = await self.get_by_id(team_id)
        if team:
            from app.models import User
            user = await self.db.get(User, user_id)
            if user:
                team.members.append(user)
                await self.db.flush()
        return team
    
    async def remove_member(self, team_id: int, user_id: int) -> Optional[Team]:
        team = await self.get_by_id(team_id)
        if team:
            from app.models import User
            user = await self.db.get(User, user_id)
            if user and user in team.members:
                team.members.remove(user)
                await self.db.flush()
        return team
    
    async def update_status(self, team_id: int, status: TeamStatus) -> Optional[Team]:
        team = await self.get_by_id(team_id)
        if team:
            team.status = status
            await self.db.flush()
        return team
    
    async def update(self, team_id: int, **kwargs) -> Optional[Team]:
        team = await self.get_by_id(team_id)
        if team:
            for key, value in kwargs.items():
                if hasattr(team, key) and value is not None:
                    setattr(team, key, value)
            await self.db.flush()
        return team
    
    async def delete(self, team_id: int) -> bool:
        team = await self.get_by_id(team_id)
        if team:
            await self.db.delete(team)
            return True
        return False

from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from app.repositories import TeamRepository, AuditLogRepository
from app.models import TeamStatus


class TeamService:
    def __init__(self, db: AsyncSession):
        self.team_repo = TeamRepository(db)
        self.audit_repo = AuditLogRepository(db)
        self.db = db
    
    async def create_team(self, vehicle_id: Optional[int] = None, member_ids: List[int] = None) -> dict:
        team = await self.team_repo.create(vehicle_id=vehicle_id)
        
        if member_ids:
            for member_id in member_ids:
                await self.team_repo.add_member(team.id, member_id)
        
        await self.db.commit()
        return {
            "id": team.id,
            "vehicle_id": team.vehicle_id,
            "status": team.status,
            "members": [{"id": m.id, "name": m.name, "email": m.email} for m in team.members]
        }
    
    async def get_team(self, team_id: int) -> Optional[dict]:
        team = await self.team_repo.get_by_id(team_id)
        if not team:
            return None
        
        return {
            "id": team.id,
            "vehicle_id": team.vehicle_id,
            "status": team.status,
            "members": [{"id": m.id, "name": m.name, "email": m.email, "role": m.role} for m in team.members]
        }
    
    async def get_all_teams(self, skip: int = 0, limit: int = 100) -> List[dict]:
        teams = await self.team_repo.get_all(skip, limit)
        return [
            {
                "id": t.id,
                "vehicle_id": t.vehicle_id,
                "status": t.status,
                "members": [{"id": m.id, "name": m.name} for m in t.members]
            }
            for t in teams
        ]
    
    async def get_available_teams(self) -> List[dict]:
        teams = await self.team_repo.get_available_teams()
        return [
            {
                "id": t.id,
                "vehicle_id": t.vehicle_id,
                "status": t.status,
                "members": [{"id": m.id, "name": m.name, "email": m.email, "role": m.role} for m in t.members]
            }
            for t in teams
        ]
    
    async def assign_team_to_incident(self, team_id: int, incident_id: int, user_id: int) -> dict:
        team = await self.team_repo.update_status(team_id, TeamStatus.DEPLOYED)
        
        # Create audit log
        await self.audit_repo.create(
            user_id=user_id,
            action="TEAM_ASSIGNED",
            target_entity="Team",
            target_entity_id=team_id,
            incident_id=incident_id,
            details=f"Team {team_id} assigned to incident {incident_id}"
        )
        
        await self.db.commit()
        return {"id": team.id, "status": team.status}
    
    async def complete_team_assignment(self, team_id: int, user_id: int) -> dict:
        team = await self.team_repo.update_status(team_id, TeamStatus.AVAILABLE)
        
        # Create audit log
        await self.audit_repo.create(
            user_id=user_id,
            action="TEAM_AVAILABLE",
            target_entity="Team",
            target_entity_id=team_id,
            details=f"Team {team_id} returned to available status"
        )
        
        await self.db.commit()
        return {"id": team.id, "status": team.status}
    
    async def add_member_to_team(self, team_id: int, user_id: int) -> Optional[dict]:
        team = await self.team_repo.add_member(team_id, user_id)
        if not team:
            return None
        
        await self.db.commit()
        return {
            "id": team.id,
            "members": [{"id": m.id, "name": m.name} for m in team.members]
        }
    
    async def remove_member_from_team(self, team_id: int, user_id: int) -> Optional[dict]:
        team = await self.team_repo.remove_member(team_id, user_id)
        if not team:
            return None
        
        await self.db.commit()
        return {
            "id": team.id,
            "members": [{"id": m.id, "name": m.name} for m in team.members]
        }

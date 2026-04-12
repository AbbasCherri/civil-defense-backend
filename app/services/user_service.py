from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional, List

from app.repositories import UserRepository
from app.models import UserRole
from app.core.security import verify_password


class UserService:
    def __init__(self, db: AsyncSession):
        self.repo = UserRepository(db)
    
    async def register_user(self, name: str, email: str, password: str, role: UserRole = UserRole.CITIZEN) -> dict:
        existing_user = await self.repo.get_by_email(email)
        if existing_user:
            return {"error": "Email already registered"}
        
        user = await self.repo.create(name, email, password, role)
        await self.repo.db.commit()
        return {"id": user.id, "name": user.name, "email": user.email, "role": user.role, "contact_info": user.contact_info, "created_at": user.created_at}
    
    async def authenticate_user(self, email: str, password: str) -> Optional[dict]:
        user = await self.repo.get_by_email(email)
        if not user or not verify_password(password, user.password_hash):
            return None
        
        return {"id": user.id, "email": user.email, "name": user.name, "role": user.role}
    
    async def get_user(self, user_id: int) -> Optional[dict]:
        user = await self.repo.get_by_id(user_id)
        if not user:
            return None
        
        return {"id": user.id, "name": user.name, "email": user.email, "role": user.role, "contact_info": user.contact_info}
    
    async def get_all_users(self, skip: int = 0, limit: int = 100) -> List[dict]:
        users = await self.repo.get_all(skip, limit)
        return [{"id": u.id, "name": u.name, "email": u.email, "role": u.role} for u in users]
    
    async def update_user(self, user_id: int, **kwargs) -> Optional[dict]:
        user = await self.repo.update(user_id, **kwargs)
        if not user:
            return None
        
        await self.repo.db.commit()
        return {"id": user.id, "name": user.name, "email": user.email, "role": user.role}
    
    async def delete_user(self, user_id: int) -> bool:
        result = await self.repo.delete(user_id)
        if result:
            await self.repo.db.commit()
        return result
    
    async def get_users_by_role(self, role: UserRole) -> List[dict]:
        users = await self.repo.get_by_role(role)
        return [{"id": u.id, "name": u.name, "email": u.email, "role": u.role} for u in users]

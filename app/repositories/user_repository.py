from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from datetime import datetime, timedelta
from typing import List, Optional

from app.models import User, UserRole
from app.core.security import get_password_hash


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, name: str, email: str, password: str, role: UserRole = UserRole.CITIZEN, contact_info: Optional[str] = None) -> User:
        user = User(
            name=name,
            email=email,
            password_hash=get_password_hash(password),
            role=role,
            contact_info=contact_info
        )
        self.db.add(user)
        await self.db.flush()
        return user
    
    async def get_by_id(self, user_id: int) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.id == user_id))
        return result.scalars().first()
    
    async def get_by_email(self, email: str) -> Optional[User]:
        result = await self.db.execute(select(User).where(User.email == email))
        return result.scalars().first()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[User]:
        query = select(User).offset(skip).limit(limit)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_by_role(self, role: UserRole) -> List[User]:
        query = select(User).where(User.role == role)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update(self, user_id: int, **kwargs) -> Optional[User]:
        user = await self.get_by_id(user_id)
        if user:
            for key, value in kwargs.items():
                if hasattr(user, key) and value is not None:
                    setattr(user, key, value)
            await self.db.flush()
        return user
    
    async def delete(self, user_id: int) -> bool:
        user = await self.get_by_id(user_id)
        if user:
            await self.db.delete(user)
            return True
        return False

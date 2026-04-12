from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.models import Resource, ResourceStatus, ResourceType


class ResourceRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, name: str, type: ResourceType, status: ResourceStatus = ResourceStatus.AVAILABLE) -> Resource:
        resource = Resource(
            name=name,
            type=type,
            status=status
        )
        self.db.add(resource)
        await self.db.flush()
        return resource
    
    async def get_by_id(self, resource_id: int) -> Optional[Resource]:
        result = await self.db.execute(select(Resource).where(Resource.id == resource_id))
        return result.scalars().first()
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[Resource]:
        query = select(Resource).offset(skip).limit(limit).order_by(desc(Resource.created_at))
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_by_status(self, status: ResourceStatus) -> List[Resource]:
        query = select(Resource).where(Resource.status == status)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def get_by_type(self, type: ResourceType) -> List[Resource]:
        query = select(Resource).where(Resource.type == type)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def update(self, resource_id: int, **kwargs) -> Optional[Resource]:
        resource = await self.get_by_id(resource_id)
        if resource:
            for key, value in kwargs.items():
                if hasattr(resource, key) and value is not None:
                    setattr(resource, key, value)
            await self.db.flush()
        return resource
    
    async def update_status(self, resource_id: int, status: ResourceStatus) -> Optional[Resource]:
        resource = await self.get_by_id(resource_id)
        if resource:
            resource.status = status
            await self.db.flush()
        return resource
    
    async def delete(self, resource_id: int) -> bool:
        resource = await self.get_by_id(resource_id)
        if resource:
            await self.db.delete(resource)
            return True
        return False

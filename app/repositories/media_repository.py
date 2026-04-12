from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.models import Media, MediaType


class MediaRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, incident_id: int, file_path: str, file_type: MediaType) -> Media:
        media = Media(
            incident_id=incident_id,
            file_path=file_path,
            file_type=file_type
        )
        self.db.add(media)
        await self.db.flush()
        return media
    
    async def get_by_id(self, media_id: int) -> Optional[Media]:
        result = await self.db.execute(select(Media).where(Media.id == media_id))
        return result.scalars().first()
    
    async def get_by_incident(self, incident_id: int) -> List[Media]:
        query = select(Media).where(Media.incident_id == incident_id)
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def delete(self, media_id: int) -> bool:
        media = await self.get_by_id(media_id)
        if media:
            await self.db.delete(media)
            return True
        return False

from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional

from app.models import Message


class MessageRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def create(self, sender_id: int, incident_id: int, content: str) -> Message:
        message = Message(
            sender_id=sender_id,
            incident_id=incident_id,
            content=content
        )
        self.db.add(message)
        await self.db.flush()
        return message
    
    async def get_by_id(self, message_id: int) -> Optional[Message]:
        result = await self.db.execute(select(Message).where(Message.id == message_id))
        return result.scalars().first()
    
    async def get_by_incident(self, incident_id: int) -> List[Message]:
        query = select(Message).where(Message.incident_id == incident_id).order_by(desc(Message.timestamp))
        result = await self.db.execute(query)
        return result.scalars().all()
    
    async def delete(self, message_id: int) -> bool:
        message = await self.get_by_id(message_id)
        if message:
            await self.db.delete(message)
            return True
        return False

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Dict, Set
import json
from datetime import datetime

from app.core.database import get_db
from app.core.security import get_current_user
from app.repositories import MessageRepository
from app.models import UserRole

router = APIRouter(prefix="/api/v1/ws", tags=["websockets"])


class ConnectionManager:
    def __init__(self):
        # Track active connections: {incident_id: {user_id: websocket}}
        self.active_connections: Dict[int, Dict[int, WebSocket]] = {}
        # Track user locations: {incident_id: {user_id: {lat, lng, timestamp}}}
        self.user_locations: Dict[int, Dict[int, dict]] = {}
        # Track chat subscribers: {incident_id: set(user_ids)}
        self.chat_subscribers: Dict[int, Set[int]] = {}
    
    async def connect(self, incident_id: int, user_id: int, websocket: WebSocket):
        await websocket.accept()
        if incident_id not in self.active_connections:
            self.active_connections[incident_id] = {}
            self.user_locations[incident_id] = {}
            self.chat_subscribers[incident_id] = set()
        
        self.active_connections[incident_id][user_id] = websocket
        self.chat_subscribers[incident_id].add(user_id)
    
    def disconnect(self, incident_id: int, user_id: int):
        if incident_id in self.active_connections:
            self.active_connections[incident_id].pop(user_id, None)
            self.user_locations[incident_id].pop(user_id, None)
            self.chat_subscribers[incident_id].discard(user_id)
            
            if not self.active_connections[incident_id]:
                del self.active_connections[incident_id]
                del self.user_locations[incident_id]
                del self.chat_subscribers[incident_id]
    
    async def broadcast_location(self, incident_id: int, user_id: int, latitude: float, longitude: float):
        """Broadcast live location to all connected users for an incident."""
        if incident_id not in self.user_locations:
            return
        
        self.user_locations[incident_id][user_id] = {
            "user_id": user_id,
            "latitude": latitude,
            "longitude": longitude,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        message = {
            "type": "location_update",
            "data": self.user_locations[incident_id][user_id]
        }
        
        # Send to all connected users
        if incident_id in self.active_connections:
            for user_ws in self.active_connections[incident_id].values():
                try:
                    await user_ws.send_json(message)
                except Exception:
                    pass
    
    async def broadcast_chat(self, incident_id: int, user_id: int, user_name: str, message_text: str):
        """Broadcast chat message to all subscribers."""
        message = {
            "type": "chat_message",
            "data": {
                "user_id": user_id,
                "user_name": user_name,
                "message": message_text,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
        if incident_id in self.active_connections:
            for user_ws in self.active_connections[incident_id].values():
                try:
                    await user_ws.send_json(message)
                except Exception:
                    pass
    
    async def send_alert(self, incident_id: int, alert_message: str, alert_type: str = "info"):
        """Send alert to specific incident subscribers."""
        message = {
            "type": "alert",
            "data": {
                "message": alert_message,
                "alert_type": alert_type,
                "timestamp": datetime.utcnow().isoformat()
            }
        }
        
        if incident_id in self.active_connections:
            for user_ws in self.active_connections[incident_id].values():
                try:
                    await user_ws.send_json(message)
                except Exception:
                    pass
    
    async def get_locations(self, incident_id: int) -> Dict:
        """Get all current user locations for an incident."""
        if incident_id not in self.user_locations:
            return {}
        
        return {
            "type": "locations_snapshot",
            "data": list(self.user_locations[incident_id].values()),
            "timestamp": datetime.utcnow().isoformat()
        }


# Global connection manager
manager = ConnectionManager()


@router.websocket("/ws/live-map/{incident_id}")
async def websocket_live_map(websocket: WebSocket, incident_id: int, user_id: int = Query(...)):
    """WebSocket endpoint for live map updates and location tracking."""
    
    await manager.connect(incident_id, user_id, websocket)
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "location":
                await manager.broadcast_location(
                    incident_id,
                    user_id,
                    data.get("latitude"),
                    data.get("longitude")
                )
            elif data.get("type") == "get_snapshot":
                snapshot = await manager.get_locations(incident_id)
                await websocket.send_json(snapshot)
    
    except WebSocketDisconnect:
        manager.disconnect(incident_id, user_id)


@router.websocket("/ws/chat/{incident_id}")
async def websocket_chat(websocket: WebSocket, incident_id: int, user_id: int = Query(...), user_name: str = Query(...)):
    """WebSocket endpoint for real-time chat."""
    
    await manager.connect(incident_id, user_id, websocket)
    
    # Notify others that user joined
    await manager.broadcast_chat(
        incident_id,
        user_id,
        "System",
        f"{user_name} joined the chat"
    )
    
    try:
        while True:
            data = await websocket.receive_json()
            
            if data.get("type") == "message":
                await manager.broadcast_chat(
                    incident_id,
                    user_id,
                    user_name,
                    data.get("content")
                )
    
    except WebSocketDisconnect:
        manager.disconnect(incident_id, user_id)
        
        # Notify others that user left
        await manager.broadcast_chat(
            incident_id,
            user_id,
            "System",
            f"{user_name} left the chat"
        )


@router.post("/send-alert/{incident_id}")
async def send_alert_to_incident(
    incident_id: int,
    alert_data: dict,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Send alert to all connected users for an incident."""
    if current_user["role"] not in [UserRole.DISPATCHER, UserRole.ADMIN]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    message = alert_data.get("message", "")
    alert_type = alert_data.get("alert_type", "info")
    
    await manager.send_alert(incident_id, message, alert_type)
    
    return {"message": "Alert sent successfully"}


@router.get("/ws/locations/{incident_id}")
async def get_current_locations(
    incident_id: int,
    current_user: dict = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    """Get current locations for all responders on an incident (REST API)."""
    if incident_id not in manager.user_locations:
        return {"locations": []}
    
    return {
        "incident_id": incident_id,
        "locations": list(manager.user_locations[incident_id].values()),
        "timestamp": datetime.utcnow().isoformat()
    }

from __future__ import annotations
from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional, List
from datetime import datetime
from app.models import UserRole, IncidentStatus, IncidentCategory, IncidentPriority, MediaType, ResourceType, ResourceStatus, TeamStatus


# User Schemas
class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: UserRole = UserRole.CITIZEN
    contact_info: Optional[str] = None


class UserCreate(UserBase):
    password: str


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    name: Optional[str] = None
    contact_info: Optional[str] = None
    role: Optional[UserRole] = None


class UserResponse(UserBase):
    id: int
    created_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# Incident Schemas
class IncidentBase(BaseModel):
    category: IncidentCategory
    priority: IncidentPriority
    latitude: float
    longitude: float
    description: str


class IncidentCreate(IncidentBase):
    pass


class IncidentUpdate(BaseModel):
    status: Optional[IncidentStatus] = None
    priority: Optional[IncidentPriority] = None
    description: Optional[str] = None


class IncidentResponse(IncidentBase):
    id: int
    citizen_id: int
    status: IncidentStatus
    created_at: datetime
    closed_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


class IncidentDetailResponse(IncidentResponse):
    media: List['MediaResponse'] = []
    messages: List['MessageResponse'] = []
    citizen: Optional[UserResponse] = None
    
    model_config = ConfigDict(from_attributes=True)


# Media Schemas
class MediaBase(BaseModel):
    file_type: MediaType


class MediaCreate(MediaBase):
    file_path: str


class MediaResponse(MediaBase):
    id: int
    incident_id: int
    file_path: str
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Resource Schemas
class ResourceBase(BaseModel):
    name: str
    type: ResourceType
    status: ResourceStatus = ResourceStatus.AVAILABLE
    fuel_usage: Optional[float] = None


class ResourceCreate(ResourceBase):
    pass


class ResourceUpdate(BaseModel):
    name: Optional[str] = None
    status: Optional[ResourceStatus] = None
    fuel_usage: Optional[float] = None
    last_inspection: Optional[datetime] = None


class ResourceResponse(ResourceBase):
    id: int
    last_inspection: Optional[datetime] = None
    created_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Team Schemas
class TeamMemberResponse(BaseModel):
    id: int
    name: str
    email: str
    role: UserRole
    
    model_config = ConfigDict(from_attributes=True)


class TeamBase(BaseModel):
    vehicle_id: Optional[int] = None
    status: TeamStatus = TeamStatus.AVAILABLE


class TeamCreate(TeamBase):
    member_ids: List[int] = []


class TeamUpdate(BaseModel):
    status: Optional[TeamStatus] = None
    vehicle_id: Optional[int] = None


class TeamResponse(TeamBase):
    id: int
    created_at: datetime
    members: List[TeamMemberResponse] = []
    vehicle: Optional[ResourceResponse] = None
    
    model_config = ConfigDict(from_attributes=True)


# Team Assignment Schemas
class TeamAssignmentBase(BaseModel):
    team_id: int
    incident_id: int


class TeamAssignmentCreate(TeamAssignmentBase):
    pass


class TeamAssignmentResponse(TeamAssignmentBase):
    id: int
    assigned_at: datetime
    completed_at: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)


# Message Schemas
class MessageBase(BaseModel):
    content: str


class MessageCreate(MessageBase):
    incident_id: int


class MessageResponse(BaseModel):
    id: int
    sender_id: int
    incident_id: int
    content: str
    timestamp: datetime
    sender: Optional[UserResponse] = None
    
    model_config = ConfigDict(from_attributes=True)


# Audit Log Schemas
class AuditLogResponse(BaseModel):
    id: int
    user_id: int
    action: str
    target_entity: str
    target_entity_id: Optional[int] = None
    incident_id: Optional[int] = None
    details: Optional[str] = None
    timestamp: datetime
    
    model_config = ConfigDict(from_attributes=True)


# Auth Response
class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None
    role: Optional[UserRole] = None


# Shared Response
class GenericResponse(BaseModel):
    detail: str


# Rebuild models with forward references to resolve circular dependencies
IncidentDetailResponse.model_rebuild()
TeamResponse.model_rebuild()
MessageResponse.model_rebuild()

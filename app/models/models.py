from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey, Text, Enum, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from datetime import datetime
import enum

from app.core.database import Base


class UserRole(str, enum.Enum):
    CITIZEN = "Citizen"
    DISPATCHER = "Dispatcher"
    RESPONDER = "Responder"
    ADMIN = "Admin"
    EXTERNAL = "External"


class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    email = Column(String(255), unique=True, index=True)
    password_hash = Column(String(255))
    role = Column(Enum(UserRole, values_callable=lambda x: [e.value for e in x]), default=UserRole.CITIZEN)
    contact_info = Column(String(255), nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    incidents = relationship("Incident", back_populates="citizen")
    messages_sent = relationship("Message", back_populates="sender", foreign_keys="Message.sender_id")
    audit_logs = relationship("AuditLog", back_populates="user")
    team_members = relationship("Team", back_populates="members", secondary="team_members")


class IncidentStatus(str, enum.Enum):
    WAITING = "Waiting"
    ACTIVE = "Active"
    CLOSED = "Closed"


class IncidentCategory(str, enum.Enum):
    FIRE = "Fire"
    MEDICAL = "Medical"
    TRAFFIC = "Traffic"
    ACCIDENT = "Accident"
    FLOOD = "Flood"
    OTHER = "Other"


class IncidentPriority(str, enum.Enum):
    LOW = "Low"
    MEDIUM = "Medium"
    HIGH = "High"
    CRITICAL = "Critical"


class Incident(Base):
    __tablename__ = "incidents"
    
    id = Column(Integer, primary_key=True, index=True)
    citizen_id = Column(Integer, ForeignKey("users.id"), index=True)
    category = Column(Enum(IncidentCategory, values_callable=lambda x: [e.value for e in x]), index=True)
    priority = Column(Enum(IncidentPriority, values_callable=lambda x: [e.value for e in x]), default=IncidentPriority.MEDIUM)
    status = Column(Enum(IncidentStatus, values_callable=lambda x: [e.value for e in x]), default=IncidentStatus.WAITING, index=True)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, server_default=func.now(), index=True)
    closed_at = Column(DateTime, nullable=True)
    
    # Relationships
    citizen = relationship("User", back_populates="incidents")
    media = relationship("Media", back_populates="incident", cascade="all, delete-orphan")
    messages = relationship("Message", back_populates="incident", cascade="all, delete-orphan")
    team_assignments = relationship("TeamAssignment", back_populates="incident", cascade="all, delete-orphan")
    audit_logs = relationship("AuditLog", back_populates="incident")


class MediaType(str, enum.Enum):
    IMAGE = "image"
    VIDEO = "video"
    VOICE = "voice"
    DOCUMENT = "document"


class Media(Base):
    __tablename__ = "media"
    
    id = Column(Integer, primary_key=True, index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), index=True)
    file_path = Column(String(500))
    file_type = Column(Enum(MediaType, values_callable=lambda x: [e.value for e in x]))
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    incident = relationship("Incident", back_populates="media")


class ResourceType(str, enum.Enum):
    VEHICLE = "Vehicle"
    EQUIPMENT = "Equipment"


class ResourceStatus(str, enum.Enum):
    AVAILABLE = "Available"
    UNAVAILABLE = "Unavailable"
    MAINTENANCE = "Maintenance"


class Resource(Base):
    __tablename__ = "resources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True)
    type = Column(Enum(ResourceType, values_callable=lambda x: [e.value for e in x]))
    status = Column(Enum(ResourceStatus, values_callable=lambda x: [e.value for e in x]), default=ResourceStatus.AVAILABLE, index=True)
    fuel_usage = Column(Float, nullable=True)
    last_inspection = Column(DateTime, nullable=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    teams = relationship("Team", back_populates="vehicle")


class TeamStatus(str, enum.Enum):
    AVAILABLE = "Available"
    DEPLOYED = "Deployed"


class Team(Base):
    __tablename__ = "teams"
    
    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("resources.id"), nullable=True)
    status = Column(Enum(TeamStatus, values_callable=lambda x: [e.value for e in x]), default=TeamStatus.AVAILABLE, index=True)
    created_at = Column(DateTime, server_default=func.now())
    
    # Relationships
    vehicle = relationship("Resource", back_populates="teams")
    members = relationship("User", secondary="team_members", back_populates="team_members")
    assignments = relationship("TeamAssignment", back_populates="team")


# Association table for team members
from sqlalchemy import Table
team_members = Table(
    "team_members",
    Base.metadata,
    Column("team_id", Integer, ForeignKey("teams.id"), primary_key=True),
    Column("user_id", Integer, ForeignKey("users.id"), primary_key=True)
)


class TeamAssignment(Base):
    __tablename__ = "team_assignments"
    
    id = Column(Integer, primary_key=True, index=True)
    team_id = Column(Integer, ForeignKey("teams.id"), index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), index=True)
    assigned_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    team = relationship("Team", back_populates="assignments")
    incident = relationship("Incident", back_populates="team_assignments")


class Message(Base):
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id"), index=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), index=True)
    content = Column(Text)
    timestamp = Column(DateTime, server_default=func.now(), index=True)
    
    # Relationships
    sender = relationship("User", back_populates="messages_sent", foreign_keys=[sender_id])
    incident = relationship("Incident", back_populates="messages")


class AuditLog(Base):
    __tablename__ = "audit_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), index=True)
    action = Column(String(255), index=True)
    target_entity = Column(String(255))  # Entity type (e.g., "Incident", "Team")
    target_entity_id = Column(Integer, nullable=True)
    incident_id = Column(Integer, ForeignKey("incidents.id"), nullable=True, index=True)
    details = Column(Text, nullable=True)
    timestamp = Column(DateTime, server_default=func.now(), index=True)
    
    # Relationships
    user = relationship("User", back_populates="audit_logs")
    incident = relationship("Incident", back_populates="audit_logs")

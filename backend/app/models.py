import uuid
from datetime import datetime, date
from sqlalchemy import Column, String, Text, Date, Boolean, DateTime, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.database import Base
import enum

class UserRole(str, enum.Enum):
    admin = "admin"
    crew = "crew"

class TaskStatus(str, enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    completed = "completed"

class DrillStatus(str, enum.Enum):
    scheduled = "scheduled"
    completed = "completed"
    missed = "missed"

class Ship(Base):
    __tablename__ = "ships"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    users = relationship("User", back_populates="ship")
    maintenance_tasks = relationship("MaintenanceTask", back_populates="ship")
    safety_drills = relationship("SafetyDrill", back_populates="ship")

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), nullable=False)
    ship_id = Column(UUID(as_uuid=True), ForeignKey("ships.id"), nullable=True)
    name = Column(String(100), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    ship = relationship("Ship", back_populates="users")
    assigned_tasks = relationship("MaintenanceTask", back_populates="assigned_user", foreign_keys="MaintenanceTask.assigned_to")
    comments = relationship("TaskComment", back_populates="user")
    drill_attendance = relationship("DrillAttendance", back_populates="user")

class MaintenanceTask(Base):
    __tablename__ = "maintenance_tasks"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus), default=TaskStatus.pending, nullable=False)
    due_date = Column(Date, nullable=False)
    ship_id = Column(UUID(as_uuid=True), ForeignKey("ships.id"), nullable=False)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    ship = relationship("Ship", back_populates="maintenance_tasks")
    assigned_user = relationship("User", back_populates="assigned_tasks", foreign_keys=[assigned_to])
    comments = relationship("TaskComment", back_populates="task")

class TaskComment(Base):
    __tablename__ = "task_comments"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    task_id = Column(UUID(as_uuid=True), ForeignKey("maintenance_tasks.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    task = relationship("MaintenanceTask", back_populates="comments")
    user = relationship("User", back_populates="comments")

class SafetyDrill(Base):
    __tablename__ = "safety_drills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    drill_type = Column(String(50), nullable=False)
    description = Column(Text, nullable=True)
    scheduled_date = Column(Date, nullable=False)
    status = Column(Enum(DrillStatus), default=DrillStatus.scheduled, nullable=False)
    ship_id = Column(UUID(as_uuid=True), ForeignKey("ships.id"), nullable=False)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    ship = relationship("Ship", back_populates="safety_drills")
    attendance = relationship("DrillAttendance", back_populates="drill")

class DrillAttendance(Base):
    __tablename__ = "drill_attendance"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    drill_id = Column(UUID(as_uuid=True), ForeignKey("safety_drills.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    attended = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    drill = relationship("SafetyDrill", back_populates="attendance")
    user = relationship("User", back_populates="drill_attendance")

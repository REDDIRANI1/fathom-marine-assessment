from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import date, datetime
from uuid import UUID
from app.models import UserRole, TaskStatus, DrillStatus

class ShipCreate(BaseModel):
    name: str

class ShipOut(BaseModel):
    id: UUID
    name: str

    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    name: str
    role: UserRole
    ship_id: Optional[UUID] = None

class UserOut(BaseModel):
    id: UUID
    email: str
    name: str
    role: UserRole
    ship_id: Optional[UUID] = None

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut

class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: date
    ship_id: UUID
    assigned_to: Optional[UUID] = None

class TaskStatusUpdate(BaseModel):
    status: TaskStatus

class TaskOut(BaseModel):
    id: UUID
    title: str
    description: Optional[str] = None
    status: TaskStatus
    due_date: date
    ship_id: UUID
    assigned_to: Optional[UUID] = None
    created_by: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class CommentCreate(BaseModel):
    content: str

class CommentOut(BaseModel):
    id: UUID
    task_id: UUID
    user_id: UUID
    content: str
    created_at: datetime

    class Config:
        from_attributes = True

class DrillCreate(BaseModel):
    drill_type: str
    description: Optional[str] = None
    scheduled_date: date
    ship_id: UUID

class DrillOut(BaseModel):
    id: UUID
    drill_type: str
    description: Optional[str] = None
    scheduled_date: date
    status: DrillStatus
    ship_id: UUID
    created_by: UUID
    created_at: datetime

    class Config:
        from_attributes = True

class AttendanceCreate(BaseModel):
    user_id: UUID
    attended: bool

class AttendanceOut(BaseModel):
    id: UUID
    drill_id: UUID
    user_id: UUID
    attended: bool
    created_at: datetime

    class Config:
        from_attributes = True

class ComplianceStats(BaseModel):
    maintenance_pct: float
    drill_pct: float
    overall_pct: float
    overdue_tasks: int
    missed_drills: int

class ShipCompliance(ComplianceStats):
    ship_id: UUID
    ship_name: str

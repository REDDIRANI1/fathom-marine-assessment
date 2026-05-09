from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session, joinedload
from typing import List, Optional
from uuid import UUID
from app.database import get_db
from app.models import MaintenanceTask, TaskComment, User
from app.schemas import TaskCreate, TaskStatusUpdate, TaskOut, CommentCreate, CommentOut
from app.auth import get_current_user, require_admin

router = APIRouter(prefix="/tasks", tags=["tasks"])


def attach_ship_name(task: MaintenanceTask) -> MaintenanceTask:
    task.ship_name = task.ship.name if task.ship else None
    return task

@router.get("", response_model=List[TaskOut])
def list_tasks(
    ship_id: Optional[UUID] = Query(None),
    status: Optional[str] = Query(None),
    assigned_to: Optional[UUID] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(MaintenanceTask).options(joinedload(MaintenanceTask.ship))

    if current_user.role.value == "crew":
        query = query.filter(MaintenanceTask.assigned_to == current_user.id)

    if ship_id:
        query = query.filter(MaintenanceTask.ship_id == ship_id)
    if status:
        query = query.filter(MaintenanceTask.status == status)
    if assigned_to and current_user.role.value == "admin":
        query = query.filter(MaintenanceTask.assigned_to == assigned_to)

    tasks = query.order_by(MaintenanceTask.due_date.asc()).all()
    return [attach_ship_name(task) for task in tasks]

@router.post("", response_model=TaskOut, status_code=201)
def create_task(data: TaskCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    if data.assigned_to is not None:
        assigned_user = db.query(User).filter(User.id == data.assigned_to).first()
        if assigned_user is None:
            raise HTTPException(status_code=404, detail="Assigned crew member was not found")
        if assigned_user.role.value != "crew":
            raise HTTPException(status_code=422, detail="Tasks can only be assigned to crew members")
        if assigned_user.ship_id != data.ship_id:
            raise HTTPException(status_code=422, detail="Assigned crew member must belong to the selected ship")

    task = MaintenanceTask(
        title=data.title,
        description=data.description,
        due_date=data.due_date,
        ship_id=data.ship_id,
        assigned_to=data.assigned_to,
        created_by=current_user.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return attach_ship_name(task)

@router.patch("/{task_id}/status", response_model=TaskOut)
def update_task_status(task_id: UUID, data: TaskStatusUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(MaintenanceTask).options(joinedload(MaintenanceTask.ship)).filter(MaintenanceTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if current_user.role.value == "crew" and task.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not assigned to this task")

    task.status = data.status
    db.commit()
    db.refresh(task)
    return attach_ship_name(task)

@router.post("/{task_id}/comments", response_model=CommentOut, status_code=201)
def add_comment(task_id: UUID, data: CommentCreate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(MaintenanceTask).filter(MaintenanceTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if current_user.role.value == "crew" and task.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not assigned to this task")

    comment = TaskComment(task_id=task_id, user_id=current_user.id, content=data.content)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment

@router.get("/{task_id}/comments", response_model=List[CommentOut])
def list_comments(task_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(MaintenanceTask).filter(MaintenanceTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    if current_user.role.value == "crew" and task.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not assigned to this task")
    return db.query(TaskComment).filter(TaskComment.task_id == task_id).order_by(TaskComment.created_at.asc()).all()

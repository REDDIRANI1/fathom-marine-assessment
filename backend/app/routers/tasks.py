from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.database import get_db
from app.models import MaintenanceTask, TaskComment, User
from app.schemas import TaskCreate, TaskStatusUpdate, TaskOut, CommentCreate, CommentOut
from app.auth import get_current_user, require_admin

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("", response_model=List[TaskOut])
def list_tasks(
    ship_id: Optional[UUID] = Query(None),
    status: Optional[str] = Query(None),
    assigned_to: Optional[UUID] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(MaintenanceTask)

    if current_user.role.value == "crew":
        query = query.filter(MaintenanceTask.assigned_to == current_user.id)

    if ship_id:
        query = query.filter(MaintenanceTask.ship_id == ship_id)
    if status:
        query = query.filter(MaintenanceTask.status == status)
    if assigned_to and current_user.role.value == "admin":
        query = query.filter(MaintenanceTask.assigned_to == assigned_to)

    return query.order_by(MaintenanceTask.due_date.asc()).all()

@router.post("", response_model=TaskOut, status_code=201)
def create_task(data: TaskCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    task = MaintenanceTask(
        title=data.title,
        description=data.description,
        due_date=data.due_date,
        ship_id=data.ship_id,
        assigned_to=data.assigned_to,
        created_by=_.id,
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.patch("/{task_id}/status", response_model=TaskOut)
def update_task_status(task_id: UUID, data: TaskStatusUpdate, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    task = db.query(MaintenanceTask).filter(MaintenanceTask.id == task_id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if current_user.role.value == "crew" and task.assigned_to != current_user.id:
        raise HTTPException(status_code=403, detail="Not assigned to this task")

    task.status = data.status
    db.commit()
    db.refresh(task)
    return task

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
    return db.query(TaskComment).filter(TaskComment.task_id == task_id).order_by(TaskComment.created_at.asc()).all()

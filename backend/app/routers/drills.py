from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.database import get_db
from app.models import SafetyDrill, DrillAttendance, User
from app.schemas import DrillCreate, DrillOut, AttendanceCreate, AttendanceOut
from app.auth import get_current_user, require_admin

router = APIRouter(prefix="/drills", tags=["drills"])

@router.get("", response_model=List[DrillOut])
def list_drills(
    ship_id: Optional[UUID] = Query(None),
    status: Optional[str] = Query(None),
    drill_type: Optional[str] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    query = db.query(SafetyDrill)

    if current_user.role.value == "crew":
        if current_user.ship_id:
            query = query.filter(SafetyDrill.ship_id == current_user.ship_id)
        else:
            return []

    if ship_id and current_user.role.value == "admin":
        query = query.filter(SafetyDrill.ship_id == ship_id)
    if status:
        query = query.filter(SafetyDrill.status == status)
    if drill_type:
        query = query.filter(SafetyDrill.drill_type == drill_type)

    return query.order_by(SafetyDrill.scheduled_date.asc()).all()

@router.post("", response_model=DrillOut, status_code=201)
def create_drill(data: DrillCreate, db: Session = Depends(get_db), current_user: User = Depends(require_admin)):
    drill = SafetyDrill(
        drill_type=data.drill_type,
        description=data.description,
        scheduled_date=data.scheduled_date,
        ship_id=data.ship_id,
        created_by=current_user.id,
    )
    db.add(drill)
    db.commit()
    db.refresh(drill)
    return drill

@router.post("/{drill_id}/attendance", response_model=List[AttendanceOut], status_code=201)
def mark_attendance(drill_id: UUID, data: List[AttendanceCreate], db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    drill = db.query(SafetyDrill).filter(SafetyDrill.id == drill_id).first()
    if not drill:
        raise HTTPException(status_code=404, detail="Drill not found")
    if current_user.role.value == "crew" and current_user.ship_id != drill.ship_id:
        raise HTTPException(status_code=403, detail="Not authorized for this ship's drills")
    if current_user.role.value == "crew":
        crew_entry = next((e for e in data if e.user_id == current_user.id), None)
        filtered = [crew_entry] if crew_entry else []
    else:
        filtered = data

    records = []
    for entry in filtered:
        existing = db.query(DrillAttendance).filter(
            DrillAttendance.drill_id == drill_id,
            DrillAttendance.user_id == entry.user_id,
        ).first()
        if existing:
            existing.attended = entry.attended
            records.append(existing)
        else:
            record = DrillAttendance(drill_id=drill_id, user_id=entry.user_id, attended=entry.attended)
            db.add(record)
            records.append(record)

    db.commit()
    for r in records:
        db.refresh(r)
    return records

@router.get("/{drill_id}/attendance", response_model=List[AttendanceOut])
def get_attendance(drill_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    drill = db.query(SafetyDrill).filter(SafetyDrill.id == drill_id).first()
    if not drill:
        raise HTTPException(status_code=404, detail="Drill not found")
    if current_user.role.value == "crew" and current_user.ship_id != drill.ship_id:
        raise HTTPException(status_code=403, detail="Not authorized for this ship's drills")
    return db.query(DrillAttendance).filter(DrillAttendance.drill_id == drill_id).all()

@router.patch("/{drill_id}/complete", response_model=DrillOut)
def complete_drill(drill_id: UUID, db: Session = Depends(get_db), current_user: User = Depends(get_current_user)):
    drill = db.query(SafetyDrill).filter(SafetyDrill.id == drill_id).first()
    if not drill:
        raise HTTPException(status_code=404, detail="Drill not found")
    if current_user.role.value == "crew" and current_user.ship_id != drill.ship_id:
        raise HTTPException(status_code=403, detail="Not authorized for this ship's drills")
    drill.status = "completed"
    db.commit()
    db.refresh(drill)
    return drill

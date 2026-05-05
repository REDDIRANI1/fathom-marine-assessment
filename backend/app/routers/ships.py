from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models import Ship, User
from app.schemas import ShipCreate, ShipOut
from app.auth import get_current_user, require_admin

router = APIRouter(prefix="/ships", tags=["ships"])

@router.get("", response_model=List[ShipOut])
def list_ships(current_user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    if current_user.role.value == "admin":
        return db.query(Ship).all()
    if current_user.ship_id:
        return db.query(Ship).filter(Ship.id == current_user.ship_id).all()
    return []

@router.post("", response_model=ShipOut, status_code=201)
def create_ship(data: ShipCreate, db: Session = Depends(get_db), _: User = Depends(require_admin)):
    if db.query(Ship).filter(Ship.name == data.name).first():
        raise HTTPException(status_code=409, detail="Ship already exists")
    ship = Ship(name=data.name)
    db.add(ship)
    db.commit()
    db.refresh(ship)
    return ship

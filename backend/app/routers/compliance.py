from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from uuid import UUID
from app.database import get_db
from app.models import User, Ship
from app.schemas import ComplianceStats, ShipCompliance
from app.auth import get_current_user, require_admin
from app.services.compliance import get_compliance_stats

router = APIRouter(prefix="/compliance", tags=["compliance"])

@router.get("", response_model=ComplianceStats)
def compliance_overview(
    ship_id: Optional[UUID] = Query(None),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.role.value == "crew" and current_user.ship_id:
        ship_id = current_user.ship_id
    return get_compliance_stats(db, str(ship_id) if ship_id else None)

@router.get("/ships", response_model=List[ShipCompliance])
def compliance_by_ship(db: Session = Depends(get_db), _: User = Depends(require_admin)):
    ships = db.query(Ship).all()
    results = []
    for ship in ships:
        stats = get_compliance_stats(db, str(ship.id))
        results.append(ShipCompliance(ship_id=ship.id, ship_name=ship.name, **stats))
    return results

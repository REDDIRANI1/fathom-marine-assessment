from datetime import date
from sqlalchemy.orm import Session
from app.models import MaintenanceTask, SafetyDrill, DrillStatus, TaskStatus

def get_compliance_stats(db: Session, ship_id: str = None) -> dict:
    tasks_query = db.query(MaintenanceTask)
    drills_query = db.query(SafetyDrill)

    if ship_id:
        tasks_query = tasks_query.filter(MaintenanceTask.ship_id == ship_id)
        drills_query = drills_query.filter(SafetyDrill.ship_id == ship_id)

    total_tasks = tasks_query.count()
    completed_tasks = tasks_query.filter(MaintenanceTask.status == TaskStatus.completed).count()
    maintenance_pct = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 100.0

    total_drills = drills_query.count()
    completed_drills = drills_query.filter(SafetyDrill.status == DrillStatus.completed).count()
    drill_pct = (completed_drills / total_drills * 100) if total_drills > 0 else 100.0

    overall_pct = round((maintenance_pct + drill_pct) / 2, 1)
    maintenance_pct = round(maintenance_pct, 1)
    drill_pct = round(drill_pct, 1)

    today = date.today()
    overdue_tasks = tasks_query.filter(
        MaintenanceTask.due_date < today,
        MaintenanceTask.status != TaskStatus.completed,
    ).count()

    missed_drills = drills_query.filter(
        SafetyDrill.scheduled_date < today,
        SafetyDrill.status != DrillStatus.completed,
    ).count()

    return {
        "maintenance_pct": maintenance_pct,
        "drill_pct": drill_pct,
        "overall_pct": overall_pct,
        "overdue_tasks": overdue_tasks,
        "missed_drills": missed_drills,
    }

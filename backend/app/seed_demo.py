from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta

from app.auth import hash_password
from app.database import Base, SessionLocal, engine
from app.models import (
    DrillAttendance,
    DrillStatus,
    MaintenanceTask,
    SafetyDrill,
    Ship,
    TaskComment,
    TaskStatus,
    User,
    UserRole,
)


@dataclass(frozen=True)
class DemoUser:
    email: str
    password: str
    name: str
    role: UserRole
    ship_name: str | None = None


@dataclass(frozen=True)
class DemoTask:
    title: str
    ship_name: str
    assigned_email: str
    status: TaskStatus
    due_offset_days: int
    description: str
    comments: tuple[tuple[str, str], ...] = ()


@dataclass(frozen=True)
class DemoDrill:
    drill_type: str
    ship_name: str
    status: DrillStatus
    scheduled_offset_days: int
    description: str
    attendance: tuple[tuple[str, bool], ...] = ()


DEMO_SHIPS = (
    "MV Horizon",
    "SS Pacific",
    "MT Atlas",
)

DEMO_USERS = (
    DemoUser("admin@fathom.ai", "admin123", "Captain Morgan", UserRole.admin),
    DemoUser("ops@fathom.ai", "admin123", "Harbor Ops", UserRole.admin),
    DemoUser("crew1@fathom.ai", "crew123", "Jack Sparrow", UserRole.crew, "MV Horizon"),
    DemoUser("crew2@fathom.ai", "crew123", "Rose Dawson", UserRole.crew, "SS Pacific"),
    DemoUser("crew3@fathom.ai", "crew123", "Mina Patel", UserRole.crew, "MT Atlas"),
    DemoUser("crew4@fathom.ai", "crew123", "Luca Romero", UserRole.crew, "MV Horizon"),
    DemoUser("crew5@fathom.ai", "crew123", "Aisha Khan", UserRole.crew, "SS Pacific"),
)

DEMO_TASKS = (
    DemoTask(
        title="Inspect fire suppression valves",
        ship_name="MV Horizon",
        assigned_email="crew1@fathom.ai",
        status=TaskStatus.completed,
        due_offset_days=-6,
        description="Verify pressure readings and log valve condition for the engine room loop.",
        comments=(
            ("crew1@fathom.ai", "Inspection completed and readings logged."),
            ("admin@fathom.ai", "Verified. Closing out for this cycle."),
        ),
    ),
    DemoTask(
        title="Bridge navigation light audit",
        ship_name="MV Horizon",
        assigned_email="crew4@fathom.ai",
        status=TaskStatus.in_progress,
        due_offset_days=2,
        description="Check starboard and port light assemblies before the next evening departure.",
        comments=(
            ("crew4@fathom.ai", "Port housing cleaned, starboard bulb replacement in progress."),
        ),
    ),
    DemoTask(
        title="Lifeboat davit lubrication",
        ship_name="MV Horizon",
        assigned_email="crew1@fathom.ai",
        status=TaskStatus.pending,
        due_offset_days=-2,
        description="Lubricate davit arms and verify release gear motion on both port lifeboats.",
    ),
    DemoTask(
        title="Engine coolant sampling",
        ship_name="SS Pacific",
        assigned_email="crew2@fathom.ai",
        status=TaskStatus.completed,
        due_offset_days=-4,
        description="Take coolant samples from both generators and submit contamination notes.",
        comments=(
            ("crew2@fathom.ai", "Samples submitted with no abnormal contamination detected."),
        ),
    ),
    DemoTask(
        title="Hull corrosion spot check",
        ship_name="SS Pacific",
        assigned_email="crew5@fathom.ai",
        status=TaskStatus.pending,
        due_offset_days=5,
        description="Spot check aft ballast access points for corrosion and repaint needs.",
    ),
    DemoTask(
        title="Emergency radio battery swap",
        ship_name="SS Pacific",
        assigned_email="crew2@fathom.ai",
        status=TaskStatus.in_progress,
        due_offset_days=-1,
        description="Replace handheld emergency radio batteries and confirm spare inventory.",
        comments=(
            ("crew2@fathom.ai", "Two units replaced, waiting on final radio inventory count."),
        ),
    ),
    DemoTask(
        title="Ballast pump vibration check",
        ship_name="MT Atlas",
        assigned_email="crew3@fathom.ai",
        status=TaskStatus.completed,
        due_offset_days=-3,
        description="Log vibration levels during ballast transfer simulation.",
    ),
    DemoTask(
        title="Cargo deck drain clearing",
        ship_name="MT Atlas",
        assigned_email="crew3@fathom.ai",
        status=TaskStatus.pending,
        due_offset_days=1,
        description="Clear deck drain channels before forecasted heavy rain operations.",
    ),
    DemoTask(
        title="Portable extinguisher pressure check",
        ship_name="MT Atlas",
        assigned_email="crew3@fathom.ai",
        status=TaskStatus.pending,
        due_offset_days=-8,
        description="Check all portable extinguishers on lower cargo deck and record any low-pressure units.",
        comments=(
            ("ops@fathom.ai", "This item is overdue and should be prioritized before next inspection."),
        ),
    ),
)

DEMO_DRILLS = (
    DemoDrill(
        drill_type="fire",
        ship_name="MV Horizon",
        status=DrillStatus.completed,
        scheduled_offset_days=-7,
        description="Engine room fire containment and mustering sequence.",
        attendance=(
            ("crew1@fathom.ai", True),
            ("crew4@fathom.ai", True),
        ),
    ),
    DemoDrill(
        drill_type="abandon_ship",
        ship_name="MV Horizon",
        status=DrillStatus.scheduled,
        scheduled_offset_days=4,
        description="Abandon ship signaling, mustering, and lifeboat preparation walkthrough.",
        attendance=(
            ("crew1@fathom.ai", False),
            ("crew4@fathom.ai", False),
        ),
    ),
    DemoDrill(
        drill_type="man_overboard",
        ship_name="SS Pacific",
        status=DrillStatus.missed,
        scheduled_offset_days=-5,
        description="Starboard-side man overboard recovery drill.",
        attendance=(
            ("crew2@fathom.ai", True),
            ("crew5@fathom.ai", False),
        ),
    ),
    DemoDrill(
        drill_type="fire",
        ship_name="SS Pacific",
        status=DrillStatus.completed,
        scheduled_offset_days=-1,
        description="Galley fire isolation and extinguisher response drill.",
        attendance=(
            ("crew2@fathom.ai", True),
            ("crew5@fathom.ai", True),
        ),
    ),
    DemoDrill(
        drill_type="spill_response",
        ship_name="MT Atlas",
        status=DrillStatus.scheduled,
        scheduled_offset_days=6,
        description="Cargo deck spill containment and reporting workflow.",
        attendance=(
            ("crew3@fathom.ai", False),
        ),
    ),
    DemoDrill(
        drill_type="confined_space",
        ship_name="MT Atlas",
        status=DrillStatus.completed,
        scheduled_offset_days=-10,
        description="Confined-space permit check and emergency extraction rehearsal.",
        attendance=(
            ("crew3@fathom.ai", True),
        ),
    ),
)


def upsert_ship(db, name: str) -> Ship:
    ship = db.query(Ship).filter(Ship.name == name).first()
    if ship is None:
        ship = Ship(name=name)
        db.add(ship)
        db.flush()
    return ship


def upsert_user(db, demo_user: DemoUser, ship_lookup: dict[str, Ship]) -> User:
    user = db.query(User).filter(User.email == demo_user.email).first()
    ship_id = ship_lookup[demo_user.ship_name].id if demo_user.ship_name else None

    if user is None:
        user = User(
            email=demo_user.email,
            password_hash=hash_password(demo_user.password),
            name=demo_user.name,
            role=demo_user.role,
            ship_id=ship_id,
        )
        db.add(user)
        db.flush()
        return user

    user.name = demo_user.name
    user.role = demo_user.role
    user.ship_id = ship_id
    user.password_hash = hash_password(demo_user.password)
    db.flush()
    return user


def upsert_task(db, demo_task: DemoTask, ship_lookup: dict[str, Ship], user_lookup: dict[str, User], admin_user: User) -> MaintenanceTask:
    due_date = date.today() + timedelta(days=demo_task.due_offset_days)
    task = (
        db.query(MaintenanceTask)
        .filter(
            MaintenanceTask.title == demo_task.title,
            MaintenanceTask.ship_id == ship_lookup[demo_task.ship_name].id,
        )
        .first()
    )

    if task is None:
        task = MaintenanceTask(
            title=demo_task.title,
            description=demo_task.description,
            due_date=due_date,
            ship_id=ship_lookup[demo_task.ship_name].id,
            assigned_to=user_lookup[demo_task.assigned_email].id,
            created_by=admin_user.id,
            status=demo_task.status,
        )
        db.add(task)
        db.flush()
    else:
        task.description = demo_task.description
        task.due_date = due_date
        task.ship_id = ship_lookup[demo_task.ship_name].id
        task.assigned_to = user_lookup[demo_task.assigned_email].id
        task.created_by = admin_user.id
        task.status = demo_task.status
        db.flush()

    for author_email, content in demo_task.comments:
        comment = (
            db.query(TaskComment)
            .filter(
                TaskComment.task_id == task.id,
                TaskComment.user_id == user_lookup[author_email].id,
                TaskComment.content == content,
            )
            .first()
        )
        if comment is None:
            db.add(TaskComment(task_id=task.id, user_id=user_lookup[author_email].id, content=content))

    db.flush()
    return task


def upsert_drill(db, demo_drill: DemoDrill, ship_lookup: dict[str, Ship], user_lookup: dict[str, User], admin_user: User) -> SafetyDrill:
    scheduled_date = date.today() + timedelta(days=demo_drill.scheduled_offset_days)
    drill = (
        db.query(SafetyDrill)
        .filter(
            SafetyDrill.drill_type == demo_drill.drill_type,
            SafetyDrill.ship_id == ship_lookup[demo_drill.ship_name].id,
            SafetyDrill.scheduled_date == scheduled_date,
        )
        .first()
    )

    if drill is None:
        drill = SafetyDrill(
            drill_type=demo_drill.drill_type,
            description=demo_drill.description,
            scheduled_date=scheduled_date,
            ship_id=ship_lookup[demo_drill.ship_name].id,
            created_by=admin_user.id,
            status=demo_drill.status,
        )
        db.add(drill)
        db.flush()
    else:
        drill.description = demo_drill.description
        drill.ship_id = ship_lookup[demo_drill.ship_name].id
        drill.created_by = admin_user.id
        drill.status = demo_drill.status
        db.flush()

    for attendee_email, attended in demo_drill.attendance:
        attendance = (
            db.query(DrillAttendance)
            .filter(
                DrillAttendance.drill_id == drill.id,
                DrillAttendance.user_id == user_lookup[attendee_email].id,
            )
            .first()
        )
        if attendance is None:
            db.add(
                DrillAttendance(
                    drill_id=drill.id,
                    user_id=user_lookup[attendee_email].id,
                    attended=attended,
                )
            )
        else:
            attendance.attended = attended

    db.flush()
    return drill


def seed_demo_data() -> None:
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        ship_lookup = {name: upsert_ship(db, name) for name in DEMO_SHIPS}
        user_lookup = {demo_user.email: upsert_user(db, demo_user, ship_lookup) for demo_user in DEMO_USERS}
        admin_user = user_lookup["admin@fathom.ai"]

        for demo_task in DEMO_TASKS:
            upsert_task(db, demo_task, ship_lookup, user_lookup, admin_user)

        for demo_drill in DEMO_DRILLS:
            upsert_drill(db, demo_drill, ship_lookup, user_lookup, admin_user)

        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_demo_data()
    print("Demo data seeded successfully.")

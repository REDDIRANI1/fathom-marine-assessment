from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base, SessionLocal
from app.models import User, Ship
from app.auth import hash_password
from app.routers import auth, ships, tasks, drills, compliance


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_demo_data()
    yield


def seed_demo_data():
    db = SessionLocal()
    try:
        if db.query(User).filter(User.email == "admin@fathom.ai").first():
            return

        ship1 = Ship(name="MV Horizon")
        ship2 = Ship(name="SS Pacific")
        db.add_all([ship1, ship2])
        db.flush()

        admin = User(
            email="admin@fathom.ai",
            password_hash=hash_password("admin123"),
            name="Captain Morgan",
            role="admin",
            ship_id=None,
        )
        crew1 = User(
            email="crew1@fathom.ai",
            password_hash=hash_password("crew123"),
            name="Jack Sparrow",
            role="crew",
            ship_id=ship1.id,
        )
        crew2 = User(
            email="crew2@fathom.ai",
            password_hash=hash_password("crew123"),
            name="Rose Dawson",
            role="crew",
            ship_id=ship2.id,
        )
        db.add_all([admin, crew1, crew2])
        db.commit()
    finally:
        db.close()


app = FastAPI(title="Fathom Marine API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(ships.router, prefix="/api/v1")
app.include_router(tasks.router, prefix="/api/v1")
app.include_router(drills.router, prefix="/api/v1")
app.include_router(compliance.router, prefix="/api/v1")


@app.get("/")
def root():
    return {"message": "Fathom Marine API", "docs": "/docs"}

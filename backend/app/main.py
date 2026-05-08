from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import auth, ships, tasks, drills, compliance
from app.seed_demo import seed_demo_data


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_demo_data()
    yield


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

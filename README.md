# Fathom Marine — Maritime Operations & Compliance System

Full-stack platform for managing ship maintenance, safety drills, and regulatory compliance.

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | React 19 + TypeScript + Tailwind CSS + Recharts |
| Backend | FastAPI (Python) + SQLAlchemy + JWT Auth |
| Database | PostgreSQL |
| Containerization | Docker Compose |

## Quick Start

### 1. Clone

```bash
git clone <repo-url>
cd fathom-marine
```

### 2. Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt

# Start PostgreSQL via Docker
docker compose -f ../docker-compose.yml up -d db

# Run API
uvicorn app.main:app --reload --port 8000

# Run tests
pytest tests/ -v
```

### 3. Frontend

```bash
cd frontend
npm install
cp .env.example .env  # Update VITE_API_URL if needed
npm run dev
```

Frontend runs on `http://localhost:5173`, API on `http://localhost:8000`.

## API Endpoints

| Method | Path | Auth | Description |
|---|---|---|---|
| POST | `/api/v1/auth/register` | — | Register (returns JWT) |
| POST | `/api/v1/auth/login` | — | Login (returns JWT) |
| GET | `/api/v1/auth/me` | All | Current user info |
| GET/POST | `/api/v1/ships` | Admin | List / Create ships |
| GET/POST | `/api/v1/tasks` | All | List / Create tasks |
| PATCH | `/api/v1/tasks/{id}/status` | All | Update task status |
| POST | `/api/v1/tasks/{id}/comments` | All | Add comment |
| GET/POST | `/api/v1/drills` | All | List / Create drills |
| PATCH | `/api/v1/drills/{id}/complete` | All | Mark drill complete |
| GET | `/api/v1/compliance` | All | Compliance overview |
| GET | `/api/v1/compliance/ships` | Admin | Per-ship breakdown |

## Architecture Decisions

- **UUIDs** for all primary keys — avoids sequential ID exposure, supports distributed systems
- **Custom GUID type** with a TypeDecorator — uses PostgreSQL UUID natively, String fallback for SQLite tests
- **bcrypt** directly (not passlib) — passlib's detection bug with Python 3.14 caused issues; bcrypt is simpler and just as secure
- **JWT with RBAC** — stateless auth, role checked via FastAPI dependency injection
- **Compliance calculated server-side** — single source of truth, avoids frontend computation drift
- **React Query (TanStack) pattern** via axios interceptors — centralized auth token injection, auto-redirect on 401

## Database Schema

6 tables: `ships`, `users`, `maintenance_tasks`, `task_comments`, `safety_drills`, `drill_attendance`

See `backend/app/models.py` for the full SQLAlchemy schema.

## Demo Credentials

The app auto-seeds on first run. Use these to log in:

| User | Email | Password | Role | Ship |
|---|---|---|---|---|
| Captain Morgan | `admin@fathom.ai` | `admin123` | Admin | — |
| Jack Sparrow | `crew1@fathom.ai` | `crew123` | Crew | MV Horizon |
| Rose Dawson | `crew2@fathom.ai` | `crew123` | Crew | SS Pacific |

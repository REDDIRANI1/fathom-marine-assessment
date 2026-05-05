---
status: Ready for HITL
version: 0.1.0
---

# Coding Standards

## Merge Strategy

- **Selected strategy:** Direct to main
- **Selected by:** user
- **Decision date:** 2026-05-05
- **Rationale:** Solo-dev assessment project — simplest workflow, no integration branch overhead
- Each story squash-merges directly to main after verification

## Code Style

### Backend (FastAPI/Python)
- Follow PEP 8
- Use Pydantic models for all request/response schemas
- Separate routers per domain (maintenance, drills, compliance, auth)
- SQLAlchemy ORM with Alembic migrations
- Type hints on all functions

### Frontend (React/TypeScript)
- Strict TypeScript mode
- Functional components with hooks only
- API client in dedicated `api/` directory
- Recharts for charts
- React Router v6 for routing

### General
- TDD where practical — test critical paths (compliance calc, auth, API endpoints)
- Clean separation: backend has no frontend knowledge, frontend consumes API only
- Environment variables for all secrets (DATABASE_URL, JWT_SECRET, etc.)

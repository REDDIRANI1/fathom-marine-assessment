# Implementation Plan: Maritime Operations & Compliance System

> **Epic ID:** E-001
> **Date:** 2026-05-05
> **Status:** Draft
> **Version:** 0.1.0
>
> **Merge-strategy HITL (asked early, before story-breakdown):**
> **merge_strategy_hitl_prompt:** ""
> **merge_strategy_hitl_response:** ""
> **merge_strategy_hitl_decision:** ""
> **merge_strategy_hitl_approved_by:** ""
> **merge_strategy_hitl_approved_at:** ""
>
> **Plan approval HITL (final stage gate):**
> **plan_approval_hitl_prompt:** ""
> **plan_approval_hitl_response:** ""
> **plan_approval_hitl_decision:** ""
> **plan_approval_hitl_approved_by:** ""
> **plan_approval_hitl_approved_at:** ""

## Milestones

| Milestone | Exit Criteria |
|---|---|
| **M1: Backend API + Database** | - PostgreSQL schema with ships, users, maintenance_tasks, safety_drills, drill_attendance, task_comments tables<br>- FastAPI CRUD endpoints for tasks, drills, ships, users<br>- Compliance calculation endpoint<br>- Auth (JWT) + RBAC middleware (admin/crew)<br>- Docker Compose for local dev |
| **M2: Frontend SPA** | - React + TypeScript with Vite<br>- Login + role-based routing<br>- Maintenance Management page (admin + crew views)<br>- Drill Management page (admin + crew views)<br>- Compliance Dashboard with charts<br>- Filters (ship, status, date)<br>- Overdue notifications/badges |
| **M3: Integration + Deploy** | - Full end-to-end smoke test<br>- Deploy frontend to Vercel<br>- Deploy backend + DB to Railway<br>- Business Flow document<br>- README with setup + architecture decisions |

## Risk Log

| Risk | Likelihood | Impact | Mitigation |
|---|---|---|---|
| FastAPI auth boilerplate takes longer than expected | Medium | Medium | Use fastapi-users or simple JWT with bcrypt — don't build from scratch |
| PostgreSQL on Railway has cold start for free tier | Medium | Low | Keep connection pool, document in README |
| CORS issues between Vercel + Railway | Low | Medium | Set explicit CORS origins in FastAPI middleware |

## Interface Contracts

See `docs/architecture/data-domain.md` for full API contracts (to be written before M2 starts).

## Proposed Changes

### M1: Backend
- `backend/` — FastAPI project (requirements.txt, main.py, models, routers, schemas, auth)
- `docker-compose.yml` — FastAPI + PostgreSQL
- Alembic migrations

### M2: Frontend
- `frontend/` — Vite + React + TypeScript (App, pages, components, hooks, api client)
- Recharts for compliance charts

### M3: Deploy
- `vercel.json` for frontend
- Railway config / Procfile for backend
- `docs/business-flow.md` — Business Flow document (submission requirement)

## Definition of Done

- [ ] All 3 milestones completed
- [ ] Every FR from BRD traceable to working code
- [ ] GitHub repo with clean commit history
- [ ] Business Flow document (`docs/business-flow.md`)
- [ ] README with setup steps + architecture decisions
- [ ] Deployed + working (Vercel + Railway live links)
- [ ] Docker Compose works locally (`docker compose up`)

---
*Written by: agentic-sdlc implementation-planning skill*

# Fathom Marine — Business Flow

## Overview

Fathom Marine is a maritime operations & compliance platform that helps organizations manage ship maintenance, safety drills, and regulatory compliance across a fleet of vessels.

## Actors

| Actor | Role |
|---|---|
| **Admin** | Creates ships, schedules maintenance tasks & drills, monitors fleet compliance |
| **Crew** | Views assigned tasks, updates status, comments, marks drill attendance |

## Business Flows

### 1. Ship Setup (Admin Only)

```
Admin → "Add Ship" → Ship created in system
                      ↓
            Available for task/drill assignment
```

### 2. Maintenance Task Flow

```
Admin creates task → Assigns to ship + due date
                        ↓
Crew member sees assigned task → Updates status (pending → in_progress → completed)
                                  ↓
Crew can add comments/notes
                                  ↓
System tracks: completed % vs pending/overdue
```

### 3. Safety Drill Flow

```
Admin schedules drill → Assigns type (fire, evacuation, etc.) + ship + date
                          ↓
Crew views upcoming drills → Marks attendance → Marks completion
                                ↓
System tracks: drill participation %
Missed drills (past date, not completed) → flagged as non-compliant
```

### 4. Compliance Calculation

The system calculates compliance per ship based on two metrics:

- **Maintenance Compliance** = completed_tasks / total_tasks × 100
- **Drill Compliance** = completed_drills / total_drills × 100
- **Overall Compliance** = (maintenance_pct + drill_pct) / 2

### 4.1 Overdue / Missed Logic

- **Overdue task:** `due_date < today AND status != 'completed'`
- **Missed drill:** `scheduled_date < today AND status != 'completed'`

Both are highlighted on the dashboard as alerts.

### 5. Role-Based Access

| Action | Admin | Crew |
|---|---|---|
| Create ships | ✅ | ❌ |
| Create/edit tasks | ✅ | ❌ |
| Update task status | ✅ | ✅ (own tasks) |
| Add/view task comments | ✅ | ✅ (own tasks) |
| Schedule drills | ✅ | ❌ |
| Mark drill attendance | ✅ | ✅ (own ship / own record) |
| Mark drill complete | ✅ | ✅ (own ship) |
| View compliance dashboard | ✅ (all ships) | ✅ (own ship) |

## Data Flow

```
Frontend (React SPA)
    ↕ REST API (JWT auth)
Backend (FastAPI)
    ↕ SQLAlchemy ORM
PostgreSQL Database
```

## State Machine — Maintenance Task

```
┌─────────┐    ┌─────────────┐    ┌───────────┐
│ Pending │ → │ In Progress  │ → │ Completed │
└─────────┘    └─────────────┘    └───────────┘
      ↑              ↕                    ↑
      └──────────────┴────────────────────┘
              Any status → Any status
```

## State Machine — Safety Drill

```
┌───────────┐               ┌───────────┐
│ Scheduled │  ──────────▶  │ Completed │
└───────────┘               └───────────┘
       │
       ▼ (past date, not completed)
┌───────────┐
│   Missed  │
└───────────┘
```

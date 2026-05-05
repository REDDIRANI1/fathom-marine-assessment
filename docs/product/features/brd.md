---
status: Ready for HITL
version: 1.0.0
created: 2026-05-05
hitl_prompt: ""
hitl_response: ""
hitl_decision: ""
hitl_approved_by: ""
hitl_approved_at: ""
---

# Business Requirements Document: Maritime Operations & Compliance System

## 1. Business Objective

Build a full-stack web application for a marine organization to manage ship maintenance activities, safety drills, and compliance monitoring. The system tracks whether ships are operationally safe and compliant with regulations, highlighting risks through a compliance dashboard.

**Measurable success criteria:**
- Admins can create, assign, and track maintenance tasks with statuses (Pending → In Progress → Completed)
- Admins can schedule and assign safety drills to ships
- Crew members can view assigned tasks, update status, add notes
- Crew members can view drills, mark attendance, submit completion
- The compliance dashboard shows pending/overdue tasks, missed drills, and completion percentages
- Overdue items (past due/scheduled date without completion) are flagged as non-compliant
- Compliance % = completed maintenance % and drill participation % — visible per ship and fleet-wide

## 2. User Personas

### Persona 1: Admin (Shore-based Fleet Manager)
- **Role:** Manages maintenance schedules and safety drills across multiple ships
- **Jobs-to-be-done:**
  - Create maintenance tasks with due dates and assign to specific crew on specific ships
  - Schedule safety drills (fire, evacuation, etc.) and assign to ships
  - Monitor compliance dashboard to identify overdue tasks and missed drills
  - Filter by ship, status, and date range
  - Receive notifications about overdue items
- **Pain points:** Needs clear visibility into fleet-wide compliance, wants to catch overdue items before they become regulatory issues

### Persona 2: Crew Member (Shipboard Personnel)
- **Role:** Executes maintenance tasks and participates in safety drills
- **Jobs-to-be-done:**
  - View tasks assigned to them on their ship
  - Update task status (Pending → In Progress → Completed)
  - Add notes/comments on tasks (e.g., "Waiting for spare parts")
  - View upcoming scheduled drills
  - Mark drill attendance and submit drill completion
- **Pain points:** Needs a simple, focused view of what they need to do today

## 3. Functional Requirements

### FR-1: Ship Maintenance Module
| ID | Requirement | Priority |
|---|---|---|
| FR-1.1 | Admin creates maintenance task with: title, description, due date, ship, assigned crew | P0 |
| FR-1.2 | Admin updates task status (Pending / In Progress / Completed) | P0 |
| FR-1.3 | Crew views their assigned tasks filtered by ship | P0 |
| FR-1.4 | Crew updates task status | P0 |
| FR-1.5 | Crew adds notes/comments on tasks | P0 |
| FR-1.6 | Filter tasks by ship, status, date range | P1 |

### FR-2: Safety Drill Management
| ID | Requirement | Priority |
|---|---|---|
| FR-2.1 | Admin schedules drill with: type, description, scheduled date, ship | P0 |
| FR-2.2 | Admin assigns drills to ships | P0 |
| FR-2.3 | Crew views upcoming drills for their ship | P0 |
| FR-2.4 | Crew marks attendance for a drill | P0 |
| FR-2.5 | Crew submits drill completion | P0 |
| FR-2.6 | Filter drills by ship, type, status, date | P1 |

### FR-3: Compliance Dashboard
| ID | Requirement | Priority |
|---|---|---|
| FR-3.1 | Show pending maintenance tasks count | P0 |
| FR-3.2 | Show missed/overdue drills count | P0 |
| FR-3.3 | Show completed vs pending activities ratio | P0 |
| FR-3.4 | Highlight overdue maintenance tasks | P0 |
| FR-3.5 | Highlight missed safety drills | P0 |
| FR-3.6 | Display compliance percentage per ship and fleet-wide | P0 |
| FR-3.7 | Charts/graphs for compliance trends | P1 |
| FR-3.8 | Notifications for overdue tasks/drills | P1 |

### FR-4: Role-Based Access Control
| ID | Requirement | Priority |
|---|---|---|
| FR-4.1 | Admin role: full CRUD on tasks and drills, view all ships | P2 |
| FR-4.2 | Crew role: view own tasks, own ship drills, update status, add notes | P2 |

## 4. Non-Functional Requirements

| NFR | Requirement |
|---|---|
| Performance | Dashboard loads within 2 seconds for fleets up to 50 ships |
| Security | Role-based access (Admin vs Crew) enforced server-side; no cross-ship data leakage |
| Availability | 99% uptime for demo (single deployment, no HA required) |
| Code Quality | TDD, clean separation of concerns, TypeScript on frontend, Python/FastAPI on backend |
| Database | PostgreSQL with proper foreign keys, indexes, migrations |
| DevOps | Docker Compose for local dev, deploy to Vercel (FE) + Railway/Render (BE+DB) |

## 5. Out of Scope

- Multi-tenant platform (this is a single marine organization)
- Real-time notifications (polling or simple badge counts are sufficient)
- Integration with real maritime regulatory databases (SOLAS, MARPOL)
- Mobile native apps (responsive web is sufficient)
- Multi-language support
- Audit logging

## 6. Compliance Calculation Logic

```
Maintenance Compliance (%) = (Completed tasks / Total tasks) × 100
Drill Compliance (%) = (Completed drills / Scheduled drills) × 100
Overall Compliance (%) = (Maintenance Compliance + Drill Compliance) / 2

Non-compliance rule:
  If task.due_date < today AND task.status != 'Completed' → Overdue → Non-compliant
  If drill.scheduled_date < today AND drill.status != 'Completed' → Missed → Non-compliant
```

## 7. Prior Art

Researched 5 industry platforms (see domain model for details):

| Platform | Key Takeaway |
|---|---|
| **Helm CONNECT** | Rule-engine approach: regulation → task mapping with interval-based scheduling |
| **DNV Navigator** | Regulatory knowledge base with geofenced compliance rules |
| **ABS Wavesight** | Certificate & survey lifecycle model with severity-weighted scoring |
| **MariApps** | Gap-analysis: "required state" vs "actual state" with risk ratings |
| **BASSnet** | Hierarchical: Requirements → Tasks → Evidence with roll-up KPIs |

**Adopted patterns for this project:**
- Task generation with due dates (not full regulatory rule engine — simplified for assessment)
- Compliance % roll-up from individual items → ship → fleet
- Binary overdue detection (past due date without completion = non-compliant)

## 8. Tech Stack

| Tier | Choice | Rationale |
|---|---|---|
| Frontend | React + TypeScript | Assessment preference, type safety |
| Backend | FastAPI (Python) | Fast, auto-docs (Swagger), async, good for data APIs |
| Database | PostgreSQL | Relational model fits compliance data well |
| Deployment | Vercel (FE) + Railway (BE+DB) | Free tier friendly, easy setup |

## 9. Assumptions & Open Questions

- One organization with multiple ships and crew members
- Crew members are assigned to specific ships
- Drills are ship-wide (all crew on the ship participate)
- No integration with real maritime regulatory databases — simplified compliance model
- Authentication is in scope (needed for RBAC)

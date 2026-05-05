# Interface Contracts

> **Status:** Draft
> **Version:** 0.1.0

## Database Schema (PostgreSQL)

### ships
| Column | Type | Notes |
|---|---|---|
| id | UUID | PK |
| name | VARCHAR(100) | NOT NULL, UNIQUE |
| created_at | TIMESTAMP | DEFAULT NOW() |

### users
| Column | Type | Notes |
|---|---|---|
| id | UUID | PK |
| email | VARCHAR(255) | NOT NULL, UNIQUE |
| password_hash | VARCHAR(255) | NOT NULL |
| role | VARCHAR(10) | NOT NULL, 'admin' or 'crew' |
| ship_id | UUID | FK → ships, nullable (admins may not be on a ship) |
| name | VARCHAR(100) | NOT NULL |
| created_at | TIMESTAMP | DEFAULT NOW() |

### maintenance_tasks
| Column | Type | Notes |
|---|---|---|
| id | UUID | PK |
| title | VARCHAR(200) | NOT NULL |
| description | TEXT | nullable |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'pending' — 'pending','in_progress','completed' |
| due_date | DATE | NOT NULL |
| ship_id | UUID | FK → ships, NOT NULL |
| assigned_to | UUID | FK → users, nullable |
| created_by | UUID | FK → users, NOT NULL |
| created_at | TIMESTAMP | DEFAULT NOW() |
| updated_at | TIMESTAMP | DEFAULT NOW() |

### task_comments
| Column | Type | Notes |
|---|---|---|
| id | UUID | PK |
| task_id | UUID | FK → maintenance_tasks, NOT NULL |
| user_id | UUID | FK → users, NOT NULL |
| content | TEXT | NOT NULL |
| created_at | TIMESTAMP | DEFAULT NOW() |

### safety_drills
| Column | Type | Notes |
|---|---|---|
| id | UUID | PK |
| drill_type | VARCHAR(50) | NOT NULL — 'fire','evacuation','man_overboard','other' |
| description | TEXT | nullable |
| scheduled_date | DATE | NOT NULL |
| status | VARCHAR(20) | NOT NULL, DEFAULT 'scheduled' — 'scheduled','completed','missed' |
| ship_id | UUID | FK → ships, NOT NULL |
| created_by | UUID | FK → users, NOT NULL |
| created_at | TIMESTAMP | DEFAULT NOW() |

### drill_attendance
| Column | Type | Notes |
|---|---|---|
| id | UUID | PK |
| drill_id | UUID | FK → safety_drills, NOT NULL |
| user_id | UUID | FK → users, NOT NULL |
| attended | BOOLEAN | NOT NULL, DEFAULT false |
| created_at | TIMESTAMP | DEFAULT NOW() |

## REST API Endpoints

Base URL: `/api/v1`

### Auth
```
POST   /auth/register        # { email, password, name, role, ship_id? } → { user, token }
POST   /auth/login           # { email, password } → { user, token }
GET    /auth/me              # → { user } (requires auth)
```

### Ships
```
GET    /ships                # → [ships] (admin: all, crew: own ship)
POST   /ships                # { name } → ship (admin only)
```

### Maintenance Tasks
```
GET    /tasks                # ?ship_id=&status=&assigned_to= → [tasks] (admin: all, crew: own)
POST   /tasks                # { title, description?, due_date, ship_id, assigned_to } → task (admin)
PATCH  /tasks/:id/status     # { status: 'pending'|'in_progress'|'completed' } → task
POST   /tasks/:id/comments   # { content } → comment
GET    /tasks/:id/comments   # → [comments]
```

### Safety Drills
```
GET    /drills               # ?ship_id=&status=&drill_type= → [drills] (admin: all, crew: own ship)
POST   /drills               # { drill_type, description?, scheduled_date, ship_id } → drill (admin)
POST   /drills/:id/attendance # { user_id, attended } → attendance (admin/crew marking own)
PATCH  /drills/:id/complete  # → drill (marks status 'completed')
```

### Compliance
```
GET    /compliance            # ?ship_id= (optional) → { maintenance_pct, drill_pct, overall_pct, overdue_tasks, missed_drills }
GET    /compliance/ships      # → [{ ship_id, ship_name, maintenance_pct, drill_pct }]
```

## Compliance Calculation Logic

```python
# For a given ship (or all ships):
total_tasks = count(maintenance_tasks)
completed_tasks = count(maintenance_tasks WHERE status == 'completed')
maintenance_pct = (completed_tasks / total_tasks * 100) if total_tasks > 0 else 100

total_drills = count(safety_drills)
completed_drills = count(safety_drills WHERE status == 'completed')
drill_pct = (completed_drills / total_drills * 100) if total_drills > 0 else 100

overall_pct = (maintenance_pct + drill_pct) / 2

overdue_tasks = count(maintenance_tasks WHERE due_date < today AND status != 'completed')
missed_drills = count(safety_drills WHERE scheduled_date < today AND status != 'completed')
```

## Shared Types (TypeScript)

```typescript
// Mirrors backend schemas for frontend consumption

interface Ship {
  id: string;
  name: string;
}

interface User {
  id: string;
  email: string;
  name: string;
  role: 'admin' | 'crew';
  ship_id: string | null;
}

interface MaintenanceTask {
  id: string;
  title: string;
  description: string | null;
  status: 'pending' | 'in_progress' | 'completed';
  due_date: string; // ISO date
  ship_id: string;
  assigned_to: string | null;
  created_by: string;
  created_at: string;
  updated_at: string;
}

interface TaskComment {
  id: string;
  task_id: string;
  user_id: string;
  content: string;
  created_at: string;
}

interface SafetyDrill {
  id: string;
  drill_type: 'fire' | 'evacuation' | 'man_overboard' | 'other';
  description: string | null;
  scheduled_date: string;
  status: 'scheduled' | 'completed' | 'missed';
  ship_id: string;
  created_by: string;
  created_at: string;
}

interface DrillAttendance {
  id: string;
  drill_id: string;
  user_id: string;
  attended: boolean;
  created_at: string;
}

interface ComplianceStats {
  maintenance_pct: number;
  drill_pct: number;
  overall_pct: number;
  overdue_tasks: number;
  missed_drills: number;
}

interface ShipCompliance extends ComplianceStats {
  ship_id: string;
  ship_name: string;
}
```

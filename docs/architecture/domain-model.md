# Domain Model: Maritime Operations & Compliance

## Industry Context

The maritime industry operates under strict international regulations (SOLAS, MARPOL, ISM Code, MLC) enforced by flag states, port states, and classification societies. Vessels must maintain equipment, conduct regular safety drills, and demonstrate compliance through documented evidence. Non-compliance leads to detention, fines, and safety risks.

## Glossary

| Term | Definition |
|---|---|
| **Maintenance Task** | A scheduled or ad-hoc work item for ship equipment/ systems (e.g., engine inspection, hull repair) |
| **Safety Drill** | A simulated emergency exercise (fire, evacuation, man overboard) required at regulated intervals |
| **Compliance** | The state of meeting all regulatory requirements — calculated as percentage of completed tasks/drills within their due windows |
| **Overdue** | A maintenance task or drill past its scheduled/due date without completion |
| **Non-compliant** | An item that was not completed on time — contributes negatively to compliance score |
| **Crew** | Maritime personnel assigned to a ship, responsible for executing maintenance tasks and participating in drills |
| **Admin** | Shore-based or fleet management staff who create, assign, and oversee maintenance tasks and drills |

## Key Entities

```
Ship ──1:N──▶ MaintenanceTask
Ship ──1:N──▶ SafetyDrill
Crew ──N:M──▶ Ship (crew members assigned to ships)
Crew ──1:N──▶ MaintenanceTask (assigned tasks)
Crew ──N:M──▶ SafetyDrill (attendance/participation)
MaintenanceTask ──1:N──▶ TaskComment
```

## Business Rules

1. Every maintenance task has a `due_date`
2. Every safety drill has a `scheduled_date`
3. If a task/drill is not completed by its date, it becomes **non-compliant**
4. Maintenance compliance % = (completed tasks / total tasks) × 100
5. Drill participation % = (completed drills / scheduled drills) × 100
6. Overall compliance = weighted average of maintenance and drill compliance

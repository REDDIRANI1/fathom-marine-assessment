# Demo Data Guide

This project includes a dedicated demo data seeder for loading realistic sample data into an existing database.

## Seed Command

For Render shell on the API service:

```bash
cd /opt/render/project/src/backend
python -m app.seed_demo
```

For local use:

```bash
cd backend
python -m app.seed_demo
```

The script is idempotent, so it can be run multiple times safely.

## Demo Accounts

### Admin Users

| Name | Email | Password | Role |
|---|---|---|---|
| Captain Morgan | `admin@fathom.ai` | `admin123` | Admin |
| Harbor Ops | `ops@fathom.ai` | `admin123` | Admin |

### Crew Users

| Name | Email | Password | Role | Ship |
|---|---|---|---|---|
| Jack Sparrow | `crew1@fathom.ai` | `crew123` | Crew | MV Horizon |
| Rose Dawson | `crew2@fathom.ai` | `crew123` | Crew | SS Pacific |
| Mina Patel | `crew3@fathom.ai` | `crew123` | Crew | MT Atlas |
| Luca Romero | `crew4@fathom.ai` | `crew123` | Crew | MV Horizon |
| Aisha Khan | `crew5@fathom.ai` | `crew123` | Crew | SS Pacific |

## Seeded Ships

- `MV Horizon`
- `SS Pacific`
- `MT Atlas`

## Seeded Demo Records

The seeder creates:

- 3 ships
- 7 users
- 9 maintenance tasks
- 6 task comments
- 6 drills
- 10 attendance records

## Demo Scenario Coverage

The seeded data is meant to show useful dashboard states:

- completed, in-progress, pending, and overdue maintenance tasks
- completed, scheduled, and missed drills
- mixed drill attendance across ships
- comments from both admin and crew users
- cross-ship compliance differences for admin dashboard review

## Recommended Demo Flow

1. Sign in as `admin@fathom.ai` / `admin123`.
2. Review fleet-level compliance and ship activity.
3. Open maintenance and drill views to show mixed statuses.
4. Sign in as a crew user like `crew1@fathom.ai` / `crew123`.
5. Show crew-scoped task visibility and drill participation.

## Notes

- The script updates or creates the known demo rows only.
- It does not wipe the database.
- It is intended for an existing Render Postgres database as well as local development.

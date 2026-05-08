# Demo Data Guide

This project includes a dedicated demo data seeder for loading realistic sample data into an existing database.

## Seed Command

On Render free tier (no shell access), seeding runs automatically on every service start. The API `startCommand` in [`render.yaml`](./render.yaml) is:

```bash
python -m app.seed_demo && uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

The seeder runs only when the database is empty (no `users` rows). On subsequent restarts it detects existing data and skips, so any edits you make during a demo are preserved across cold starts.

### Forcing a re-seed (no DB shell needed)

To wipe and re-seed on the Render free tier:

1. In the Render dashboard, open the `fathom-api` service → **Environment**.
2. Add (or set) the env var `RESEED_ON_START=true` and save. Render auto-restarts the service; on boot it drops all tables, recreates them, and re-seeds.
3. Once the service is healthy, set `RESEED_ON_START=false` (or delete the var) and restart again so the next deploy doesn't wipe your data.

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

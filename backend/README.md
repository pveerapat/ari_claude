# ARI Backend

FastAPI backend for ARI V1.

## Starting Locally

```bash
# From repo root
cp .env.example .env
docker compose up -d --build api
```

Or run directly (requires Python 3.12+ and dependencies installed):

```bash
cd backend
pip install -e .
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## Health Check

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/health
```

Expected response:

```json
{"status": "ok", "service": "ari-backend", "api": "/api/v1"}
```

## What P2-2 Implements

- `app/main.py` — FastAPI app entry, mounts `/api/v1`, exposes `GET /health`
- `app/api/v1/health.py` — `GET /api/v1/health`
- `app/api/v1/router.py` — API v1 router
- `app/core/config.py` — Settings loaded from environment
- `app/db/base.py` — SQLAlchemy Base placeholder
- `app/db/session.py` — Database session placeholder
- `alembic.ini` — Alembic placeholder only

## What Is Deferred

| Feature | Deferred to |
|---------|-------------|
| Backend feature foundation | P2-3 |
| Database and Alembic migrations | P2-4 |
| Auth and onboarding | P2-5 |
| Farm / Zone / Tree APIs | P2-6 |
| Notebook / upload / sync | P2-7 |

## Forbidden Backend Modules

Do not create:
- `api/v1/auth.py`, `users.py`, `farms.py`, `zones.py`, `trees.py`
- `api/v1/notebook_entries.py`, `note_items.py`, `follow_ups.py`
- `api/v1/notifications.py`, `upload_queue.py`, `files.py`, `sync.py`
- `consultation_service.py`, `qr_registry_service.py`, `permission_service.py`
- `models/`, `schemas/`, `repositories/`, `services/`

# ARI Backend

FastAPI backend for ARI V1.

## Starting Locally

```bash
# From repo root
cp .env.example .env
docker-compose up -d --build
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

## Running Tests

```bash
docker-compose exec -T api pytest -v
```

## What P2-2 Implements

| File | Purpose |
|------|---------|
| `app/main.py` | FastAPI app entry, mounts `/api/v1`, exposes `GET /health` |
| `app/api/v1/health.py` | `GET /api/v1/health` |
| `app/api/v1/router.py` | API v1 router |
| `app/core/config.py` | Settings loaded from environment |
| `app/db/base.py` | SQLAlchemy Base placeholder |
| `app/db/session.py` | Database session placeholder |
| `alembic.ini` | Alembic placeholder only |

## What P2-3 Adds

| File | Purpose |
|------|---------|
| `app/core/constants.py` | Service name, prefix, error code constants |
| `app/core/logging.py` | `setup_logging()`, `get_logger()` |
| `app/core/response.py` | `success_response()`, `list_response()`, `error_response()` |
| `app/core/errors.py` | `AppError`, `register_exception_handlers()` |
| `app/middleware/request_id.py` | Reads/generates `X-Request-ID`, echoes in response |
| `app/dependencies/db.py` | `get_db()` — request-scoped DB session with rollback |
| `app/schemas/common.py` | `SuccessResponse[T]`, `ListResponse[T]`, `ErrorResponse`, `Pagination`, `HealthResponse` |
| `app/repositories/base.py` | `BaseRepository[ModelType]` pattern |
| `app/services/base.py` | `BaseService` pattern with session lifecycle notes |
| `app/utils/datetime.py` | `utcnow()`, `to_iso()`, `utcnow_iso()` |
| `app/utils/uuid.py` | `generate_uuid()`, `is_valid_uuid()` |
| `app/utils/pagination.py` | `pagination_meta()`, `calc_offset()`, `clamp_page/page_size()` |
| `app/tests/test_health.py` | 6 foundation health tests |
| `app/tests/test_app_startup.py` | 14 foundation startup/util tests |

## What Is Deferred

| Feature | Deferred to |
|---------|-------------|
| `core/security.py` (JWT/password) | P2-5 |
| `core/enums.py` (domain enums) | P2-4 |
| `dependencies/auth.py`, `rbac.py`, `scope.py` | P2-5 |
| Database and Alembic migrations | P2-4 |
| Auth and onboarding | P2-5 |
| Farm / Zone / Tree APIs | P2-6 |
| Notebook / upload / sync | P2-7 |
| Mobile MVP | P2-8 |
| Web MVP | P2-9 |
| E2E and prototype deployment | P2-10 |

## Key Locations

| Concept | Location |
|---------|----------|
| Common response helpers | `app/core/response.py` |
| Common error foundation | `app/core/errors.py` |
| Logging setup | `app/core/logging.py` |
| Request ID middleware | `app/middleware/request_id.py` |
| DB dependency | `app/dependencies/db.py` |
| Common schemas | `app/schemas/common.py` |
| Base repository | `app/repositories/base.py` |
| Base service | `app/services/base.py` |
| Tests | `app/tests/` |

## Forbidden Backend Modules

Do not create in P2-3:

- `api/v1/auth.py`, `users.py`, `organizations.py`, `farms.py`, `zones.py`, `trees.py`
- `api/v1/notebook_entries.py`, `note_items.py`, `follow_ups.py`
- `api/v1/notifications.py`, `upload_queue.py`, `files.py`, `sync.py`
- `core/security.py`, `core/enums.py`
- `dependencies/auth.py`, `dependencies/rbac.py`, `dependencies/scope.py`
- `models/` (any file)
- `consultation_service.py`, `qr_registry_service.py`, `permission_service.py`
- Any real Alembic migration version files

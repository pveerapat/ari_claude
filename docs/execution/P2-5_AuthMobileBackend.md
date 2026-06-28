# ARI V1 — P2-5 Auth and Mobile Onboarding Backend v1.0

## Document Type

P2 Coding Execution Document

## Status

IMPLEMENTED

## Phase

P2-5 — Auth and Mobile Onboarding Backend

## Frozen Source Documents

- ARI V1 — P0 Domain Model Specification v1.0 (FROZEN)
- ARI V1 — P0 Database Schema Specification v1.0 + Additive Revision v1.1 (FROZEN)
- ARI V1 — P0 API Specification v1.0 + Additive Revision v1.1 (FROZEN)
- ARI V1 — P1-1 Backend Implementation Spec v1.0 (FROZEN)
- ARI V1 — P1-2 Mobile App Spec (FROZEN)

## Prerequisites Confirmed

- P2-2 Monorepo: FROZEN, IMPLEMENTED
- P2-3 Backend: FROZEN, IMPLEMENTED
- P2-4 Database + Alembic: FROZEN, IMPLEMENTED (alembic upgrade head verified, 82/82 pytest passed)

---

## Implementation Summary

P2-5 adds JWT authentication, phone-based registration, and mobile onboarding flows on top of the existing P2-4 schema. No new database migration was required — all required columns (`phone`, `farmer_status`, `membership_status`, `account_status`, `primary_farm_id`, `password_hash`, `role`) were already created in the P2-4 migration.

---

## Files Created

| File | Purpose |
|------|---------|
| `backend/app/auth/__init__.py` | Package marker |
| `backend/app/auth/utils.py` | `normalize_phone`, `hash_password`, `verify_password`, `create_access_token`, `create_refresh_token`, `decode_token` |
| `backend/app/schemas/auth.py` | Pydantic request/response schemas for all auth endpoints |
| `backend/app/repositories/auth.py` | `AuthRepository`: user by phone, user by id, farm by id, create user, create org |
| `backend/app/services/auth.py` | `AuthService`: register, login, refresh, get_user_by_id |
| `backend/app/dependencies/auth.py` | `get_current_user`, `require_authenticated_user`, `require_active_account`, `require_active_membership` |
| `backend/app/api/v1/auth.py` | Auth router: register, login, refresh, me, logout |
| `backend/app/tests/test_auth_utils.py` | Unit tests: phone norm, password, JWT |
| `backend/app/tests/test_auth_service.py` | Service tests with mocked repository |
| `backend/app/tests/test_auth_api.py` | API tests with mocked service/dependencies |

## Files Modified

| File | Change |
|------|--------|
| `backend/requirements.txt` | Added `bcrypt>=4.0.0`, `python-jose[cryptography]>=3.3.0` |
| `backend/pyproject.toml` | Added same dependencies |
| `backend/app/api/v1/router.py` | Registered `auth.router` |
| `backend/app/tests/test_app_startup.py` | Updated `test_no_feature_routes` → `test_no_unimplemented_feature_routes`; added `test_auth_routes_registered` |

---

## Endpoint Summary

| Method | Path | Auth | Description |
|--------|------|------|-------------|
| POST | `/api/v1/auth/register` | None | Register owner / owner_family / farm_staff |
| POST | `/api/v1/auth/login` | None | Login by phone + password |
| POST | `/api/v1/auth/refresh` | None | Exchange refresh token for new access token |
| GET | `/api/v1/auth/me` | Bearer | Return current user onboarding state |
| POST | `/api/v1/auth/logout` | Bearer | Logout boundary (returns success, no token blacklist) |

---

## Registration Flows

### Owner

- `farmer_status = owner`
- Creates a new `Organization` (type = individual)
- `role = farmer`
- `membership_status = active`
- `account_status = active_pending_verification`
- `primary_farm_id = null`
- Returns `access_token` + `refresh_token`

### owner_family / farm_staff

- `farmer_status = owner_family | farm_staff`
- `farm_id` required — validated against `farms` table
- `organization_id` resolved from `farm.organization_id`
- `role = farmer`
- `primary_farm_id = provided farm_id`
- `membership_status = pending_farm_approval`
- `account_status = active`
- Returns `access_token` + `refresh_token`

---

## JWT Claims

```json
{
  "sub": "user_id",
  "organization_id": "uuid",
  "role": "farmer",
  "type": "access",
  "exp": "<timestamp>"
}
```

Refresh token carries only `sub`, `type`, and `exp`.

---

## Auth Guards

| Guard | Behavior |
|-------|---------|
| `get_current_user` | Decodes Bearer JWT, loads user from DB |
| `require_authenticated_user` | Alias for `get_current_user` |
| `require_active_account` | Blocks if `account_status` not in `{active, active_pending_verification}` |
| `require_active_membership` | Blocks if `membership_status != active` — for protected farm-scoped routes (P2-6+) |

---

## Dependencies Added

| Package | Version | Purpose |
|---------|---------|---------|
| `bcrypt` | >=4.0.0 | Password hashing (used directly, not via passlib) |
| `python-jose[cryptography]` | >=3.3.0 | JWT encode/decode |

**Note on passlib:** `passlib[bcrypt]` was evaluated but incompatible with `bcrypt>=5.0.0` (version conflict in wrap-bug detection). Switched to `bcrypt` directly.

---

## Database Migration

**No new migration required.**

All P2-5 fields were already created in P2-4 migration `a1b2c3d4e5f6`:
- `users.phone`
- `users.password_hash`
- `users.role`
- `users.farmer_status`
- `users.membership_status`
- `users.account_status`
- `users.primary_farm_id`
- `users.registered_at`

---

## Test Results

```
pytest app/tests/
157 passed in ~12s
```

Previous count (P2-4): 82 tests
P2-5 additions: 75 new tests

### New Tests Added

| File | Tests |
|------|-------|
| `test_auth_utils.py` | phone normalization (7), password hash/verify (6), JWT creation (3), JWT decode (6) |
| `test_auth_service.py` | owner register (7), owner_family/farm_staff register (10), login (4), refresh (3) |
| `test_auth_api.py` | register endpoint (9), login endpoint (4), refresh endpoint (3), me endpoint (6), logout endpoint (2) |
| `test_app_startup.py` | `test_auth_routes_registered` (1), updated `test_no_unimplemented_feature_routes` (1) |

---

## API Gaps

No new API gaps were identified during P2-5 implementation.

All required frozen fields were present in the P2-4 schema. All frozen API behaviors were implementable without schema changes.

---

## Smoke Test Commands

```bash
# Start services
docker compose up -d

# Run migrations
docker compose exec api alembic upgrade head

# Run tests
docker compose exec api pytest app/tests/ -q

# Register owner
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"phone":"0812345678","name":"Somchai","password":"1234","farmer_status":"owner"}'

# Login
curl -X POST http://localhost:8000/api/v1/auth/login \
  -H "Content-Type: application/json" \
  -d '{"phone":"0812345678","password":"1234"}'

# Auth Me (replace TOKEN)
curl http://localhost:8000/api/v1/auth/me \
  -H "Authorization: Bearer TOKEN"

# Refresh (replace REFRESH_TOKEN)
curl -X POST http://localhost:8000/api/v1/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh_token":"REFRESH_TOKEN"}'

# Logout
curl -X POST http://localhost:8000/api/v1/auth/logout \
  -H "Authorization: Bearer TOKEN"

# Duplicate phone (should return 409)
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H "Content-Type: application/json" \
  -d '{"phone":"0812345678","name":"Another","password":"1234","farmer_status":"owner"}'
```

---

## Out of Scope (Confirmed Deferred)

- Farm CRUD (P2-6+)
- farm_memberships table (NEVER — frozen exclusion)
- Token blacklist / refresh_tokens table (NEVER — frozen exclusion)
- auth_sessions table (NEVER — frozen exclusion)
- Permission service / ABAC (NEVER — frozen exclusion)
- Owner-managed approval screen (P2-6+)
- Email login (not implemented — phone login is P2-5 requirement)

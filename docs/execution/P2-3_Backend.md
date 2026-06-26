# ARI V1 — P2-3 Backend Feature Foundation v1.0

Project: ARI — Agricultural Intelligence Platform
Phase: P2 Coding Execution Phase
Document Number: P2-3
Document Type: Backend Feature Foundation Specification / Execution Document
Version: v1.0
Status: Draft Final / Ready for Owner Freeze
Prepared From: Frozen Source of Truth + P2-1 / P2-2 Coding Execution Authority
Coding Direction: Backend Foundation First → Database → Auth → Farm Structure → Notebook / Upload / Sync → Mobile MVP → Web MVP → E2E → Prototype Deployment

---

# 1. Document Control

## 1.1 Document Identity

```text
Document Title:
ARI V1 — P2-3 Backend Feature Foundation v1.0

Project:
ARI — Agricultural Intelligence Platform

Phase:
P2 Coding Execution Phase

Document Number:
P2-3

Document Status:
Draft Final / Ready for Owner Freeze

Previous Frozen Documents:
ARI V1 — P2-1 Coding Execution Plan & Sprint Backlog v1.0
Status: FROZEN

ARI V1 — P2-2 Monorepo & Local Development Setup v1.0
Status: FROZEN

P2-2 Coding Foundation:
IMPLEMENTED

P2-2 Smoke Test:
PASS
```

## 1.2 Latest P2-2 Status Clarification

The uploaded P2-2 source file may still show earlier metadata such as:

```text
Draft / Not Frozen
```

For P2-3 execution, the latest Owner-confirmed status is authoritative:

```text
P2-2 Document: FROZEN
P2-2 Coding Foundation: IMPLEMENTED
P2-2 Smoke Test: PASS
```

## 1.3 Document Boundary

This document defines the backend feature foundation only.

It is still a specification / execution document.

It does not authorize actual ARI business feature coding beyond generic backend foundation files.

It does not authorize database migrations, authentication, farm APIs, notebook APIs, upload / sync APIs, mobile screens, web pages, or deployment work.

## Comment

P2-3 exists to make the backend codebase ready for later ARI business feature implementation without letting coding agents accidentally create feature modules, new entities, new tables, or forbidden services too early.

---

# 2. Purpose

The purpose of P2-3 is to define the safe backend foundation after P2-2.

P2-3 prepares the FastAPI backend for later implementation of:

```text
Database and Alembic migrations
Auth and mobile onboarding
Farm structure APIs
Notebook APIs
Upload / sync APIs
Mobile MVP integration
Web MVP integration
```

But P2-3 does not implement those features yet.

P2-3 defines:

```text
Backend package organization
API v1 router foundation
Common response convention
Common error handling foundation
Logging foundation
CORS foundation
Request ID middleware foundation
Configuration foundation
Database session integration placeholder
SQLAlchemy Base boundary
Repository / service / router pattern definition
Dependency injection foundation
Testing foundation
Code quality foundation
Backend README update requirements
Backend smoke test update
AI coding guardrail update if needed
GitHub issue breakdown for P2-3
```

## Comment

This document is intentionally narrow.

The backend foundation should become safer, cleaner, and easier to extend, but still must not begin ARI business feature implementation.

---

# 3. Scope

## 3.1 In Scope

P2-3 covers generic backend foundation work only:

```text
FastAPI application organization refinement
/api/v1 router foundation preservation
Health endpoint preservation
Common response envelope helper definitions
Common error class and error formatter definitions
Generic error code constants
Exception handler registration foundation
Application logging foundation
Request ID middleware foundation
CORS configuration foundation
Settings expansion for foundation-level config
Database session dependency placeholder
SQLAlchemy Base placeholder boundary
Repository base pattern
Service base pattern
Common schema pattern
Utility helpers
Foundation-only tests
Backend README update
Local smoke test update
AI coding guardrail updates if needed
GitHub issue breakdown for P2-3
```

## 3.2 Out of Scope

The following are not part of P2-3:

```text
Business feature APIs
Database schema migrations
Domain SQLAlchemy models
Auth implementation
RBAC implementation
MinIO upload implementation
Sync batch implementation
Mobile implementation
Web implementation
Production deployment
Pilot deployment
```

## 3.3 P2-3 Deliverable

The deliverable is a backend foundation specification that can guide coding agents and human developers to safely extend the P2-2 backend skeleton.

Target result after later implementation of P2-3:

```text
backend starts
health endpoints still work
foundation modules import cleanly
tests pass
no feature APIs exist
no migrations exist
no forbidden services exist
```

## Comment

P2-3 is not “feature implementation.”

It is “feature readiness.”

---

# 4. Source of Truth

## 4.1 Frozen Source Documents

P2-3 must follow these frozen documents:

```text
ARI V1 — P0 Domain Model Specification v1.0
ARI V1 — P0 Domain Model Additive Revision v1.1

ARI V1 — P0 Database Schema Specification v1.0
ARI V1 — P0 Database Schema Additive Revision v1.1

ARI V1 — P0 API Specification v1.0
ARI V1 — P0 API Specification Additive Revision v1.1

ARI V1 — P1-1 Backend Implementation Specification v1.0
ARI V1 — P1-2 Mobile App Implementation Specification v1.0
ARI V1 — P1-3 Web App Implementation Specification v1.0

ARI V1 — P2-1 Coding Execution Plan & Sprint Backlog v1.0
ARI V1 — P2-2 Monorepo & Local Development Setup v1.0
```

## 4.2 Current Coding Execution Authority

The direct coding execution authority for P2-3 is:

```text
ARI V1 — P2-1 Coding Execution Plan & Sprint Backlog v1.0
ARI V1 — P2-2 Monorepo & Local Development Setup v1.0
```

## 4.3 Frozen Architecture Rules

P2-3 must preserve:

```text
One Platform
One Backend
One Database Architecture
One Mobile App
One Web App
One Domain Model
One RBAC System
```

P2-3 must not introduce:

```text
Separate farmer app
Separate staff app
Separate admin backend
Separate web backend
New database architecture
New RBAC role
Permission service
Permission matrix engine
QR registry
Consultation entity
Owner registry
Farmer registry
Member registry
Block registry
Farm membership table
Knowledge graph
Vector database
RAG system
Internal AI assistant
Robot control module
Commerce module
Desktop app
Electron app
Flutter desktop app
```

## Comment

If a developer finds that a detail is missing, unclear, or inconsistent, the correct action is not to invent behavior.

The correct action is to create an API Gap / Revision Proposal.

---

# 5. Relationship to P2-1 and P2-2

## 5.1 Relationship to P2-1

P2-1 defines the coding execution order:

```text
1. Backend foundation
2. Database migrations
3. Auth and onboarding
4. Farm structure
5. Notebook / upload / sync
6. Mobile MVP
7. Web MVP
8. E2E test
9. Prototype deployment
10. Pilot
```

P2-3 corresponds to:

```text
Backend feature foundation
```

It is still before:

```text
Database migrations
Auth
Farm APIs
Notebook APIs
Mobile MVP
Web MVP
```

## 5.2 Relationship to P2-2

P2-2 created the local development foundation:

```text
ari/
├── backend/
├── mobile/
├── web/
├── infra/
├── docs/
├── scripts/
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
├── AGENTS.md
├── CLAUDE.md
└── CODEX.md
```

P2-2 confirmed local services:

```text
api
postgres
minio
emqx
```

P2-2 confirmed health endpoints:

```text
GET /health
GET /api/v1/health
```

P2-3 extends only the backend foundation created by P2-2.

## 5.3 P2-2 Health Contract Preserved

P2-3 must not break:

```text
GET /health
GET /api/v1/health
```

Expected response remains:

```json
{
  "status": "ok",
  "service": "ari-backend",
  "api": "/api/v1"
}
```

## Comment

P2-2 proved the local foundation works.

P2-3 must strengthen that foundation without starting business features early.

---

# 6. Non-Goals

P2-3 must not implement:

```text
Full database schema migrations
Actual Alembic migration files
Full authentication
Phone registration
Phone login
JWT token issuing
Refresh token flow
RBAC permission logic
User APIs
Organization APIs
Farm APIs
Zone APIs
Tree APIs
Notebook Entry APIs
Note Item APIs
Follow-Up APIs
Notification APIs
File upload flow
Upload queue
Sync batch
Mobile screens
Web pages
Production deployment
Pilot deployment
```

## 6.1 Explicit Deferrals

```text
Database and Alembic migrations → Deferred to P2-4
Auth and mobile onboarding → Deferred to P2-5
Farm structure backend → Deferred to P2-6
Notebook / upload / sync backend → Deferred to P2-7
Mobile MVP → Deferred to P2-8
Web MVP → Deferred to P2-9
E2E and prototype deployment → Deferred to P2-10
```

## Comment

P2-3 is a foundation layer.

If a file, endpoint, test, model, or service requires ARI business logic, it belongs to a later P2 document.

---

# 7. Backend Foundation Assumptions

## 7.1 Backend Stack

P2-3 assumes the backend stack remains:

```text
FastAPI
Python 3.12+
PostgreSQL / TimescaleDB
SQLAlchemy
Alembic
MinIO
EMQX
JWT Access Token / Refresh Token
Docker
/api/v1
```

## 7.2 Mobile Context

P2-3 must prepare for later mobile integration but not implement it.

Mobile context remains:

```text
Flutter
Android
iOS
Offline-first capture
Phone registration
Phone login
Upload queue
Sync batch
External Ask AI consultation flow
```

## 7.3 Web Context

P2-3 must prepare for later web integration but not implement it.

Web context remains:

```text
Browser-based Web App
Next.js / React / TypeScript recommended
Work Deep interface
No native desktop app
No Electron
No Flutter desktop
```

## 7.4 Deployment Direction

P2-3 follows the deployment direction already approved:

```text
Development = Local Docker Server
Pilot Prototype = Central Remote Server / Cloud VPS
Farm Local Server = Future Enhancement / Optional Hybrid Deployment
```

## Comment

P2-3 should improve local backend development quality only.

It must not introduce production deployment architecture.

---

# 8. Existing P2-2 Backend Baseline

P2-2 created the backend skeleton:

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       └── health.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   └── db/
│       ├── __init__.py
│       ├── base.py
│       └── session.py
├── alembic.ini
├── Dockerfile
├── pyproject.toml
├── requirements.txt
└── README.md
```

Existing P2-2 backend responsibilities:

```text
FastAPI app starts
Settings load from environment
GET /health works
GET /api/v1/health works
API v1 router exists
Database session placeholder exists
SQLAlchemy Base placeholder exists
Alembic placeholder exists
```

## Comment

P2-3 must build on this baseline.

It must not replace the baseline with a new backend structure.

---

# 9. P2-3 Allowed Changes

P2-3 may define or prepare generic foundation files only.

Allowed files:

```text
backend/app/core/errors.py
backend/app/core/logging.py
backend/app/core/response.py
backend/app/core/constants.py

backend/app/dependencies/db.py

backend/app/middleware/request_id.py

backend/app/schemas/common.py

backend/app/repositories/base.py

backend/app/services/base.py

backend/app/utils/datetime.py
backend/app/utils/uuid.py
backend/app/utils/pagination.py

backend/app/tests/test_health.py
backend/app/tests/test_app_startup.py
```

Allowed existing file updates:

```text
backend/app/main.py
backend/app/api/v1/router.py
backend/app/api/v1/health.py
backend/app/core/config.py
backend/app/db/base.py
backend/app/db/session.py
backend/README.md
backend/pyproject.toml
backend/requirements.txt
.env.example
AGENTS.md
CLAUDE.md
CODEX.md
```

Allowed only if needed:

```text
Add pytest as backend development dependency
Add httpx / TestClient-compatible dependency for backend tests
Add ruff / formatting guidance if already aligned with P2 coding guardrails
```

## Comment

Every allowed file must remain generic.

No ARI business feature logic may be placed in these files during P2-3.

---

# 10. P2-3 Forbidden Changes

## 10.1 Forbidden Feature Routers

Do not create:

```text
backend/app/api/v1/auth.py
backend/app/api/v1/users.py
backend/app/api/v1/organizations.py
backend/app/api/v1/farms.py
backend/app/api/v1/zones.py
backend/app/api/v1/trees.py
backend/app/api/v1/notebook_entries.py
backend/app/api/v1/note_items.py
backend/app/api/v1/follow_ups.py
backend/app/api/v1/notifications.py
backend/app/api/v1/upload_queue.py
backend/app/api/v1/files.py
backend/app/api/v1/sync.py
```

## 10.2 Forbidden Feature Models

Do not create:

```text
backend/app/models/user.py
backend/app/models/organization.py
backend/app/models/farm.py
backend/app/models/zone.py
backend/app/models/tree.py
backend/app/models/notebook_entry.py
backend/app/models/note_item.py
backend/app/models/follow_up.py
backend/app/models/notification.py
backend/app/models/upload_job.py
backend/app/models/role.py
```

## 10.3 Forbidden Services

Do not create:

```text
consultation_service.py
qr_registry_service.py
permission_service.py
knowledge_service.py
robot_service.py
commerce_service.py
```

## 10.4 Forbidden Folders

Do not create:

```text
apps/
services/
worker/
permission/
qr_registry/
consultation/
knowledge/
robot/
commerce/
rag/
vector/
```

## 10.5 Forbidden Database Changes

Do not create:

```text
new tables
real migration versions
seed data
domain SQLAlchemy models
feature repositories tied to frozen tables
feature services tied to domain rules
```

## 10.6 Forbidden Security / Enum Foundation Files In P2-3

Do not create in P2-3:

```text
backend/app/core/security.py
backend/app/core/enums.py
```

Reason:

```text
security.py belongs to JWT/auth implementation and is deferred to P2-5.

enums.py may become domain-specific and should be introduced with database/domain model implementation in P2-4 or later, not during generic foundation setup.
```

## Comment

P2-3 must be checked not only by what it creates, but also by what it does not create.

---

# 11. Backend Package Structure After P2-3

The target backend structure after P2-3 implementation should be:

```text
backend/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── router.py
│   │       └── health.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── errors.py
│   │   ├── logging.py
│   │   ├── response.py
│   │   └── constants.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── session.py
│   ├── dependencies/
│   │   ├── __init__.py
│   │   └── db.py
│   ├── middleware/
│   │   ├── __init__.py
│   │   └── request_id.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── common.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── base.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── base.py
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── datetime.py
│   │   ├── uuid.py
│   │   └── pagination.py
│   └── tests/
│       ├── __init__.py
│       ├── test_health.py
│       └── test_app_startup.py
├── alembic.ini
├── Dockerfile
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Comment

This structure intentionally excludes feature routers, feature schemas, feature models, feature repositories, and feature services.

Those belong to later P2 documents.

---

# 12. API v1 Router Foundation

## 12.1 Required Router Behavior

The `/api/v1` router must remain the single API v1 mount point.

Existing route:

```text
GET /api/v1/health
```

must remain active.

P2-3 may prepare router structure for future inclusion of feature routers, but must not import or register feature routers yet.

## 12.2 Allowed Router Foundation

Allowed:

```text
Keep api/v1/router.py as the central API v1 router
Keep api/v1/health.py registered
Keep API_V1_PREFIX from settings
Add comments showing future routers are deferred
```

## 12.3 Not Allowed

Do not register:

```text
auth router
users router
organizations router
farms router
zones router
trees router
notebook router
upload router
sync router
```

## Comment

P2-3 should make routing clean, not broader.

A router placeholder is acceptable.

A feature router is not.

---

# 13. Health Endpoint Preservation

P2-3 must preserve:

```text
GET /health
GET /api/v1/health
```

Expected response for both:

```json
{
  "status": "ok",
  "service": "ari-backend",
  "api": "/api/v1"
}
```

## 13.1 Health Endpoint Purpose

```text
GET /health
```

Purpose:

```text
Confirm FastAPI process is running.
```

```text
GET /api/v1/health
```

Purpose:

```text
Confirm /api/v1 router is mounted.
```

## 13.2 Health Endpoint / Database Reachability Boundary

P2-3 must preserve the existing P2-2 health response exactly.

P2-3 may prepare a database reachability helper or local test utility, but it must not:

```text
change the existing health response shape
require completed database schema migrations
require domain tables to exist
block /health or /api/v1/health because P2-4 migrations are not implemented yet
```

Full database health behavior and migration-aware database validation are deferred to P2-4.

## 13.3 Health Response Rule

Do not change the health response unless a documented reason exists.

If a change is required later, it must be handled through revision control.

## Comment

The health response is already proven by P2-2 smoke test.

Changing it in P2-3 creates unnecessary risk for no feature value.

---

# 14. Common Response Convention

P2-3 may define common response envelope helpers for future APIs.

The convention must align with the frozen P0 API style.

## 14.1 Success: Single Object

```json
{
  "data": {}
}
```

## 14.2 Success: List

```json
{
  "data": [],
  "pagination": {}
}
```

## 14.3 Error

```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid request"
  }
}
```

## 14.4 Allowed Foundation File

```text
backend/app/core/response.py
backend/app/schemas/common.py
```

## 14.5 Allowed Definitions

P2-3 may define:

```text
success_response helper
list_response helper
error_response helper
Pagination schema
Error schema
Generic response envelope schema
```

## 14.6 Not Allowed

Do not define feature response schemas yet, such as:

```text
UserResponse
FarmResponse
NotebookEntryResponse
UploadJobResponse
SyncBatchResponse
```

## Comment

P2-3 defines response shape, not business response content.

---

# 15. Common Error Handling Foundation

P2-3 may define a common error handling foundation.

## 15.1 Allowed Error Foundation

Allowed:

```text
AppError base class
Error code constants
Standard error response formatter
Exception handler registration
Request ID included in logs
Generic HTTP exception mapping
Generic validation error mapping
```

Allowed generic errors:

```text
validation_error
unauthorized
forbidden
not_found
conflict
internal_error
```

## 15.2 Error Response Shape

Generic error response should follow:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid request"
  }
}
```

Optional future-safe field:

```json
{
  "error": {
    "code": "validation_error",
    "message": "Invalid request",
    "request_id": "optional-request-id"
  }
}
```

If `request_id` is added to error responses in P2-3, it must remain generic and not expose sensitive data.

## 15.3 Allowed File

```text
backend/app/core/errors.py
```

## 15.4 Not Allowed

Do not implement feature-specific errors yet, such as:

```text
farm_not_found
tree_not_in_zone
phone_already_registered
notebook_entry_not_found
upload_already_completed
sync_conflict
membership_approval_required
```

These are deferred to later P2 documents.

## Comment

Common error handling improves consistency now.

Feature error semantics must wait until feature implementation.

---

# 16. Logging Foundation

P2-3 may define a basic logging foundation.

## 16.1 Allowed Logging

Allowed:

```text
LOG_LEVEL from environment
basic application logger
request ID logging support
startup log
shutdown log
health check log
unexpected exception log
```

Allowed file:

```text
backend/app/core/logging.py
```

## 16.2 Logging Requirements

Logs may include:

```text
request_id
method
path
status_code
latency_ms
error_code
```

Logs must not include:

```text
passwords
JWT access tokens
JWT refresh tokens
private keys
MinIO secret keys
sensitive media URLs
raw file contents
```

## 16.3 Not Allowed

Do not implement:

```text
external log shipping
advanced observability dashboard
audit log service
audit_logs table
SIEM integration
distributed tracing system
```

## Comment

P2-3 logging is for local development and debugging.

It is not an audit system.

---

# 17. CORS Foundation

P2-3 may configure CORS using environment variables.

## 17.1 Required Environment Variables

Use the P2-2 environment convention:

```text
CORS_ALLOW_ORIGINS
CORS_ALLOW_CREDENTIALS
```

Example local values:

```env
CORS_ALLOW_ORIGINS=http://localhost:3000,http://localhost:5173
CORS_ALLOW_CREDENTIALS=true
```

## 17.2 Allowed Behavior

Allowed:

```text
Parse comma-separated origins
Register FastAPI CORS middleware
Allow local web development origin
Allow local mobile / tool testing when needed
Keep defaults safe for local development
```

## 17.3 Not Allowed

Do not create:

```text
separate web backend
frontend proxy service
admin backend
staff backend
farmer backend
```

## Comment

CORS supports the one backend / one web app direction.

It must not become a reason to create another backend.

---

# 18. Request ID Middleware Foundation

P2-3 may add request ID middleware.

## 18.1 Purpose

```text
Improve debugging and traceability during backend development.
```

## 18.2 Allowed Behavior

Request ID middleware may:

```text
Read X-Request-ID if provided
Generate request_id if missing
Attach request_id to request state
Add X-Request-ID to response headers
Include request_id in logs
Include request_id in generic error response if approved
```

Allowed file:

```text
backend/app/middleware/request_id.py
```

## 18.3 Boundary

Request ID middleware is not:

```text
audit system
user tracking system
security event system
compliance system
```

## 18.4 Not Allowed

Do not create:

```text
audit_logs table
audit service
advanced tracing platform
user behavior analytics
```

## Comment

Request ID helps developers debug a request across logs.

It does not create a new data model.

---

# 19. Configuration Foundation

P2-3 may extend the existing settings foundation created in P2-2.

Allowed file:

```text
backend/app/core/config.py
```

## 19.1 Required Settings Groups

P2-3 settings may include:

```text
App settings
API settings
Database settings
CORS settings
Logging settings
Testing settings
```

## 19.2 Required Environment Variables

The backend should preserve and use:

```text
APP_NAME
APP_ENV
APP_DEBUG
API_V1_PREFIX
DATABASE_URL
CORS_ALLOW_ORIGINS
CORS_ALLOW_CREDENTIALS
LOG_LEVEL
LOG_FORMAT
```

## 19.3 Future Settings

Settings for the following may remain present as placeholders from P2-2 but must not activate feature logic:

```text
JWT settings
MinIO settings
EMQX settings
```

## 19.4 Not Allowed

Do not add real secrets.

Do not commit `.env`.

Do not introduce production deployment secrets.

Do not add feature-specific settings that imply early implementation.

## Comment

Configuration should make the backend predictable across local runs.

Feature-specific configuration becomes active only when that feature is implemented in later P2 documents.

---

# 20. Database Session Placeholder / Integration Boundary

P2-3 may prepare database session and dependency wiring.

Allowed files:

```text
backend/app/db/session.py
backend/app/dependencies/db.py
```

## 20.1 Allowed Database Foundation

Allowed:

```text
Read DATABASE_URL from settings
Create SQLAlchemy engine placeholder
Create sessionmaker placeholder
Define get_db dependency
Provide database reachability helper if needed
Use request-scoped session pattern
```

## 20.2 Session Lifecycle Pattern

The intended pattern remains:

```text
one session per request
commit only after service success
rollback on exception
close session after request
do not share session globally
```

## 20.3 P2-3 Boundary

P2-3 must not require real schema readiness.

P2-3 must not run migrations.

P2-3 must not seed data.

P2-3 must not implement feature repositories.

## 20.4 Deferral

```text
Database and Alembic migrations → Deferred to P2-4
```

## Comment

Database session wiring is allowed because later features will need it.

But P2-3 must not define ARI domain tables yet.

---

# 21. SQLAlchemy Base Boundary

P2-3 may preserve or cleanly define SQLAlchemy Base placeholder.

Allowed file:

```text
backend/app/db/base.py
```

## 21.1 Allowed

Allowed:

```text
Define Declarative Base placeholder
Expose Base for future models
Keep Base importable
Document that domain models are deferred
```

## 21.2 Not Allowed

Do not create domain models:

```text
User
Organization
Farm
Zone
Tree
NotebookEntry
NoteItem
FollowUp
Notification
UploadJob
Role
```

Do not create new tables.

Do not define table metadata for frozen domain tables yet.

## 21.3 Deferral

```text
Database and Alembic migrations → Deferred to P2-4
```

## Comment

SQLAlchemy Base may exist now.

SQLAlchemy model mapping must wait for the database migration phase.

---

# 22. Alembic Boundary

P2-3 may keep Alembic as a placeholder only.

## 22.1 Allowed

Allowed:

```text
Confirm alembic.ini exists
Document migration workflow for P2-4
Keep migration folders absent or empty if created by P2-2 placeholder
Do not create real migration versions
```

## 22.2 Not Allowed

Do not create:

```text
versions/001_create_users.py
versions/002_create_farms.py
versions/003_create_notebook_entries.py
```

Do not create any real migration file for:

```text
users
organizations
farms
zones
trees
notebook_entries
note_items
follow_ups
notifications
upload_queue
roles
```

## 22.3 Deferral

```text
Database and Alembic migrations → Deferred to P2-4
```

## Comment

Alembic belongs to the backend stack, but real schema migration belongs to P2-4.

---

# 23. Dependency Injection Foundation

P2-3 may define generic dependency foundation.

Allowed folder:

```text
backend/app/dependencies/
```

Allowed file:

```text
backend/app/dependencies/db.py
```

## 23.1 Allowed

Allowed:

```text
get_db dependency
future-safe dependency folder
generic dependency import pattern
```

## 23.2 Not Allowed

Do not create in P2-3:

```text
backend/app/dependencies/auth.py
backend/app/dependencies/rbac.py
backend/app/dependencies/scope.py
```

Auth dependency, RBAC dependency, and scope dependency implementation are deferred to P2-5 and later feature documents.

## 23.3 Deferral

```text
Auth and mobile onboarding → Deferred to P2-5
RBAC permission logic → Deferred to P2-5 and later feature documents
```

## Comment

Database dependency is foundation.

Auth / RBAC dependencies are feature behavior and must wait.

---

# 24. Repository Base Pattern

P2-3 must preserve the P1-1 backend layering:

```text
Router Layer
↓
Service Layer
↓
Repository Layer
↓
Database Layer
```

Allowed file:

```text
backend/app/repositories/base.py
```

## 24.1 Repository Layer Responsibility

Repository layer is responsible for:

```text
SQLAlchemy query construction
CRUD operations
Filtering
Pagination
Database constraint interaction
```

## 24.2 Allowed P2-3 Repository Base

P2-3 may define:

```text
BaseRepository pattern
Generic typing pattern if useful
Session injection pattern
Documentation comments for future repositories
```

## 24.3 Not Allowed

Do not create feature repositories:

```text
users.py
organizations.py
farms.py
zones.py
trees.py
notebook_entries.py
note_items.py
follow_ups.py
notifications.py
upload_jobs.py
```

Do not connect base repository to specific ARI domain tables.

## Comment

The base repository defines coding style.

It must not become a hidden feature implementation.

---

# 25. Service Base Pattern

Allowed file:

```text
backend/app/services/base.py
```

## 25.1 Service Layer Responsibility

Service layer is responsible for:

```text
Application rules
Frozen domain rules
Hierarchy validation
Transaction orchestration
Repository calls
External integration calls when allowed
```

## 25.2 Allowed P2-3 Service Base

P2-3 may define:

```text
BaseService pattern
Generic dependency injection pattern
Transaction boundary comments
Error handling conventions
```

## 25.3 Not Allowed

Do not create feature services:

```text
auth_service.py
user_service.py
organization_service.py
farm_service.py
zone_service.py
tree_service.py
notebook_service.py
note_item_service.py
follow_up_service.py
notification_service.py
upload_queue_service.py
file_service.py
sync_service.py
```

Do not create forbidden services:

```text
consultation_service.py
qr_registry_service.py
permission_service.py
knowledge_service.py
robot_service.py
commerce_service.py
```

## Comment

Service base pattern is allowed only as a template for later work.

No business rules should be implemented in P2-3.

---

# 26. Schema Common Pattern

Allowed file:

```text
backend/app/schemas/common.py
```

## 26.1 Allowed Common Schemas

Allowed:

```text
SuccessResponse
ListResponse
ErrorResponse
ErrorDetail
Pagination
HealthResponse if already consistent with P2-2
```

## 26.2 Common Pagination Shape

Future list APIs should use:

```json
{
  "data": [],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_records": 0,
    "total_pages": 0
  }
}
```

## 26.3 Not Allowed

Do not create feature schemas:

```text
AuthLoginRequest
RegisterRequest
UserResponse
FarmCreate
NotebookEntryCreate
NoteItemResponse
UploadUrlRequest
SyncBatchRequest
```

## Comment

Common schemas are shared language.

Feature schemas are deferred.

---

# 27. Utility Foundation

P2-3 may add utility helpers only if generic.

Allowed files:

```text
backend/app/utils/datetime.py
backend/app/utils/uuid.py
backend/app/utils/pagination.py
```

## 27.1 datetime.py

Allowed:

```text
UTC datetime helper
current UTC timestamp helper
ISO datetime helper
```

Not allowed:

```text
farm-specific timezone logic
seasonal calendar logic
follow-up scheduler logic
```

## 27.2 uuid.py

Allowed:

```text
UUID validation helper
UUID generation helper
```

Not allowed:

```text
Farm ID business rule
QR payload generation
Owner ID mapping
```

## 27.3 pagination.py

Allowed:

```text
page / page_size validation
offset calculation
pagination metadata helper
```

Not allowed:

```text
feature-specific filters
search logic
dashboard aggregation
```

## Comment

Utilities must stay boring and generic.

If a utility understands ARI business meaning, it is too early for P2-3.

---

# 28. Testing Foundation

P2-3 may add backend tests for foundation only.

Allowed test files:

```text
backend/app/tests/test_health.py
backend/app/tests/test_app_startup.py
```

## 28.1 Allowed Tests

Allowed tests:

```text
test app imports
test app startup
test GET /health
test GET /api/v1/health
test health response shape
test request ID header if middleware is added
test common response helper if simple and generic
test generic error formatter if simple and generic
```

## 28.2 Not Allowed Tests

Do not create tests for:

```text
auth
phone registration
phone login
JWT issuing
refresh token
RBAC
user APIs
organization APIs
farm APIs
zone APIs
tree APIs
notebook APIs
note item APIs
file upload
upload queue
sync batch
mobile screens
web pages
```

## 28.3 Test Dependency

If pytest is not yet available, P2-3 may add it as a backend development dependency.

Allowed:

```text
pytest
httpx or FastAPI TestClient-compatible dependency
```

## 28.4 Code Quality Foundation

P2-3 may define basic code quality expectations:

```text
Python imports must resolve
No unused feature modules
No forbidden folders
No forbidden services
Tests must run inside Docker api container
Health endpoints must still pass
```

Optional but allowed if already compatible:

```text
ruff check
basic formatting command
```

## Comment

Testing in P2-3 proves the foundation still works.

It does not prove ARI business behavior yet.

---

# 29. Backend README Update Requirements

`backend/README.md` must be updated for P2-3.

## 29.1 README Must Explain

```text
What P2-3 adds
What remains deferred
How to run backend locally
How to run health checks
How to run backend tests
Where common response / errors / logging live
Where request ID middleware lives
Where database dependency placeholder lives
What files are forbidden in P2-3
```

## 29.2 README Must Warn

README must clearly warn:

```text
Do not create feature APIs in P2-3
Do not create database migrations in P2-3
Do not create domain models in P2-3
Do not create auth / RBAC implementation in P2-3
Do not create upload / sync implementation in P2-3
Do not create mobile or web implementation in P2-3
```

## 29.3 README Must Include Smoke Test Commands

```bash
docker compose up -d --build
docker compose ps
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/health
docker compose exec api pytest
```

## Comment

The README is part of the guardrail system.

Coding agents should be able to read it and avoid expanding scope.

---

# 30. Docker / Local Workflow Update Requirements

P2-3 must preserve the P2-2 Docker stack:

```text
api
postgres
minio
emqx
```

## 30.1 Allowed Docker Changes

Allowed:

```text
Install test dependencies required for backend tests
Ensure pytest can run in api container
Ensure backend imports work inside container
Keep api service startup unchanged unless needed for foundation modules
```

## 30.2 Not Allowed Docker Changes

Do not add:

```text
worker service
scheduler service
separate auth service
separate upload service
separate web backend
separate admin backend
production deployment service
```

## 30.3 Local Workflow Must Still Work

Required commands:

```bash
docker compose up -d --build
docker compose ps
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/health
docker compose exec api pytest
```

## 30.4 AI Coding Guardrail Update

If P2-3 implementation modifies agent guardrail files, update only scope-specific warnings in:

```text
AGENTS.md
CLAUDE.md
CODEX.md
```

Allowed additions:

```text
P2-3 may create generic backend foundation files only
P2-3 must not create feature routers
P2-3 must not create domain models
P2-3 must not create migrations
P2-3 must not create forbidden services
P2-3 must not create core/security.py
P2-3 must not create core/enums.py
```

## Comment

Docker remains local development only.

P2-3 must not move the project toward deployment yet.

---

# 31. Smoke Test Checklist

P2-3 is complete only when:

```text
[ ] Docker stack still starts
[ ] api container starts
[ ] postgres container starts
[ ] minio container starts
[ ] emqx container starts
[ ] FastAPI backend still starts
[ ] GET /health still works
[ ] GET /api/v1/health still works
[ ] Health response remains unchanged
[ ] Backend tests pass
[ ] Common response foundation imports cleanly
[ ] Common error foundation imports cleanly
[ ] Logging foundation imports cleanly
[ ] Request ID middleware imports cleanly
[ ] Database dependency placeholder imports cleanly
[ ] Repository base imports cleanly
[ ] Service base imports cleanly
[ ] Common schemas import cleanly
[ ] No feature APIs are introduced
[ ] No database migrations are introduced
[ ] No domain models are introduced
[ ] No forbidden services are introduced
[ ] No forbidden database tables are introduced
[ ] No core/security.py is introduced
[ ] No core/enums.py is introduced
[ ] No mobile implementation begins
[ ] No web implementation begins
```

Example commands:

```bash
docker compose up -d --build
docker compose ps
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/health
docker compose exec api pytest
```

Expected health response:

```json
{
  "status": "ok",
  "service": "ari-backend",
  "api": "/api/v1"
}
```

## Comment

The smoke test must verify both positive and negative conditions.

P2-3 passes only if it works and remains within scope.

---

# 32. Acceptance Criteria

P2-3 can be accepted when all criteria below are met:

```text
[ ] Document scope matches P2-3 only
[ ] P2-1 and P2-2 authority is preserved
[ ] Latest Owner-confirmed P2-2 Frozen / Implemented / PASS status is recorded
[ ] Existing P2-2 backend baseline is preserved
[ ] /health is unchanged
[ ] /api/v1/health is unchanged
[ ] API v1 router remains mounted
[ ] Common response convention is defined
[ ] Common error handling foundation is defined
[ ] Logging foundation is defined
[ ] CORS foundation is defined
[ ] Request ID middleware foundation is defined
[ ] Configuration foundation is defined
[ ] Database session placeholder / integration boundary is defined
[ ] Health endpoint / database reachability boundary is clear
[ ] SQLAlchemy Base boundary is defined
[ ] Alembic boundary is defined
[ ] Dependency injection foundation is defined
[ ] Auth / RBAC dependency files are explicitly forbidden in P2-3
[ ] Repository base pattern is defined
[ ] Service base pattern is defined
[ ] Schema common pattern is defined
[ ] Utility foundation is defined
[ ] Testing foundation is defined
[ ] Backend README update requirements are defined
[ ] Docker/local workflow update requirements are defined
[ ] Smoke test checklist is defined
[ ] Git branch rules are defined
[ ] Commit message rules are defined
[ ] GitHub issue breakdown is limited to P2-3
[ ] What to create now is explicit
[ ] What not to create yet is explicit
[ ] API Gap / Revision Proposal handling is defined
[ ] No feature API is authorized
[ ] No database migration is authorized
[ ] No domain model is authorized
[ ] No forbidden service is authorized
[ ] No core/security.py is authorized
[ ] No core/enums.py is authorized
[ ] No mobile implementation is authorized
[ ] No web implementation is authorized
[ ] No production or pilot deployment is authorized
```

## Comment

Acceptance is based on foundation readiness, not feature completeness.

---

# 33. Git Branch Rules

## 33.1 Long-Lived Branches

```text
main
develop
```

## 33.2 P2-3 Working Branches

Recommended branches:

```text
feature/p2-3-backend-feature-foundation
feature/backend-common-foundation
chore/backend-test-foundation
docs/p2-3-backend-foundation
```

## 33.3 Branch Usage

```text
main
```

Stable branch only.

```text
develop
```

Integration branch for accepted P2 work.

```text
feature/p2-3-backend-feature-foundation
```

Main feature branch for P2-3 foundation work.

```text
feature/backend-common-foundation
```

Optional sub-branch for response / error / logging / middleware foundation.

```text
chore/backend-test-foundation
```

Optional sub-branch for pytest and foundation tests.

```text
docs/p2-3-backend-foundation
```

Documentation-only branch for P2-3 guide and README updates.

## 33.4 Merge Rule

P2-3 branches should merge into:

```text
develop
```

Only after:

```text
tests pass
smoke test passes
forbidden scope check passes
owner review if required
```

## Comment

Branch names must remain narrow so coding agents do not interpret P2-3 as permission to implement business APIs.

---

# 34. Commit Message Rules

## 34.1 Required Commit Sequence

Recommended commit sequence:

```text
1. chore(backend): prepare backend package foundation
2. feat(backend): add common response and error foundation
3. feat(backend): add request id and logging foundation
4. chore(backend): add backend foundation tests
5. docs: add P2-3 backend feature foundation guide
```

## 34.2 Commit Style

Use conventional commit style:

```text
chore(scope): message
feat(scope): message
fix(scope): message
docs: message
test(scope): message
refactor(scope): message
```

## 34.3 Allowed P2-3 Commit Scopes

```text
backend
docs
test
config
```

## 34.4 Forbidden P2-3 Commit Themes

Do not commit:

```text
feat(auth): ...
feat(farms): ...
feat(notebook): ...
feat(upload): ...
feat(sync): ...
feat(mobile): ...
feat(web): ...
feat(permission): ...
feat(qr-registry): ...
feat(knowledge): ...
feat(robot): ...
feat(commerce): ...
```

## Comment

Commit messages are another guardrail.

They should make scope violations obvious during review.

---

# 35. GitHub Issue Breakdown for P2-3

Create GitHub issues only for P2-3 scope.

## 35.1 Required Issues

```text
#1 Review P2-2 backend baseline before P2-3
#2 Add backend common response foundation
#3 Add backend common error foundation
#4 Add backend logging foundation
#5 Add request ID middleware foundation
#6 Add CORS configuration foundation
#7 Add database dependency placeholder
#8 Add repository base pattern
#9 Add service base pattern
#10 Add common schema pattern
#11 Add utility foundation
#12 Add backend foundation tests
#13 Update backend README for P2-3
#14 Update local smoke test checklist
#15 Run P2-3 smoke test and forbidden scope check
```

## 35.2 Suggested Labels

```text
p2-3
backend
foundation
docs
test
scope-guard
no-feature-api
```

## 35.3 Do Not Create P2-3 Issues For

```text
auth
phone registration
phone login
database migrations
farm APIs
zone APIs
tree APIs
notebook APIs
note item APIs
upload flow
sync batch
mobile screens
web pages
production deployment
```

## Comment

P2-3 issue breakdown must not pull later work into the current phase.

---

# 36. What to Create Now

P2-3 authorizes creating or updating only the following foundation items.

## 36.1 Create Generic Backend Foundation Files

```text
backend/app/core/errors.py
backend/app/core/logging.py
backend/app/core/response.py
backend/app/core/constants.py

backend/app/dependencies/__init__.py
backend/app/dependencies/db.py

backend/app/middleware/__init__.py
backend/app/middleware/request_id.py

backend/app/schemas/__init__.py
backend/app/schemas/common.py

backend/app/repositories/__init__.py
backend/app/repositories/base.py

backend/app/services/__init__.py
backend/app/services/base.py

backend/app/utils/__init__.py
backend/app/utils/datetime.py
backend/app/utils/uuid.py
backend/app/utils/pagination.py

backend/app/tests/__init__.py
backend/app/tests/test_health.py
backend/app/tests/test_app_startup.py
```

## 36.2 Update Existing Backend Files If Needed

```text
backend/app/main.py
backend/app/api/v1/router.py
backend/app/api/v1/health.py
backend/app/core/config.py
backend/app/db/base.py
backend/app/db/session.py
backend/README.md
backend/pyproject.toml
backend/requirements.txt
```

## 36.3 Update Root / Guardrail Files If Needed

```text
.env.example
AGENTS.md
CLAUDE.md
CODEX.md
README.md
```

## 36.4 Add Test Dependency If Needed

Allowed:

```text
pytest
httpx or FastAPI TestClient-compatible dependency
```

## Comment

This list is the positive allowlist.

Anything not on this list should be treated as out of scope unless explicitly approved.

---

# 37. What Not to Create Yet

Do not create feature implementation yet.

## 37.1 Do Not Create Feature Routers

```text
auth.py
users.py
organizations.py
farms.py
zones.py
trees.py
notebook_entries.py
note_items.py
follow_ups.py
notifications.py
upload_queue.py
files.py
sync.py
```

## 37.2 Do Not Create Domain Models

```text
models/user.py
models/organization.py
models/farm.py
models/zone.py
models/tree.py
models/notebook_entry.py
models/note_item.py
models/follow_up.py
models/notification.py
models/upload_job.py
models/role.py
```

## 37.3 Do Not Create Feature Services

```text
auth_service.py
user_service.py
organization_service.py
farm_service.py
zone_service.py
tree_service.py
notebook_service.py
note_item_service.py
follow_up_service.py
notification_service.py
upload_queue_service.py
file_service.py
sync_service.py
```

## 37.4 Do Not Create Forbidden Services

```text
consultation_service.py
qr_registry_service.py
permission_service.py
knowledge_service.py
robot_service.py
commerce_service.py
```

## 37.5 Do Not Create Database Artifacts

```text
migration versions
seed data
domain SQLAlchemy models
feature repositories tied to tables
new tables
```

## 37.6 Do Not Create Security / Enum Files Yet

```text
backend/app/core/security.py
backend/app/core/enums.py
```

Reason:

```text
security.py → Deferred to P2-5
enums.py → Deferred to P2-4 or later, when database/domain model implementation begins
```

## 37.7 Do Not Start Later P2 Work

```text
Database and Alembic migrations → Deferred to P2-4
Auth and mobile onboarding → Deferred to P2-5
Farm structure backend → Deferred to P2-6
Notebook / upload / sync backend → Deferred to P2-7
Mobile MVP → Deferred to P2-8
Web MVP → Deferred to P2-9
E2E and prototype deployment → Deferred to P2-10
```

## Comment

P2-3 must not become P2-4, P2-5, or P2-7 by accident.

---

# 38. API Gap / Revision Proposal Handling

If anything is missing, unclear, or inconsistent with frozen specs, do not invent behavior.

Create an API Gap / Revision Proposal.

## 38.1 Storage Location

Store API gap notes under:

```text
docs/api-gaps/
```

## 38.2 Required Template

```markdown
# API Gap / Revision Proposal

Gap ID:
API-GAP-000X

Title:
<short title>

Discovered In:
P2-3 Backend Feature Foundation

Related Frozen Document:
<document name>

Current Frozen Behavior:
<what frozen spec currently says>

Missing / Ambiguous Detail:
<what is missing or unclear>

Impact:
<why this matters>

Proposed Handling:
<option A / option B / defer>

Scope Risk:
Does this introduce new architecture?
Does this introduce a new entity?
Does this introduce a new database table?
Does this introduce a new RBAC role?

Recommendation:
<recommended action>

Status:
Draft / Owner Review / Approved / Rejected
```

## 38.3 P2-3 Expected API Gaps

P2-3 should not normally create API gaps because it does not implement feature APIs.

Potential gaps in P2-3 are likely to be foundation-only naming or convention issues, such as:

```text
CORS environment variable naming mismatch
Error envelope optional request_id placement
Test dependency location
```

If a gap affects feature behavior, defer it to the relevant later P2 document.

## 38.4 Existing Known Future API Gaps From P2-1

Do not resolve these in P2-3.

They remain later-phase concerns:

```text
auth/me missing farmer_status / membership_status / account_status / primary_farm_id
GET /api/v1/users missing membership_status filter
PATCH /api/v1/users/{user_id} missing membership status transition behavior
Notebook review status transition missing
Knowledge Candidate status representation missing
Media read URL missing for Web viewer
Dashboard aggregate endpoint missing
```

## Comment

API Gap handling protects frozen documents from silent mutation.

---

# 39. Freeze Readiness Checklist

P2-3 is ready for owner freeze review when:

```text
[ ] Document control is complete
[ ] Latest Owner-confirmed P2-2 status is clarified
[ ] Purpose is clear
[ ] Scope is limited to backend feature foundation
[ ] Source of Truth list is complete
[ ] Relationship to P2-1 and P2-2 is clear
[ ] Non-goals are explicit
[ ] Backend foundation assumptions are defined
[ ] Existing P2-2 backend baseline is preserved
[ ] P2-3 allowed changes are explicit
[ ] P2-3 forbidden changes are explicit
[ ] backend/app/core/security.py is forbidden in P2-3
[ ] backend/app/core/enums.py is forbidden in P2-3
[ ] Backend package structure after P2-3 is defined
[ ] API v1 router foundation is defined
[ ] Health endpoint preservation is defined
[ ] Health endpoint / database reachability boundary is clear
[ ] Common response convention is defined
[ ] Common error handling foundation is defined
[ ] Logging foundation is defined
[ ] CORS foundation is defined
[ ] Request ID middleware foundation is defined
[ ] Configuration foundation is defined
[ ] Database session placeholder / integration boundary is defined
[ ] SQLAlchemy Base boundary is defined
[ ] Alembic boundary is defined
[ ] Dependency injection foundation is defined
[ ] Auth / RBAC / scope dependencies are forbidden in P2-3
[ ] Repository base pattern is defined
[ ] Service base pattern is defined
[ ] Schema common pattern is defined
[ ] Utility foundation is defined
[ ] Testing foundation is defined
[ ] Backend README update requirements are defined
[ ] Docker/local workflow update requirements are defined
[ ] Smoke test checklist is defined
[ ] Acceptance criteria are defined
[ ] Git branch rules are defined
[ ] Commit message rules are defined
[ ] GitHub issue breakdown is limited to P2-3
[ ] What to create now is explicit
[ ] What not to create yet is explicit
[ ] API Gap / Revision Proposal handling is defined
[ ] No feature API is authorized
[ ] No database migration is authorized
[ ] No domain model is authorized
[ ] No forbidden service is authorized
[ ] No mobile implementation is authorized
[ ] No web implementation is authorized
[ ] No production or pilot deployment is authorized
```

---

# Final P2-3 Boundary Statement

P2-3 authorizes only backend foundation work.

P2-3 authorizes:

```text
backend package organization
common response foundation
common error foundation
logging foundation
CORS foundation
request ID middleware foundation
configuration foundation
database dependency placeholder
SQLAlchemy Base placeholder boundary
repository base pattern
service base pattern
common schemas
generic utilities
foundation tests
backend README update
local smoke test update
AI coding guardrail update if needed
```

P2-3 does not authorize:

```text
database schema migrations
auth implementation
phone registration
phone login
JWT issuing
RBAC logic
user APIs
organization APIs
farm APIs
zone APIs
tree APIs
notebook APIs
note item APIs
follow-up APIs
notification APIs
file upload
upload queue
sync batch
mobile screens
web pages
production deployment
pilot deployment
new architecture
new services
new entities
new database tables
new RBAC roles
backend/app/core/security.py
backend/app/core/enums.py
```

After P2-3 is reviewed and frozen, the next document should be:

```text
ARI V1 — P2-4 Database and Alembic Migration Foundation v1.0
```

Status:

```text
ARI V1 — P2-3 Backend Feature Foundation v1.0
Status: Draft Final / Ready for Owner Freeze
```

**********************************************
ARI V1 — P2-3 Backend Feature Foundation v1.0
Status: FROZEN by owner
**********************************************
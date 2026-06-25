# ARI V1 — P2-1 Coding Execution Plan & Sprint Backlog v1.0

Project: ARI — Agricultural Intelligence Platform
Phase: P2 Coding Execution
Document Number: P2-1
Document Type: Coding Execution Plan + Sprint Backlog + Cross-Check Comments
Status: FROZEN
Freeze Status: FROZEN FOR CODING EXECUTION
Prepared From: Frozen Library / Project ARIS Files
Coding Direction: Backend First → Mobile MVP → Web MVP → E2E → Prototype Server → Real Pilot

---

# 0. Document Purpose

This document defines the coding execution plan for ARI V1 small real-world prototype.

It combines:

```text
1. Coding assumptions
2. Frozen document cross-check comments
3. Corrected monorepo structure
4. Environment setup
5. Sprint plan
6. Backend backlog
7. Database backlog
8. Mobile backlog
9. Web backlog
10. Testing backlog
11. Deployment backlog
12. Acceptance criteria
13. GitHub issue breakdown
14. What to code first
15. What not to code yet
16. API Gap / Revision Proposal list
```

## Comment

This document is not a redesign document.

It is a coding execution document.

The purpose is to prevent developers from accidentally adding new architecture while coding.

Every section below includes implementation comments to explain why that section is included, limited, or delayed.

---

# 1. Source of Truth

## 1.1 Frozen Documents Used

The following documents are treated as Source of Truth for this coding execution plan:

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
```

## Comment

This section is intentionally placed before the sprint plan.

Reason:

```text
Coding must follow frozen documents.
Developers must not treat sprint backlog as permission to invent missing tables, endpoints, services, or roles.
```

If coding reaches a missing detail, mark it as:

```text
API Gap / Revision Proposal
```

Do not silently implement a new system.

---

# 2. Frozen Architecture Rules

## 2.1 Must Preserve

```text
One Platform
One Backend
One Database Architecture
One Mobile App
One Web App
One Domain Model
One RBAC System
```

## 2.2 Must Not Introduce

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

This is the highest-level guardrail for coding.

A developer may create folders, modules, services, and components only inside the approved backend/mobile/web applications.

But the following are not allowed:

```text
new backend service
new microservice
new domain entity
new database table outside frozen schema
new user role
new permission engine
```

Example:

```text
Allowed:
backend/app/services/notebook_service.py

Not allowed:
backend/app/services/consultation_service.py
```

Reason:

```text
Consultation is Notebook Entry Type, not a separate entity/service boundary.
```

---

# 3. Cross-Check Result Summary

## 3.1 Corrected From Previous Draft

The previous draft required correction in these areas:

```text
1. Repo structure must align with backend/, mobile/, web/
2. Docker local stack must include EMQX because P1-1 includes it
3. Upload endpoints must use frozen API names
4. Follow-Up is an allowed entity/table/module
5. Consultation must not become a separate entity/module/service/router
6. QR must remain representation only
7. Knowledge Candidate and Knowledge Library must be Web views/workflows over Notebook Entries
8. Pending member approval must use users + membership_status
9. Farm membership table must not be created
10. Mobile MVP should follow backend core and come before full Web MVP
```

## 3.2 Safe To Code

```text
backend/
mobile/
web/

FastAPI
SQLAlchemy
Alembic
PostgreSQL / TimescaleDB
MinIO
EMQX in local Docker stack
JWT access token / refresh token
Phone registration
Phone login
Organization / User / Farm / Zone / Tree APIs
Notebook Entry APIs
Note Item APIs
Follow-Up APIs
Notification APIs
Upload Queue APIs
File upload via MinIO
Sync batch
Flutter Android/iOS mobile app
Browser-based Web App
```

## 3.3 Must Be API Gap / Revision Proposal If Missing

```text
auth/me missing farmer_status / membership_status / account_status / primary_farm_id
GET /api/v1/users missing membership_status filter
PATCH /api/v1/users/{user_id} missing membership status transition behavior
Notebook review status transition missing
Knowledge Candidate status representation missing
Media read URL missing for Web viewer
Dashboard aggregate endpoint missing
```

## 3.4 Do Not Code

```text
qr_registry table
consultations table
farm_memberships table
reviews table
knowledge table
audit_logs table
permissions table
owner registry
member registry
farmer registry
block registry
internal AI assistant
RAG
vector database
knowledge graph
commerce
robot control
desktop app
Electron app
Flutter desktop app
```

## Comment

This is the main cross-check result.

The plan is allowed to proceed only if developers treat this section as execution law.

When in doubt:

```text
Prefer smaller implementation.
Use existing entities.
Use existing endpoints.
Mark missing capability as API Gap.
```

---

# 4. Coding Assumptions

## 4.1 Prototype Principle

```text
Build small real-world prototype first.
Use with real pilot users.
Collect real data.
Review actual problems.
Improve in later phase.
```

## Comment

This prevents the coding phase from expanding into full ARI platform too early.

P2 coding is not the time to build:

```text
full intelligence layer
robot integration
commerce
advanced dashboard
knowledge graph
internal AI assistant
```

---

## 4.2 Deployment Assumption

```text
Development = Local Docker Server
Pilot Prototype = Central Remote Server / Cloud VPS
Farm Local Server = Future Enhancement / Optional Hybrid Deployment
```

## Comment

Do not build farm local server in P2-1.

Reason:

```text
P2 prototype should validate the product with a central remote server first.
Farm local server is useful later but will add deployment complexity too early.
```

---

## 4.3 Backend First Assumption

Coding order:

```text
1. Backend foundation
2. Database migrations
3. Auth and onboarding
4. Core farm structure
5. Notebook/upload/sync
6. Mobile MVP
7. Web MVP
8. E2E test
9. Prototype deployment
10. Pilot
```

## Comment

Mobile and Web depend on the same `/api/v1`.

If Mobile or Web is coded first without backend contract, the project will likely duplicate models and rewrite screens later.

Backend-first does not mean finishing the whole backend before mobile.

It means creating enough stable backend core before mobile begins.

---

# 5. Corrected Monorepo Structure

## 5.1 Repository Root

Recommended root:

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
└── README.md
```

## Comment

This corrects the earlier draft that used `apps/backend`.

The frozen implementation documents define the implementation roots as:

```text
backend/
mobile/
web/
```

Therefore the coding repo should use those folders directly.

This avoids confusion between spec and implementation.

---

## 5.2 Backend Structure

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
│   │       ├── auth.py
│   │       ├── users.py
│   │       ├── organizations.py
│   │       ├── farms.py
│   │       ├── zones.py
│   │       ├── trees.py
│   │       ├── notebook_entries.py
│   │       ├── note_items.py
│   │       ├── follow_ups.py
│   │       ├── notifications.py
│   │       ├── upload_queue.py
│   │       ├── files.py
│   │       └── sync.py
│   ├── core/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── security.py
│   │   ├── enums.py
│   │   ├── errors.py
│   │   └── logging.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── session.py
│   │   └── migrations/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user.py
│   │   ├── organization.py
│   │   ├── farm.py
│   │   ├── zone.py
│   │   ├── tree.py
│   │   ├── notebook_entry.py
│   │   ├── note_item.py
│   │   ├── follow_up.py
│   │   ├── notification.py
│   │   ├── upload_job.py
│   │   └── role.py
│   ├── schemas/
│   ├── repositories/
│   ├── services/
│   ├── dependencies/
│   ├── middleware/
│   ├── utils/
│   └── tests/
├── alembic.ini
├── Dockerfile
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Comment

Backend must use layered architecture:

```text
Router → Service → Repository → Database
```

Do not put SQL directly in routers.

Do not put business rules directly in routers.

Do not create:

```text
consultation_service.py
qr_registry_service.py
permission_service.py
knowledge_service.py
robot_service.py
commerce_service.py
```

---

## 5.3 Mobile Structure

```text
mobile/
├── pubspec.yaml
├── analysis_options.yaml
├── README.md
├── lib/
│   ├── main.dart
│   ├── app.dart
│   ├── core/
│   ├── shared/
│   ├── features/
│   │   ├── auth/
│   │   ├── onboarding/
│   │   ├── home/
│   │   ├── farm_context/
│   │   ├── farm_setup/
│   │   ├── notebook/
│   │   ├── ask_ai/
│   │   ├── media_capture/
│   │   ├── notifications/
│   │   ├── follow_ups/
│   │   ├── qr/
│   │   ├── upload_queue/
│   │   └── profile/
│   └── generated/
├── test/
├── android/
└── ios/
```

## Comment

There is only one Flutter mobile app.

Allowed:

```text
features/auth
features/notebook
features/upload_queue
features/ask_ai
features/qr
```

Not allowed:

```text
farmer_app/
staff_app/
desktop_app/
web_app/
```

The `qr/` feature is allowed only for scan/display helper UI.

It must not create:

```text
QR registry
QR entity
QR service boundary
```

---

## 5.4 Web Structure

```text
web/
├── package.json
├── tsconfig.json
├── next.config.js
├── README.md
├── .env.example
├── public/
├── src/
│   ├── app/
│   │   ├── login/
│   │   ├── dashboard/
│   │   ├── farms/
│   │   ├── notebook/
│   │   ├── review/
│   │   ├── knowledge-candidates/
│   │   ├── knowledge-library/
│   │   ├── follow-ups/
│   │   ├── notifications/
│   │   ├── administration/
│   │   └── settings/
│   ├── core/
│   │   ├── api/
│   │   ├── auth/
│   │   ├── config/
│   │   ├── rbac/
│   │   ├── i18n/
│   │   └── utils/
│   ├── features/
│   ├── shared/
│   └── tests/
└── Dockerfile
```

## Comment

Web App is browser-based only.

It must not become:

```text
Electron app
native desktop app
separate admin frontend
separate staff frontend
separate farmer frontend
separate web backend
```

Knowledge Candidate and Knowledge Library are allowed as Web views only.

They must use existing Notebook Entries and statuses.

They must not create:

```text
knowledge table
knowledge asset service
case library entity
knowledge graph
RAG
vector database
```

---

# 6. Environment Setup

## 6.1 Required Local Tools

```text
Git
Docker
Docker Compose
Python 3.12+
Node.js LTS
Flutter stable
PostgreSQL client tools
```

## Comment

The project should be runnable locally before cloud deployment.

Do not require production server setup before local smoke test works.

---

## 6.2 Local Docker Stack

Required services:

```text
backend API
PostgreSQL / TimescaleDB
MinIO
EMQX
```

Recommended Docker Compose service names:

```text
api
postgres
minio
emqx
```

Optional local tools:

```text
pgadmin
minio-console
```

## Comment

EMQX is included because it is part of the frozen backend stack.

However, P2 must not build robot services or microservice messaging architecture.

Allowed P0-compatible MQTT events:

```text
upload.completed
sync.completed
notification.created
```

---

## 6.3 Root .env.example

```text
APP_ENV=local
APP_NAME=ARI Backend
API_V1_PREFIX=/api/v1

DATABASE_URL=postgresql+psycopg://ari:ari_dev_password@postgres:5432/ari

JWT_SECRET_KEY=change_me
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=30

MINIO_ENDPOINT=minio:9000
MINIO_ACCESS_KEY=ari_minio
MINIO_SECRET_KEY=ari_minio_password
MINIO_BUCKET=ari-media
MINIO_SECURE=false

MQTT_HOST=emqx
MQTT_PORT=1883
MQTT_USERNAME=ari
MQTT_PASSWORD=ari_mqtt_password

CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
LOG_LEVEL=INFO
```

## Comment

Use one central configuration pattern.

Do not hard-code credentials in code.

Do not commit real production secrets.

---

# 7. Sprint Plan

## Sprint 0 — Monorepo + Local Foundation

Goal:

```text
Create runnable repository foundation.
```

Tasks:

```text
SP0-001 Create root repo structure
SP0-002 Add README
SP0-003 Add .env.example
SP0-004 Add docker-compose.yml
SP0-005 Add backend skeleton
SP0-006 Add health endpoints
SP0-007 Add local startup script
SP0-008 Add GitHub issue labels
```

Acceptance:

```text
docker compose up starts postgres, minio, emqx, backend
GET /health works
GET /api/v1/health works
backend can read environment settings
```

## Comment

Sprint 0 should not implement business features.

The only goal is to prove the development environment works.

---

## Sprint 1 — Database + Alembic Foundation

Goal:

```text
Create frozen schema foundation and additive v1.1 migration.
```

Tasks:

```text
SP1-001 Initialize Alembic
SP1-002 Create SQLAlchemy Base
SP1-003 Create database session
SP1-004 Create enum definitions
SP1-005 Create frozen P0 base tables
SP1-006 Add P0 v1.1 user fields
SP1-007 Add optional farms.location JSONB if approved in schema
SP1-008 Add indexes and constraints
SP1-009 Add migration test
```

Acceptance:

```text
Empty database can migrate successfully
Models map to frozen tables
No forbidden table exists
Rollback/dev reset works locally
```

## Comment

This sprint is where accidental scope expansion usually happens.

Do not create missing tables to make features easier.

Specifically do not create:

```text
consultations
qr_registry
farm_memberships
reviews
knowledge
audit_logs
permissions
```

---

## Sprint 2 — Auth + Onboarding Backend

Goal:

```text
Implement phone registration/login and user lifecycle.
```

Tasks:

```text
SP2-001 Password hashing
SP2-002 JWT access token
SP2-003 JWT refresh token
SP2-004 Phone normalization
SP2-005 POST /api/v1/auth/register
SP2-006 POST /api/v1/auth/login using phone
SP2-007 POST /api/v1/auth/refresh
SP2-008 GET /api/v1/auth/me
SP2-009 Account status guard
SP2-010 Membership status guard
SP2-011 Owner registration creates/assigns organization
SP2-012 Owner family/farm staff Farm ID join flow
SP2-013 Pending farm approval support via users table
```

Acceptance:

```text
Owner can register by phone
Owner gets organization_id
Owner can login
Owner family/farm staff can register with Farm ID
Farm ID resolves organization_id
membership_status=pending_farm_approval for owner_family/farm_staff
Tokens are returned after successful registration
/auth/me returns required user state
```

## Comment

farmer_status is not RBAC.

Use:

```text
role = farmer
farmer_status = owner | owner_family | farm_staff
```

Do not create:

```text
owner role
owner_family role
farm_staff role
member registry
farm membership table
```

---

## Sprint 3 — Organization / Farm / Zone / Tree Backend

Goal:

```text
Implement physical farm hierarchy and context selection.
```

Tasks:

```text
SP3-001 Organizations API
SP3-002 Users API
SP3-003 Farms API
SP3-004 Zones API
SP3-005 Trees API
SP3-006 Farm hierarchy validation
SP3-007 Owner may create multiple farms
SP3-008 owner_family/farm_staff cannot create Farm/Zone/Tree before approval
SP3-009 Optional QR payload endpoints if approved
```

Acceptance:

```text
Farm belongs to Organization
Zone belongs to Farm
Tree belongs to Zone
Owner can create multiple farms under own organization
Farm/Zone/Tree APIs enforce backend authorization
QR payload is generated from existing ID only if implemented
```

## Comment

QR is representation only.

Allowed:

```text
GET /api/v1/farms/{farm_id}/qr
GET /api/v1/zones/{zone_id}/qr
GET /api/v1/trees/{tree_id}/qr
```

Not allowed:

```text
qr_registry table
qr_registry model
qr_registry service
```

---

## Sprint 4 — Notebook / Note Items / Follow-Ups / Notifications Backend

Goal:

```text
Implement Digital Farm Notebook core.
```

Tasks:

```text
SP4-001 Create Notebook Entry
SP4-002 List Notebook Entries
SP4-003 Get Notebook Entry Detail
SP4-004 Update Notebook Entry
SP4-005 Archive Notebook Entry
SP4-006 Create Note Item
SP4-007 List Note Items by Entry
SP4-008 Update Note Item
SP4-009 sequence_order validation
SP4-010 Consultation as Notebook Entry Type
SP4-011 Follow-Up create/list/update outcome
SP4-012 Notifications list/read/mark-all-read
SP4-013 Keyword search only
```

Acceptance:

```text
Notebook Entry works as Note Session
Note Items preserve timeline order
Supported item types: photo/video/voice/text/file/link
Consultation uses entry_type=consultation
Follow-Up supports 3/7/14 days
Outcomes support improved/same/worse/unknown
Keyword search works without vector/RAG/LLM search
```

## Comment

Important correction from earlier draft:

```text
Follow-Up is allowed as its own frozen domain/table/module.
Consultation is not.
```

Therefore:

```text
Allowed:
follow_up.py
follow_up_service.py
api/v1/follow_ups.py

Not allowed:
consultation.py
consultation_service.py
api/v1/consultations.py
```

Consultation logic belongs inside notebook entry logic.

---

## Sprint 5 — File Upload / Upload Queue / Offline Sync Backend

Goal:

```text
Implement media upload and offline synchronization.
```

Tasks:

```text
SP5-001 MinIO client
SP5-002 Object key generation
SP5-003 POST /api/v1/files/upload-url
SP5-004 POST /api/v1/files/complete
SP5-005 POST /api/v1/files/upload-failed
SP5-006 Upload queue create/list/update/retry
SP5-007 POST /api/v1/sync/batch
SP5-008 client_id idempotency
SP5-009 Conflict handling
SP5-010 Sync result mapping
```

Acceptance:

```text
Client can request upload URL
Client can upload to MinIO
Client can complete upload
Upload queue status updates correctly
Sync batch creates records idempotently
Duplicate client_id does not create duplicate records
```

## Comment

Endpoint names must follow frozen API.

Use:

```text
POST /api/v1/files/upload-url
POST /api/v1/files/complete
POST /api/v1/files/upload-failed
POST /api/v1/sync/batch
```

Do not invent:

```text
/files/presign-upload
/files/confirm-upload
/media/upload
/upload/presign
```

---

## Sprint 6 — Backend Tests + API Stabilization

Goal:

```text
Stabilize backend before mobile implementation.
```

Tasks:

```text
SP6-001 Unit tests
SP6-002 Repository tests
SP6-003 Service tests
SP6-004 API tests
SP6-005 Integration tests with PostgreSQL
SP6-006 Integration tests with MinIO
SP6-007 Sync idempotency tests
SP6-008 Auth lifecycle tests
SP6-009 Forbidden table/module audit
```

Acceptance:

```text
Core backend tests pass
Database migration test passes
No forbidden modules/tables exist
Swagger/OpenAPI usable for mobile and web developers
```

## Comment

Testing should verify not only what exists, but also what must not exist.

Example test/audit:

```text
No consultations table
No qr_registry table
No permission service
No farm_memberships table
```

---

## Sprint 7 — Mobile MVP

Goal:

```text
Build the capture-first Flutter app for Android/iOS.
```

Tasks:

```text
SP7-001 Create Flutter app
SP7-002 Environment config
SP7-003 API client
SP7-004 Secure token storage
SP7-005 Phone registration screen
SP7-006 Phone login screen
SP7-007 Farmer status selection
SP7-008 Pending approval screen
SP7-009 First-time permission setup
SP7-010 Home screen
SP7-011 Farm selector
SP7-012 Create Farm for owner
SP7-013 Add Note flow
SP7-014 Media capture
SP7-015 Local storage
SP7-016 Upload queue
SP7-017 Sync batch
SP7-018 External Ask AI flow
SP7-019 Follow-up outcome capture
SP7-020 Notifications screen
```

Acceptance:

```text
Android build works
iOS build works
User can register/login by phone
Owner can create farm
owner_family/farm_staff can wait for approval
User can capture notebook entry offline
User can add photo/video/voice/text/file/link
User can upload later
External Ask AI flow saves learned_summary
Follow-up outcome can be recorded
```

## Comment

Mobile is the main capture tool.

The app must preserve:

```text
Save Local ≠ Upload ≠ Analyze
```

Do not implement:

```text
internal AI assistant
AI diagnosis
object detection
speech-to-text pipeline
robot control
commerce
web app features
desktop app
```

---

## Sprint 8 — Web MVP

Goal:

```text
Build browser-based Work Deep interface.
```

Tasks:

```text
SP8-001 Create Next.js/React/TypeScript app
SP8-002 Environment config
SP8-003 API client wrapper
SP8-004 Phone login
SP8-005 Current user restore
SP8-006 RBAC navigation visibility
SP8-007 Dashboard
SP8-008 Farm list
SP8-009 Farm detail
SP8-010 Notebook list
SP8-011 Notebook entry detail
SP8-012 Media viewer
SP8-013 Review / Approval Queue
SP8-014 Follow-ups
SP8-015 Notifications
SP8-016 Administration users
SP8-017 Organizations
SP8-018 Pending members if backend supports users filter/patch
SP8-019 Knowledge Candidates as notebook view
SP8-020 Knowledge Library as notebook view
SP8-021 Search workspace using keyword/filter search
SP8-022 Simulator/field collection filter if supported
```

Acceptance:

```text
Browser web app runs
Uses existing /api/v1 only
No separate web backend
Phone login works
Farm list/detail works
Notebook review works
Media viewer uses backend-approved URL only
Pending member approval works if backend supports it
Knowledge Candidate is a view over notebook entries
Knowledge Library is a view over notebook entries
```

## Comment

Web is Work Deep.

It is not offline-first capture.

It must not directly access MinIO without backend-approved URL.

It must not create:

```text
admin backend
knowledge service
review table
knowledge table
permission service
desktop app
```

---

## Sprint 9 — End-to-End Integration

Goal:

```text
Validate real user flow from registration to review.
```

E2E flows:

```text
SP9-001 Owner registers
SP9-002 Owner creates farm
SP9-003 Farm staff registers by Farm ID
SP9-004 Admin/ARI staff approves membership
SP9-005 Mobile captures note offline
SP9-006 Mobile uploads note/media
SP9-007 Web reviews notebook entry
SP9-008 External Ask AI learned_summary saved
SP9-009 Follow-up scheduled
SP9-010 Follow-up outcome recorded
SP9-011 Notification shown/read
```

Acceptance:

```text
One backend supports mobile and web
One database stores shared data
Mobile capture appears in Web review
Auth and membership rules are enforced
No forbidden architecture is introduced
```

## Comment

This sprint is where prototype becomes real.

Do not add new architecture to fix integration problems.

If an endpoint or field is missing, record API Gap / Revision Proposal.

---

## Sprint 10 — Prototype Server Deployment

Goal:

```text
Deploy small prototype to central remote server / cloud VPS.
```

Tasks:

```text
SP10-001 Prepare server
SP10-002 Install Docker
SP10-003 Configure production-like .env
SP10-004 Deploy backend
SP10-005 Deploy PostgreSQL/TimescaleDB
SP10-006 Deploy MinIO
SP10-007 Deploy EMQX
SP10-008 Deploy Web App
SP10-009 Configure HTTPS
SP10-010 Configure database backup
SP10-011 Configure MinIO backup
SP10-012 Smoke test
SP10-013 Pilot readiness checklist
```

Acceptance:

```text
Remote server reachable
Backend health works
Web app works
Mobile app connects to remote API
Upload works
Backup procedure documented
Pilot users can start
```

## Comment

Do not deploy farm local server in this sprint.

Farm local server remains Future Enhancement / Optional Hybrid Deployment.

---

# 8. Backend Task Backlog

## 8.1 Backend Foundation

```text
BE-001 Create backend folder
BE-002 Create FastAPI app
BE-003 Add /health
BE-004 Add /api/v1/health
BE-005 Add app/core/config.py
BE-006 Add app/core/security.py
BE-007 Add app/core/enums.py
BE-008 Add app/core/errors.py
BE-009 Add logging middleware
BE-010 Add request ID middleware
BE-011 Add API v1 router
BE-012 Add CORS config
BE-013 Add Dockerfile
```

## Comment

Health check must verify at least API and database reachability.

MinIO and EMQX health checks may be optional at first.

---

## 8.2 Auth / Onboarding

```text
BE-014 Password hashing
BE-015 Phone normalization
BE-016 User lookup by phone
BE-017 POST /api/v1/auth/register
BE-018 POST /api/v1/auth/login
BE-019 POST /api/v1/auth/refresh
BE-020 POST /api/v1/auth/logout
BE-021 GET /api/v1/auth/me
BE-022 JWT access token
BE-023 JWT refresh token
BE-024 Account status validation
BE-025 Membership status validation
BE-026 Owner registration flow
BE-027 Owner family registration flow
BE-028 Farm staff registration flow
```

## Comment

Registration must assign:

```text
role = farmer
```

Do not create new RBAC roles.

---

## 8.3 User / Organization / Farm Structure

```text
BE-029 Organizations CRUD
BE-030 Users list/detail/update
BE-031 Farm CRUD
BE-032 Zone CRUD
BE-033 Tree CRUD
BE-034 Farm hierarchy validation
BE-035 Zone hierarchy validation
BE-036 Tree hierarchy validation
BE-037 Farm ID / farm_code lookup for join
BE-038 Pending member approval through users update
```

## Comment

Pending member approval should use existing users table and membership_status.

Do not create:

```text
join_requests
farm_memberships
member_registry
```

---

## 8.4 Notebook / Note Items

```text
BE-039 Create notebook entry
BE-040 List notebook entries
BE-041 Get notebook entry
BE-042 Update notebook entry
BE-043 Archive notebook entry
BE-044 Search notebook entries
BE-045 Create note item
BE-046 List note items
BE-047 Get note item
BE-048 Update note item
BE-049 Delete note item carefully
BE-050 Enforce sequence_order
BE-051 Support link item type
```

## Comment

Search is keyword/filter only.

Do not implement:

```text
vector search
semantic search
LLM search
RAG search
```

---

## 8.5 Consultation Flow

```text
BE-052 Support entry_type=consultation
BE-053 Support ai_provider / external AI field according to frozen API
BE-054 Save learned_summary
BE-055 Save consultation status if supported
BE-056 Validate consultation entry_type before consultation update
```

## Comment

This is not a separate Consultation module.

Do not create:

```text
models/consultation.py
schemas/consultation.py
repositories/consultations.py
services/consultation_service.py
api/v1/consultations.py
```

---

## 8.6 Follow-Ups

```text
BE-057 Create follow-up
BE-058 List follow-ups
BE-059 Get follow-up
BE-060 Record outcome
BE-061 Validate follow_up_day = 3 / 7 / 14
BE-062 Validate outcome = improved / same / worse / unknown
```

## Comment

Follow-Up is allowed because it is a frozen domain/API scope.

This is different from Consultation.

---

## 8.7 Notifications

```text
BE-063 List notifications
BE-064 Get notification
BE-065 Mark notification read
BE-066 Mark all notifications read
BE-067 Create upload reminder notification if required
BE-068 Create follow-up reminder notification if required
```

## Comment

Notification is not audit log.

Do not create audit_logs table.

---

## 8.8 Files / Upload Queue / Sync

```text
BE-069 MinIO bucket initialization
BE-070 Object key generation
BE-071 POST /api/v1/files/upload-url
BE-072 POST /api/v1/files/complete
BE-073 POST /api/v1/files/upload-failed
BE-074 Create upload queue record
BE-075 List upload queue
BE-076 Update upload queue status
BE-077 Retry upload queue record
BE-078 POST /api/v1/sync/batch
BE-079 client_id idempotency
BE-080 conflict handling
```

## Comment

Upload Queue must not be confused with Notebook Analysis status.

Save, Upload, Analyze remain separate.

---

# 9. Database Task Backlog

## 9.1 Required Tables

Implement only frozen tables:

```text
organizations
users
farms
zones
trees
notebook_entries
note_items
follow_ups
notifications
upload_queue
roles / user_roles only if included in frozen schema
```

## 9.2 Additive v1.1 User Fields

```text
phone
farmer_status
membership_status
account_status
primary_farm_id
registered_at if included in additive DB revision
```

## 9.3 Optional Farm Location Enhancement

```text
farms.location JSONB NULL
```

## Comment

Farm location JSONB is allowed only as approved additive enhancement.

Do not create a separate location table.

---

## 9.4 Forbidden Tables

```text
qr_registry
consultations
owners
farmers
members
blocks
farm_memberships
reviews
knowledge
audit_logs
permissions
vectors
documents
commerce
robots
```

## Comment

This is the database guardrail.

Developers should verify this after migrations.

---

# 10. Mobile Task Backlog

## 10.1 Foundation

```text
MOB-001 Create Flutter project
MOB-002 Add Android target
MOB-003 Add iOS target
MOB-004 Add environment config
MOB-005 Add API client
MOB-006 Add secure token storage
MOB-007 Add local database
MOB-008 Add media file storage
MOB-009 Add connectivity service
MOB-010 Add session manager
```

## 10.2 Auth / Onboarding

```text
MOB-011 Register screen
MOB-012 Login screen
MOB-013 Phone normalization
MOB-014 Farmer status selection
MOB-015 Farm ID input for owner_family/farm_staff
MOB-016 Pending approval screen
MOB-017 Account blocked screen
MOB-018 First-time permission setup
```

## 10.3 Owner Farm Setup

```text
MOB-019 Create Farm screen
MOB-020 Farm name required
MOB-021 GPS auto-fill if permission granted
MOB-022 Editable location fields
MOB-023 Create Zone screen if allowed
MOB-024 Create Tree screen if allowed
```

## 10.4 Capture / Notebook

```text
MOB-025 Home screen
MOB-026 Farm selector
MOB-027 Add Note flow
MOB-028 Notebook Entry local draft
MOB-029 Note Item timeline
MOB-030 Photo capture
MOB-031 Video capture
MOB-032 Voice recording
MOB-033 Text note
MOB-034 File picker
MOB-035 Link item
MOB-036 Existing media picker
```

## 10.5 Upload / Sync

```text
MOB-037 Upload queue local
MOB-038 Sync queue local
MOB-039 client_id generation
MOB-040 device_id generation
MOB-041 client_batch_id generation
MOB-042 Upload URL request
MOB-043 Upload to MinIO
MOB-044 Complete upload
MOB-045 Retry failed upload
MOB-046 Sync batch
MOB-047 Partial success handling
```

## 10.6 Ask AI External Flow

```text
MOB-048 Ask AI screen
MOB-049 Capture evidence
MOB-050 Save local consultation entry
MOB-051 Open external AI app
MOB-052 Return to ARI
MOB-053 Prompt “What did you learn?”
MOB-054 Save learned_summary
MOB-055 Schedule 3/7/14 follow-up
MOB-056 Record outcome
```

## Comment

Ask AI is external.

Do not implement internal AI assistant.

Do not call OpenAI/Gemini/Claude API from backend in P2-1.

---

# 11. Web Task Backlog

## 11.1 Foundation

```text
WEB-001 Create Next.js app
WEB-002 Add TypeScript
WEB-003 Add environment config
WEB-004 Add API client
WEB-005 Add auth/session manager
WEB-006 Add token refresh flow
WEB-007 Add layout
WEB-008 Add role-based navigation visibility
WEB-009 Add TH/EN text support if simple
```

## 11.2 Core Pages

```text
WEB-010 Login page
WEB-011 Dashboard page
WEB-012 Farm list
WEB-013 Farm detail
WEB-014 Notebook list
WEB-015 Notebook entry detail
WEB-016 Media viewer
WEB-017 Follow-ups page
WEB-018 Notifications page
WEB-019 Review / Approval Queue
```

## 11.3 Administration Pages

```text
WEB-020 Users page
WEB-021 Organizations page
WEB-022 Pending members page if backend supports users filter
WEB-023 User status update if backend supports patch
WEB-024 membership_status transition UI if backend supports it
```

## 11.4 Knowledge Views

```text
WEB-025 Knowledge Candidates view over notebook entries
WEB-026 Knowledge Library view over notebook entries
```

## Comment

Knowledge Candidate is not a new entity.

Knowledge Library is not a new entity.

They are views over existing Notebook Entries.

If status fields are insufficient, mark API Gap.

---

# 12. Testing Backlog

## 12.1 Backend Tests

```text
TEST-BE-001 Health check
TEST-BE-002 DB connection
TEST-BE-003 Alembic migration
TEST-BE-004 Phone normalization
TEST-BE-005 Register owner
TEST-BE-006 Register owner_family
TEST-BE-007 Register farm_staff
TEST-BE-008 Login by phone
TEST-BE-009 Refresh token
TEST-BE-010 Auth/me fields
TEST-BE-011 Account status guard
TEST-BE-012 Membership status guard
TEST-BE-013 Farm hierarchy validation
TEST-BE-014 Notebook entry create/list/detail
TEST-BE-015 Note item sequence_order
TEST-BE-016 Consultation as notebook entry
TEST-BE-017 Follow-up outcome
TEST-BE-018 Upload URL
TEST-BE-019 Upload complete
TEST-BE-020 Sync batch idempotency
TEST-BE-021 Forbidden table/module audit
```

## 12.2 Mobile Tests

```text
TEST-MOB-001 Register form
TEST-MOB-002 Login form
TEST-MOB-003 Pending approval route
TEST-MOB-004 Offline local save
TEST-MOB-005 Media capture metadata
TEST-MOB-006 Upload queue retry
TEST-MOB-007 Sync batch
TEST-MOB-008 Ask AI learned_summary flow
TEST-MOB-009 Follow-up outcome offline
```

## 12.3 Web Tests

```text
TEST-WEB-001 Login
TEST-WEB-002 Auth/me restore
TEST-WEB-003 Token refresh
TEST-WEB-004 Role navigation visibility
TEST-WEB-005 Farm list/detail
TEST-WEB-006 Notebook list/detail
TEST-WEB-007 Media viewer
TEST-WEB-008 Review queue
TEST-WEB-009 Pending members if supported
TEST-WEB-010 Knowledge candidate view
```

## 12.4 E2E Tests

```text
TEST-E2E-001 Owner register → create farm
TEST-E2E-002 Farm staff register → pending approval
TEST-E2E-003 Admin approves member
TEST-E2E-004 Mobile offline note capture
TEST-E2E-005 Mobile upload media
TEST-E2E-006 Web review notebook entry
TEST-E2E-007 Consultation learned_summary
TEST-E2E-008 Follow-up outcome
```

## Comment

E2E tests should mirror pilot behavior.

Do not test future modules in P2-1.

---

# 13. Deployment Backlog

## 13.1 Local Development

```text
DEP-001 docker compose up
DEP-002 run migrations
DEP-003 seed local data
DEP-004 health check
DEP-005 MinIO bucket check
DEP-006 EMQX check
DEP-007 backend API smoke test
DEP-008 mobile connects to local API
DEP-009 web connects to local API
```

## 13.2 Prototype VPS / Cloud

```text
DEP-010 Provision server
DEP-011 Install Docker
DEP-012 Configure firewall
DEP-013 Configure environment variables
DEP-014 Deploy backend
DEP-015 Deploy database
DEP-016 Deploy MinIO
DEP-017 Deploy EMQX
DEP-018 Deploy web app
DEP-019 Configure HTTPS
DEP-020 Configure backup
DEP-021 Smoke test remote API
DEP-022 Pilot user account setup
```

## 13.3 Not P2-1 Deployment

```text
Farm local server
Hybrid sync
Robot edge deployment
Commerce deployment
Internal AI deployment
RAG/vector infrastructure
```

## Comment

Do not build deployment complexity before pilot validation.

---

# 14. Acceptance Criteria

## 14.1 System Acceptance

```text
One backend serves Mobile and Web
One database stores shared data
One RBAC system is used
Mobile and Web call /api/v1
No separate app/backend/database is created
No forbidden tables or services exist
```

## 14.2 Backend Acceptance

```text
FastAPI runs locally
Docker stack runs locally
Database migrations work
Phone register/login works
JWT access/refresh works
Owner onboarding works
Family/staff Farm ID join works
Pending approval works through users/membership_status
Farm/Zone/Tree hierarchy works
Notebook Entry and Note Item work
Follow-Up works
Notification works
Upload URL/complete works
Sync batch works
```

## 14.3 Mobile Acceptance

```text
Flutter Android build works
Flutter iOS build works
Phone registration works
Phone login works
Offline capture works
Local note save works
Upload queue works
Sync works
External Ask AI flow works
Follow-up outcome works
```

## 14.4 Web Acceptance

```text
Browser Web App runs
Phone login works
Dashboard works
Farm list/detail works
Notebook list/detail works
Media viewer works through backend-approved URL
Review Queue works over Notebook Entries
Knowledge Candidate view works over Notebook Entries
Knowledge Library view works over Notebook Entries
Pending member approval works if backend supports it
```

## 14.5 Pilot Acceptance

```text
Prototype server works
Real pilot user can register
Real farm can be created
Real note with media can be captured
Real upload works
Web review works
Pilot feedback can be collected
Known gaps are documented
```

---

# 15. GitHub Issue Breakdown

## Epic 1 — Repository Foundation

```text
#1 Initialize ARI monorepo
#2 Add backend/mobile/web folders
#3 Add README
#4 Add .env.example
#5 Add docker-compose local stack
#6 Add GitHub labels and issue templates
```

## Epic 2 — Backend Foundation

```text
#7 Create FastAPI backend skeleton
#8 Add app config
#9 Add health endpoints
#10 Add DB session
#11 Add logging/error middleware
#12 Add Dockerfile
```

## Epic 3 — Database / Migration

```text
#13 Initialize Alembic
#14 Create frozen P0 base migration
#15 Create additive v1.1 migration
#16 Add indexes/constraints
#17 Add migration tests
#18 Add forbidden table audit
```

## Epic 4 — Auth / Onboarding

```text
#19 Implement password hashing
#20 Implement JWT access/refresh
#21 Implement phone normalization
#22 Implement auth/register
#23 Implement phone login
#24 Implement auth/me expanded payload
#25 Implement owner onboarding
#26 Implement family/staff Farm ID join
#27 Implement membership status transitions
```

## Epic 5 — Farm Structure

```text
#28 Organizations API
#29 Users API
#30 Farms API
#31 Zones API
#32 Trees API
#33 Hierarchy validation
#34 Optional QR payload endpoints
```

## Epic 6 — Notebook Core

```text
#35 Notebook Entry API
#36 Note Item API
#37 Timeline sequence_order
#38 Consultation as entry_type
#39 Follow-Up API
#40 Notifications API
#41 Keyword search
```

## Epic 7 — Upload / Sync

```text
#42 MinIO client
#43 files/upload-url
#44 files/complete
#45 files/upload-failed
#46 upload_queue API
#47 sync/batch API
#48 client_id idempotency
```

## Epic 8 — Mobile MVP

```text
#49 Flutter app foundation
#50 Mobile auth
#51 Onboarding
#52 Permission setup
#53 Farm setup
#54 Add Note
#55 Media capture
#56 Local storage
#57 Upload queue
#58 Sync batch
#59 Ask AI external flow
#60 Follow-up outcome
```

## Epic 9 — Web MVP

```text
#61 Next.js app foundation
#62 Web auth
#63 Dashboard
#64 Farm list/detail
#65 Notebook list/detail
#66 Media viewer
#67 Review Queue
#68 Knowledge Candidate view
#69 Knowledge Library view
#70 Administration users/orgs
#71 Pending members if supported
```

## Epic 10 — Testing / Deployment / Pilot

```text
#72 Backend tests
#73 Mobile tests
#74 Web tests
#75 E2E tests
#76 VPS deployment
#77 HTTPS
#78 Backups
#79 Pilot readiness checklist
#80 Pilot feedback log
```

---

# 16. What To Code First

## 16.1 First Commands

```bash
mkdir -p ari/{backend,mobile,web,infra,docs,scripts}
cd ari
git init

mkdir -p backend/app/{api/v1,core,db,models,schemas,repositories,services,dependencies,middleware,utils,tests}
mkdir -p backend/app/db/migrations/versions
mkdir -p docs/{frozen,execution,api-gaps}
mkdir -p scripts/{dev,db,deploy}
```

## 16.2 First Files

```text
README.md
.env.example
.gitignore
docker-compose.yml

backend/README.md
backend/Dockerfile
backend/pyproject.toml
backend/alembic.ini
backend/app/__init__.py
backend/app/main.py
backend/app/core/config.py
backend/app/api/v1/router.py
backend/app/api/v1/health.py
backend/app/db/base.py
backend/app/db/session.py
```

## 16.3 First Endpoint

```text
GET /health
GET /api/v1/health
```

Expected response:

```json
{
  "status": "ok",
  "service": "ari-backend",
  "api": "/api/v1"
}
```

## 16.4 First Commit

```text
chore: initialize ARI V1 monorepo foundation
```

## 16.5 Second Commit

```text
feat(backend): add FastAPI health check and config foundation
```

## 16.6 Third Commit

```text
chore(infra): add local docker stack with postgres minio emqx
```

## Comment

Do not start by coding Mobile UI.

Do not start by coding Web Dashboard.

Start with backend health + Docker + DB.

---

# 17. What Not To Code Yet

## 17.1 Not in Current P2-1 Prototype

```text
Internal AI assistant
Knowledge Graph
Vector Database
RAG
Agent orchestration
Robot control
Commerce
Audit system
Permission service
Advanced GIS
Farm local server
Hybrid farm/cloud sync
Desktop app
Electron app
Flutter desktop app
```

## 17.2 Not Allowed as Shortcut

```text
Create consultations table to simplify Ask AI
Create qr_registry table to simplify QR
Create farm_memberships table to simplify pending approval
Create reviews table to simplify Review Queue
Create knowledge table to simplify Knowledge Library
Create permissions table to simplify authorization
```

## Comment

These shortcuts create future redesign risk.

Use existing models first.

Mark gaps instead.

---

# 18. API Gap / Revision Proposal Register

## GAP-001 — auth/me Expanded Payload

Need:

```text
phone
farmer_status
membership_status
account_status
primary_farm_id
```

Status:

```text
Safe if already in Additive API v1.1.
If missing in implementation, add as API Gap / Revision Proposal.
```

---

## GAP-002 — Users Filter by membership_status

Needed for:

```text
Web Pending Members page
Admin approval workflow
```

Allowed pattern:

```text
GET /api/v1/users?membership_status=pending_farm_approval
```

Do not create:

```text
/member-approvals
/farm-memberships
/join-requests
```

---

## GAP-003 — Membership Status Transition

Needed for:

```text
Approve/reject pending farm members
```

Allowed pattern:

```text
PATCH /api/v1/users/{user_id}
```

Payload:

```json
{
  "membership_status": "active"
}
```

or:

```json
{
  "membership_status": "rejected"
}
```

Do not create:

```text
approval service
farm_memberships table
member registry
```

---

## GAP-004 — Review Queue Status Update

Needed for:

```text
Web Review / Approval Queue
```

Allowed pattern:

```text
PATCH /api/v1/notebook-entries/{entry_id}
```

Use existing status fields if available.

Do not create:

```text
reviews table
review service
review API
```

---

## GAP-005 — Knowledge Candidate Representation

Needed for:

```text
Knowledge Candidate Web view
```

Allowed:

```text
Use existing notebook_entries status / analysis_status / suggested_category if available.
```

If missing:

```text
Propose additive enum/status field.
```

Do not create:

```text
knowledge table
knowledge service
case library entity
knowledge graph
```

---

## GAP-006 — Media Read URL

Needed for:

```text
Web Media Viewer
```

Allowed:

```text
Backend-approved media read URL
Backend-generated presigned download URL
```

Do not:

```text
Directly expose MinIO public bucket
Access MinIO directly from Web
Log presigned URLs
```

---

## GAP-007 — Dashboard Aggregates

Needed for:

```text
Dashboard cards
Counts
Review queue summary
```

Initial solution:

```text
Use existing list endpoints.
```

Future proposal:

```text
Add dashboard summary endpoint only if performance requires.
```

Do not add silently in P2-1.

---

# 19. Developer Execution Rule

Before implementing any new file, developer should ask:

```text
1. Is this file/module listed in frozen implementation structure?
2. Does it map to an existing frozen entity or API?
3. Does it introduce a new table/entity/service?
4. Does it violate One Backend / One Database / One RBAC?
5. If missing, should it be API Gap instead?
```

## Comment

This rule should be placed in README or CONTRIBUTING.md.

It prevents accidental redesign during coding.

---

# 20. Final Execution Recommendation

Start with:

```text
Sprint 0
↓
Sprint 1
↓
Sprint 2
↓
Sprint 3
↓
Sprint 4
↓
Sprint 5
↓
Sprint 6
↓
Sprint 7
↓
Sprint 8
↓
Sprint 9
↓
Sprint 10
```

Immediate first coding target:

```text
Repository foundation
Docker local stack
FastAPI health
Database connection
Alembic migration
Auth register/login
```

Do not begin with:

```text
full mobile UI
full web dashboard
knowledge workspace
AI assistant
robot/commercial modules
```

---

# 21. Freeze Confirmation

```text
Document: ARI V1 — P2-1 Coding Execution Plan & Sprint Backlog v1.0
Status: FROZEN
Freeze Scope: P2 Coding Execution Plan and Sprint Backlog
Library Cross-Check: Completed against uploaded P0/P1 frozen files
Freeze Authority: Owner conditional approval after readiness confirmation
```

After this freeze:

```text
No silent coding expansion.
No new architecture.
No new database table.
No new domain entity.
No new RBAC role.
No new service boundary.

Changes require:
Revision Proposal → Owner Review → Approval → New Version
```

---

# 22. Final Statement

ARI V1 — P2-1 Coding Execution Plan & Sprint Backlog v1.0 is now the frozen execution guide for starting ARI V1 coding.

It preserves:

```text
One Platform
One Backend
One Database Architecture
One Mobile App
One Web App
One Domain Model
One RBAC System
```

It directs implementation toward:

```text
Backend-first coding
Local Docker development
Frozen database migrations
Auth and mobile onboarding
Notebook / media / sync core
Flutter Android/iOS mobile MVP
Browser-based Web App MVP
End-to-end integration
Prototype VPS deployment
Small real pilot
```

It does not authorize:

```text
new architecture
new domain entity
new database system
new RBAC role
new service boundary
forbidden future modules
```

Official Status:

```text
ARI V1 — P2-1 Coding Execution Plan & Sprint Backlog v1.0
FROZEN
```

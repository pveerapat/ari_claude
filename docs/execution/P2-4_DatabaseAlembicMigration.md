# ARI V1 — P2-4 Database and Alembic Migration Foundation v1.0

Project: ARI — Agricultural Intelligence Platform  
Phase: P2 Coding Execution Phase  
Document Number: P2-4  
Document Type: Database and Alembic Migration Foundation Specification / Execution Document  
Version: v1.0  
Status: Draft Final / Ready for Owner Review  
Prepared From: Frozen Source of Truth + P2-1 / P2-2 / P2-3 Coding Execution Authority  
Coding Direction: Backend Foundation First → Database → Auth → Farm Structure → Notebook / Upload / Sync → Mobile MVP → Web MVP → E2E → Prototype Deployment

---

# 1. Document Control

## 1.1 Document Identity

```text
Document Title:
ARI V1 — P2-4 Database and Alembic Migration Foundation v1.0

Project:
ARI — Agricultural Intelligence Platform

Phase:
P2 Coding Execution Phase

Document Number:
P2-4

Document Status:
Draft Final / Ready for Owner Review
```

## 1.2 Previous Frozen / Confirmed Documents

```text
ARI V1 — P2-1 Coding Execution Plan & Sprint Backlog v1.0
Status: FROZEN

ARI V1 — P2-2 Monorepo & Local Development Setup v1.0
Status: FROZEN
Coding Foundation: IMPLEMENTED
Smoke Test: PASS

ARI V1 — P2-3 Backend Feature Foundation v1.0
Status: FROZEN
Coding Foundation: IMPLEMENTED
Smoke Test: PASS
```

## 1.3 Document Boundary

This document defines the database and Alembic migration foundation only.

It is still a specification / execution document.

It does not authorize coding implementation unless the Owner explicitly instructs implementation later.

It does not create P2-5.

It does not redesign ARI.

## Comment

P2-4 is the first document that may allow real SQLAlchemy domain models and the first real Alembic migration, but only for frozen database scope.

---

# 2. Purpose

The purpose of P2-4 is to prepare the backend database layer for ARI V1 implementation using the frozen P0 Domain Model, P0 Database Schema, P0 API, P1 backend/mobile/web specifications, and current P2 execution documents.

P2-4 defines:

```text
Database model implementation boundary
SQLAlchemy model foundation
Alembic migration foundation
Initial migration strategy
Enum implementation strategy
Index and constraint strategy
Nullable hierarchy rules
UTC timestamp rules
User additive fields from P0 v1.1
Phone uniqueness rule
Ownership and foreign key rules
Seed data boundary
Database testing foundation
Migration smoke test checklist
Rollback / reset strategy for local development
Forbidden database changes
GitHub issue breakdown for P2-4
```

## Comment

The goal is to move from generic backend foundation into real database schema foundation without accidentally implementing authentication, business APIs, mobile screens, web pages, or future platform modules.

---

# 3. Scope

## 3.1 In Scope

P2-4 covers:

```text
Database schema implementation plan
SQLAlchemy model boundary
Alembic migration plan
Initial migration file scope
Frozen table list validation
Frozen enum list validation
Primary key / foreign key strategy
Nullable FK rules
User identity additive fields
Index strategy
Constraint strategy
Timestamp strategy
Local database reset workflow
Migration smoke test workflow
Database test foundation
Backend README database section update
AI coding guardrail update if needed
GitHub issue breakdown for P2-4
```

## 3.2 Deliverable

The deliverable is a safe database and migration foundation specification that can guide the later P2-4 coding implementation.

Target result after P2-4 coding implementation is explicitly approved:

```text
SQLAlchemy models exist only for frozen tables
Alembic is bound to SQLAlchemy Base metadata
Initial migration creates only frozen tables
Database tests verify expected tables
Forbidden tables are absent
Health endpoints remain unchanged
Backend tests pass
No feature APIs are introduced
No auth implementation is introduced
```

## 3.3 Scope Principle

P2-4 implements the Database Layer foundation only.

It must preserve this backend pattern:

```text
Router Layer
↓
Service Layer
↓
Repository Layer
↓
Database Layer
```

P2-4 may touch the Database Layer and model metadata.

P2-4 must not implement feature router, service, repository behavior, auth, RBAC, mobile, or web behavior.

---

# 4. Source of Truth

## 4.1 Frozen Source Documents

P2-4 must follow these frozen documents:

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
ARI V1 — P2-3 Backend Feature Foundation v1.0
```

## 4.2 Frozen Architecture Rules

P2-4 must preserve:

```text
One Platform
One Backend
One Database Architecture
One Mobile App
One Web App
One Domain Model
One RBAC System
```

P2-4 must not introduce:

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

## 4.3 Missing / Ambiguous Detail Rule

If a frozen document is missing, unclear, or inconsistent, developers must not invent behavior.

They must create:

```text
API Gap / Revision Proposal
```

and continue only with approved scope.

---

# 5. Relationship to P2-1, P2-2, and P2-3

## 5.1 Relationship to P2-1

P2-1 defines the coding order:

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

P2-4 corresponds to:

```text
Database migrations
```

It is still before:

```text
Auth and onboarding
Farm structure APIs
Notebook APIs
Upload / sync APIs
Mobile MVP
Web MVP
```

## 5.2 Relationship to P2-2

P2-2 created the monorepo and local development foundation:

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

Confirmed local services:

```text
api
postgres
minio
emqx
```

P2-4 uses this local Docker stack for database migration smoke tests.

## 5.3 Relationship to P2-3

P2-3 created the generic backend foundation:

```text
Common response foundation
Common error foundation
Logging foundation
CORS foundation
Request ID middleware foundation
Configuration foundation
Database dependency placeholder
SQLAlchemy Base boundary
Alembic boundary placeholder
Repository base pattern
Service base pattern
Common schemas
Generic utilities
Foundation tests
Backend README update
Local smoke test update
```

P2-4 extends only the database and Alembic parts of that backend foundation.

## 5.4 Health Contract Preserved

P2-4 must preserve:

```text
GET /health
GET /api/v1/health
```

Expected response must remain:

```json
{
  "status": "ok",
  "service": "ari-backend",
  "api": "/api/v1"
}
```

P2-4 must not change this response.

---

# 6. Non-Goals

P2-4 must not implement:

```text
Auth
Phone registration
Phone login
JWT issuing
RBAC logic
Business feature APIs
Farm APIs
Zone APIs
Tree APIs
Notebook APIs
Note Item APIs
Follow-Up APIs
Notification APIs
File upload flow
Upload queue API behavior
Sync batch behavior
Mobile screens
Web pages
Production deployment
Pilot deployment
```

P2-4 must not create feature routers:

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

P2-4 must not create feature services:

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

P2-4 must not create:

```text
backend/app/core/security.py
backend/app/dependencies/auth.py
backend/app/dependencies/rbac.py
backend/app/dependencies/scope.py
```

These are deferred to P2-5.

---

# 7. Database Foundation Assumptions

## 7.1 Stack

P2-4 assumes:

```text
PostgreSQL / TimescaleDB
SQLAlchemy ORM
Alembic migrations
UUID primary keys
UTC timestamps
JSONB where frozen specs require or approve JSON payloads
MinIO object storage references only
```

## 7.2 Development and Deployment Direction

```text
Development = Local Docker Server
Pilot Prototype = Central Remote Server / Cloud VPS
Farm Local Server = Future Enhancement / Optional Hybrid Deployment
```

## 7.3 TimescaleDB Boundary

TimescaleDB is part of the approved stack, but P2-4 must not redesign notebook storage as a time-series architecture.

Allowed:

```text
Use PostgreSQL-compatible SQLAlchemy models
Use normal relational tables
Enable TimescaleDB extension only if local stack already requires it
```

Not allowed:

```text
Hypertables unless frozen schema explicitly requires them
New time-series schema
Separate analytics database
```

## Comment

P2-4 is a relational schema foundation, not an analytics/database redesign.

---

# 8. Existing P2-3 Backend Baseline

P2-4 starts from the P2-3 backend foundation:

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
│   │   ├── constants.py
│   │   ├── errors.py
│   │   ├── logging.py
│   │   └── response.py
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

P2-4 should extend this structure carefully. It must not replace it with a new backend layout.

---

# 9. P2-4 Allowed Changes

P2-4 may define or prepare these files:

```text
backend/app/core/enums.py

backend/app/models/__init__.py
backend/app/models/organization.py
backend/app/models/user.py
backend/app/models/role.py
backend/app/models/farm.py
backend/app/models/zone.py
backend/app/models/tree.py
backend/app/models/notebook_entry.py
backend/app/models/note_item.py
backend/app/models/upload_job.py
backend/app/models/follow_up.py
backend/app/models/notification.py

backend/app/db/base.py
backend/app/db/session.py

backend/app/db/migrations/env.py
backend/app/db/migrations/script.py.mako
backend/app/db/migrations/versions/<initial_migration>.py

backend/alembic.ini

backend/app/tests/test_database_imports.py
backend/app/tests/test_migrations.py
backend/app/tests/test_model_metadata.py
```

P2-4 may update:

```text
backend/README.md
README.md
AGENTS.md
CLAUDE.md
CODEX.md
.env.example
backend/requirements.txt
backend/pyproject.toml
docker-compose.yml only if strictly needed for migration commands
```

## Comment

The model filename `upload_job.py` is allowed as an implementation filename, but the database table name must follow the frozen table name decision. See section 25 and API Gap handling for the `upload_queue` / `upload_jobs` naming mismatch.

---

# 10. P2-4 Forbidden Changes

P2-4 must not create forbidden services:

```text
consultation_service.py
qr_registry_service.py
permission_service.py
knowledge_service.py
robot_service.py
commerce_service.py
```

P2-4 must not create forbidden tables:

```text
consultations
qr_registry
permissions
permission_matrix
farm_memberships
owner_registry
farmer_registry
member_registry
block_registry
knowledge_assets
knowledge_graph
vectors
audit_logs
robot_commands
commerce_orders
```

P2-4 must not create forbidden folders:

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

P2-4 must not add seed users:

```text
admin user
root user
demo farmer
demo farm
test production user
```

## Comment

P2-4 must be checked by what it does not create.

---

# 11. Backend Database Package Structure After P2-4

Target structure after P2-4 implementation is approved:

```text
backend/
├── app/
│   ├── core/
│   │   └── enums.py
│   ├── db/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── session.py
│   │   └── migrations/
│   │       ├── env.py
│   │       ├── script.py.mako
│   │       └── versions/
│   │           └── <initial_migration>.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── organization.py
│   │   ├── user.py
│   │   ├── role.py
│   │   ├── farm.py
│   │   ├── zone.py
│   │   ├── tree.py
│   │   ├── notebook_entry.py
│   │   ├── note_item.py
│   │   ├── upload_job.py
│   │   ├── follow_up.py
│   │   └── notification.py
│   └── tests/
│       ├── test_database_imports.py
│       ├── test_migrations.py
│       └── test_model_metadata.py
├── alembic.ini
└── README.md
```

## Comment

This structure introduces SQLAlchemy domain models, not feature modules. There must still be no feature APIs, auth files, or business services.

---

# 12. Frozen Table List

## 12.1 Required Frozen Tables

P2-4 may implement SQLAlchemy models and initial migration for these frozen P0/P1 database tables:

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
```

## 12.2 Conditional Role Tables

Role-related tables are allowed only if the current frozen database schema explicitly includes them or the Owner confirms their inclusion for P2-4:

```text
roles
user_roles
```

Current handling:

```text
roles / user_roles = Conditional P2-4 scope
```

Recommended handling:

```text
Create API Gap / Revision Proposal before adding roles and user_roles to the initial migration if the frozen DB file does not explicitly define them.
```

## 12.3 Upload Queue Naming Guardrail

Frozen P0/P1 language uses:

```text
upload_queue
```

Some later implementation prompts and filenames use:

```text
upload_job.py
upload_jobs
```

P2-4 rule:

```text
Use upload_queue as the database table name unless Owner approves a formal naming revision.
UploadJob may be the Python class name and upload_job.py may be the model filename.
Do not create both upload_queue and upload_jobs.
```

## Comment

This section prevents duplicate table creation caused by naming drift.

---

# 13. Frozen Enum List

P2-4 may define database/domain enums only if they are frozen in P0/P1 specs.

Allowed enum groups include:

```text
user_role
entry_type
entry_context
item_type / note_item_type
ai_provider / external_ai
analysis_status
consultation_status
upload_status
upload_entity_type
upload_action
notification_type
notification_status
follow_up_outcome
farmer_status
membership_status
account_status
generic status where frozen table requires it
```

Known frozen values:

```text
entry_type:
  - note
  - consultation

entry_context:
  - general_note
  - registered_farm
  - external_observation
  - interview

item_type / note_item_type:
  - photo
  - video
  - voice
  - text
  - file
  - link

ai_provider / external_ai:
  - chatgpt
  - gemini
  - claude
  - other

follow_up_outcome:
  - improved
  - same
  - worse
  - unknown

farmer_status:
  - owner
  - owner_family
  - farm_staff

membership_status:
  - pending_farm_approval
  - active
  - rejected
  - suspended
  - revoked

account_status:
  - active
  - active_pending_verification
  - pending_review
  - suspended
  - rejected
  - revoked
```

Known status values that appear in frozen workflow and may require exact DB confirmation before enum migration:

```text
analysis_status:
  - not_started
  - other values require frozen confirmation

consultation_status:
  - pending
  - completed
  - other values require frozen confirmation

upload_status:
  - pending
  - uploading
  - failed
  - completed

notification_status:
  - exact values require frozen DB/API confirmation

notification_type:
  - exact values require frozen DB/API confirmation

upload_entity_type:
  - notebook_entry
  - exact complete value set requires frozen DB/API confirmation

upload_action:
  - create
  - exact complete value set requires frozen DB/API confirmation
```

If frozen documents disagree on enum names or values, create an API Gap / Revision Proposal.

## Comment

Do not invent enum values. It is safer to make a gap than silently hard-code a value that later conflicts with mobile/web/API behavior.

---

# 14. User Additive Fields From v1.1

P2-4 must include the approved additive user identity fields from P0 Domain / Database / API Additive Revision v1.1 and P1-1 Backend Additive Revision:

```text
phone
farmer_status
membership_status
account_status
primary_farm_id
```

The P0 Database Additive Revision also includes:

```text
registered_at
```

P2-4 handling:

```text
registered_at may be included if the current frozen P0 Database Additive Revision v1.1 is confirmed as the migration source.
```

Rules:

```text
phone may be NULL for existing migrated users
phone is required for new mobile self-registration later
phone uniqueness is enforced where phone IS NOT NULL
farmer_status is not an RBAC role
primary_farm_id references farms if present
membership_status does not create farm_memberships table
account_status does not create a separate account table
registered_at does not implement registration behavior
```

P2-4 must not implement registration or login behavior.

Auth and onboarding are deferred to P2-5.

---

# 15. SQLAlchemy Model Implementation Boundary

## 15.1 Allowed

P2-4 may define SQLAlchemy ORM models for frozen tables only.

Allowed model responsibilities:

```text
Table names
Column names
Column types
Primary keys
Foreign keys
Indexes
Unique constraints
Check constraints where safe
Relationships for ORM navigation only
UTC timestamp defaults
Enum bindings
JSONB nullable fields where approved
```

## 15.2 Not Allowed

SQLAlchemy models must not contain business behavior such as:

```text
Register user
Login user
Issue JWT
Approve farm member
Check RBAC permission
Generate QR code
Call MinIO
Call EMQX
Analyze notebook entry
Run AI
Sync mobile batch
```

## 15.3 Naming Rule

Models may use Python class names:

```text
Organization
User
Farm
Zone
Tree
NotebookEntry
NoteItem
FollowUp
Notification
UploadJob
Role
UserRole
```

Table names must stay frozen:

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
roles / user_roles only if confirmed
```

## Comment

Models are schema mapping only, not application logic.

---

# 16. Alembic Migration Foundation

P2-4 may create the first real Alembic migration.

Allowed Alembic work:

```text
Configure alembic.ini
Configure app/db/migrations/env.py
Bind Alembic to SQLAlchemy Base metadata
Create app/db/migrations/script.py.mako
Create app/db/migrations/versions/<initial_migration>.py
Support alembic upgrade head
Support alembic downgrade base for local development if safe
Document local migration commands
```

Not allowed:

```text
Auth token tables
Refresh token blacklist table
Audit log table
Permission tables
Knowledge tables
Vector tables
Robot tables
Commerce tables
Production seed data
```

## Comment

Alembic must represent the frozen schema only. It must not become a place to sneak in future architecture.

---

# 17. Initial Migration Scope

## 17.1 Initial Migration Must Create

The initial migration should create only confirmed frozen tables:

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
```

Optional / conditional if confirmed before implementation:

```text
roles
user_roles
```

## 17.2 Initial Migration May Include

```text
PostgreSQL enum types for frozen enums
UUID primary keys
Foreign keys for frozen relationships
Indexes required by frozen specs
Partial unique index for users.phone where phone IS NOT NULL
Nullable farms.location JSONB if approved additive v1.1 is included
```

## 17.3 Initial Migration Must Not Include

```text
consultations
qr_registry
farm_memberships
permissions
audit_logs
knowledge_assets
vectors
robot_commands
commerce_orders
```

## 17.4 Table Naming Decision

P2-4 initial migration must not create both:

```text
upload_queue
upload_jobs
```

Default decision:

```text
Create upload_queue only.
```

If the implementation team wants `upload_jobs`, that requires Owner-approved Database Revision.

---

# 18. Primary Key Strategy

P2-4 uses UUID primary keys.

Recommended column pattern:

```text
id UUID PRIMARY KEY
```

Where frozen API/domain names use domain-specific ID names:

```text
organization_id
user_id
farm_id
zone_id
tree_id
entry_id
item_id
follow_up_id
notification_id
queue_id
```

Implementation rule:

```text
Either map public API field names to internal id columns through schemas later, or use explicit database column names only if already frozen.
Do not create duplicate ID columns.
```

Recommended P2-4 choice:

```text
Use id as physical primary key column if P1-1 backend convention expects it.
Expose domain-specific IDs through API schemas later.
```

But if existing frozen database file uses specific primary key column names, follow the frozen database file.

## API Gap Note

If the frozen database specification does not clearly decide between `id` and `*_id` physical column names, create:

```text
API-GAP-P2-4-001 — Physical primary key column naming
```

before coding.

## Comment

Do not let naming ambiguity create duplicate primary key columns.

---

# 19. Foreign Key Strategy

Required relationships:

```text
users.organization_id → organizations.id
farms.organization_id → organizations.id
zones.farm_id → farms.id
trees.zone_id → zones.id

notebook_entries.organization_id → organizations.id
notebook_entries.created_by_user_id → users.id
notebook_entries.farm_id → farms.id NULL
notebook_entries.zone_id → zones.id NULL
notebook_entries.tree_id → trees.id NULL

note_items.entry_id → notebook_entries.id

follow_ups.entry_id → notebook_entries.id

notifications.user_id → users.id

upload_queue.entry_id → notebook_entries.id NULL or NOT NULL according to frozen schema

users.primary_farm_id → farms.id NULL

user_roles.user_id → users.id if role tables confirmed
user_roles.role_id → roles.id if role tables confirmed
```

Foreign key deletion policy should be conservative:

```text
Do not cascade-delete evidence records by default.
Prefer restrict or set null only where frozen schema allows it.
Hard delete is not recommended for evidence-first records.
```

## Comment

Evidence First means accidental cascading deletes should be avoided.

---

# 20. Nullable Hierarchy Rules

P2-4 must preserve:

```text
farm_id nullable
zone_id nullable
tree_id nullable
```

Reasons:

```text
External observations
Interviews
General notes
Consultations outside registered farms
Capture First / Structure Later
Offline First
```

Hierarchy consistency must still be preserved when values exist:

```text
farm belongs to organization
zone belongs to farm
tree belongs to zone
```

P2-4 database constraints may enforce direct FK existence.

Cross-field hierarchy validation may be deferred to service layer if too complex for the initial migration.

Examples of service-layer validation deferred to later P2 documents:

```text
If zone_id is provided, zone.farm_id must match notebook_entries.farm_id when farm_id is provided.
If tree_id is provided, tree.zone_id must match notebook_entries.zone_id when zone_id is provided.
If farm_id is provided, farm.organization_id must match notebook_entries.organization_id.
```

Deferred to:

```text
P2-6 Farm Structure Backend
P2-7 Notebook / Upload / Sync Backend
```

## Comment

P2-4 can enforce relational existence. It does not implement business validation services.

---

# 21. Organization Ownership Rules

Frozen ownership principle:

```text
Organization owns data.
Users create data.
```

P2-4 must reflect this through schema relationships:

```text
organizations own users
organizations own farms
notebook_entries belong to organization
notebook_entries are created by users
```

Required database fields where frozen specs require them:

```text
users.organization_id
farms.organization_id
notebook_entries.organization_id
notebook_entries.created_by_user_id
```

P2-4 must not create:

```text
owner_registry
farmer_registry
member_registry
farm_memberships
```

Owner is represented by:

```text
Organization + User + farmer_status
```

Membership approval is represented by:

```text
users.membership_status
users.primary_farm_id
```

## Comment

This preserves One Domain Model and prevents registry/table expansion.

---

# 22. Timestamp and UTC Rules

P2-4 must use UTC timestamp conventions.

Allowed timestamp columns:

```text
created_at
updated_at
recorded_at
uploaded_at
registered_at
deleted_at only if already present or required for approved partial index compatibility
```

Rules:

```text
Store timestamps in UTC
Use TIMESTAMPTZ for PostgreSQL where possible
Do not introduce local timezone business logic
Do not calculate farm-local day boundaries in P2-4
```

Farm-specific timezone behavior is deferred.

If `deleted_at` is needed only because the approved phone partial unique index references it, the migration must either:

```text
1. Include deleted_at only if frozen schema already includes soft delete; or
2. Adjust the unique index to WHERE phone IS NOT NULL only and create an API Gap for deleted_at dependency.
```

Recommended P2-4 handling:

```text
Create API-GAP-P2-4-002 if deleted_at is not clearly defined in frozen users schema.
```

## Comment

UTC is a storage rule. Local display belongs to mobile/web later.

---

# 23. JSONB Usage Boundary

Allowed JSONB usage:

```text
farms.location JSONB NULL if approved additive v1.1 is included
metadata fields only if already frozen in the database schema
```

P2-4 must not create broad JSONB escape hatches such as:

```text
notebook_entries.extra
users.profile_blob
farm_membership_json
permissions_json
knowledge_json
```

P2-4 must not create a separate location table.

## Comment

JSONB is allowed only where already approved. It must not become a way to bypass the frozen domain model.

---

# 24. MinIO Reference Boundary

P2-4 may define database fields that store MinIO object references.

Allowed in `note_items` if frozen schema supports them:

```text
file_path
file_ref
local_path
checksum
duration_sec
content_type
file_size
upload_status
```

P2-4 must not implement:

```text
Presigned upload URL generation
File upload API
MinIO client
Media read URL
Thumbnail generation
Virus scanning
Upload worker
```

These are deferred to:

```text
P2-7 Notebook / Upload / Sync Backend
```

## Comment

The database may store references to evidence files. Object storage behavior is not part of P2-4.

---

# 25. Upload Job Table Boundary

Frozen P0/P1 scope names the upload lifecycle entity as:

```text
upload_queue
```

P2-4 implementation may use:

```text
UploadJob model class
backend/app/models/upload_job.py
```

But the table name should be:

```text
upload_queue
```

unless the Owner approves a formal database naming revision.

Required fields from frozen domain/API direction may include:

```text
queue_id / id
entry_id
client_id
upload_entity_type
upload_action
status
retry_count
created_at
uploaded_at
```

Allowed status values:

```text
pending
uploading
failed
completed
```

P2-4 must not implement upload retry behavior or sync behavior.

Those are deferred to:

```text
P2-7 Notebook / Upload / Sync Backend
```

## API Gap

Create:

```text
API-GAP-P2-4-003 — upload_queue vs upload_jobs naming
```

if implementation files or migration tools attempt to create `upload_jobs`.

---

# 26. Follow-Up and Notification Table Boundary

## 26.1 Follow-Ups

P0 Domain/API and P1-1 include Follow-Up as frozen P0 scope.

P2-4 may create:

```text
follow_ups
```

Required concept:

```text
Follow-Up references Notebook Entry
Follow-Up supports 3 / 7 / 14 day reminders
Outcome values: improved / same / worse / unknown
```

P2-4 must not implement follow-up scheduling behavior, notification generation, or endpoint logic.

## 26.2 Notifications

P0 Domain/API and P1-1 include Notifications as frozen P0 scope.

P2-4 may create:

```text
notifications
```

Required concept:

```text
Notification references user
Notification stores type, message, status, created_at
```

P2-4 must not implement push notifications, mobile permission flow, notification read APIs, or scheduler logic.

## Comment

Tables are allowed because they are frozen P0 scope. Behavior is deferred.

---

# 27. Role and User_Roles Boundary

P1-1 and P2-1 mention role-related tables conditionally.

P2-4 rule:

```text
Do not create roles / user_roles unless confirmed by frozen database schema or Owner approval for P2-4.
```

If confirmed, role tables may support frozen RBAC roles only:

```text
farmer
ari_staff
farm_coordinator
agronomist
reviewer
admin
root
```

P2-4 must not create:

```text
new RBAC role
permission table
permission matrix
permission service
policy engine
```

Seed role data is deferred to P2-5 unless required for migration integrity.

## API Gap

Create:

```text
API-GAP-P2-4-004 — roles/user_roles database inclusion confirmation
```

if the frozen DB schema file does not explicitly define these tables.

---

# 28. Index Strategy

P2-4 may create indexes required by frozen specs and basic relational access patterns.

Recommended indexes:

```text
idx_users_organization_id
uq_users_phone_not_null or uq_users_phone_active
idx_users_membership_status
idx_users_account_status
idx_users_primary_farm_id

idx_farms_organization_id
idx_farms_org_name if frozen schema requires farms(org_id, name)

idx_zones_farm_id
idx_trees_zone_id

idx_notebook_entries_organization_id
idx_notebook_entries_created_by_created_at
idx_notebook_entries_farm_id
idx_notebook_entries_zone_id
idx_notebook_entries_tree_id
idx_notebook_entries_entry_type
idx_notebook_entries_entry_context
idx_notebook_entries_created_at

idx_note_items_entry_id_sequence_order

idx_follow_ups_entry_id
idx_follow_ups_outcome

idx_notifications_user_id
idx_notifications_status

idx_upload_queue_entry_id
idx_upload_queue_status
idx_upload_queue_client_id
```

Partial unique phone index:

```sql
CREATE UNIQUE INDEX uq_users_phone_not_null
ON users(phone)
WHERE phone IS NOT NULL;
```

If frozen schema clearly includes `deleted_at`, use:

```sql
CREATE UNIQUE INDEX uq_users_phone_active
ON users(phone)
WHERE phone IS NOT NULL
AND deleted_at IS NULL;
```

## Comment

Indexes should support frozen access patterns, not future analytics systems.

---

# 29. Constraint Strategy

P2-4 may define constraints for schema safety.

Allowed constraints:

```text
Primary keys
Foreign keys
Unique phone where not null
Unique sequence_order per entry if frozen / safe
Enum constraints
Basic NOT NULL for required frozen fields
Basic check constraints for positive sequence_order
Basic check constraints for retry_count >= 0
```

Nullable rules:

```text
farm_id nullable
zone_id nullable
tree_id nullable
primary_farm_id nullable
phone nullable for existing migrated users
farms.location nullable
```

Do not make `phone` NOT NULL in P2-4.

Do not create database constraints that require:

```text
farm_id when zone_id exists
zone_id when tree_id exists
organization membership approval
role authorization
mobile onboarding state transitions
```

These belong to later service-layer implementation.

## Comment

Constraints should protect data shape without implementing business workflows too early.

---

# 30. Seed Data Boundary

Default P2-4 rule:

```text
No production seed data
No demo farm data
No user accounts
No admin/root user seed
No mobile test accounts
```

Role seed data:

```text
Deferred to P2-5 unless required for migration integrity and confirmed by frozen DB scope.
```

If role seed data is later approved, it must include frozen roles only:

```text
farmer
ari_staff
farm_coordinator
agronomist
reviewer
admin
root
```

P2-4 may include test-only fixtures inside tests if they do not become production seed data.

## Comment

Creating users or roles too early can accidentally implement auth/onboarding before P2-5.

---

# 31. Database Reset / Local Development Workflow

P2-4 must document local reset workflow only.

Allowed local commands:

```bash
docker compose up -d --build
docker compose ps
docker compose exec api alembic upgrade head
docker compose exec api pytest
```

Reset local database:

```bash
docker compose down -v
docker compose up -d --build
docker compose exec api alembic upgrade head
docker compose exec api pytest
```

Local downgrade if safe:

```bash
docker compose exec api alembic downgrade base
docker compose exec api alembic upgrade head
```

Rules:

```text
Use reset only for local development
Do not document destructive production reset
Do not use migration reset as a substitute for proper migration history
```

## Comment

P2-4 reset workflow is for developer machines only.

---

# 32. Migration Testing Foundation

Allowed tests:

```text
test SQLAlchemy model imports
test Base metadata includes expected frozen tables
test Alembic config loads
test migration can run against local Postgres
test no forbidden tables exist
test health endpoints still unchanged
```

Not allowed tests:

```text
auth tests
phone registration tests
phone login tests
JWT tests
RBAC tests
farm API tests
notebook API tests
file upload tests
sync tests
mobile tests
web tests
```

Recommended test files:

```text
backend/app/tests/test_database_imports.py
backend/app/tests/test_model_metadata.py
backend/app/tests/test_migrations.py
```

Minimum metadata test expectations:

```text
Expected tables exist:
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

Forbidden tables absent:
  consultations
  qr_registry
  farm_memberships
  permissions
  audit_logs
  knowledge_assets
  vectors
```

Conditional expectations:

```text
roles
user_roles
```

only if confirmed for P2-4.

---

# 33. Backend README Update Requirements

P2-4 must update backend README with:

```text
Database architecture summary
SQLAlchemy model boundary
Alembic command reference
Local migration workflow
Local reset workflow
P2-4 forbidden table warning
Health endpoint preservation
Troubleshooting notes
```

README must clearly state:

```text
P2-4 does not implement auth
P2-4 does not implement feature APIs
P2-4 does not implement mobile/web
P2-4 creates only database foundation
```

---

# 34. Docker / Local Workflow Update Requirements

P2-4 may update Docker/local workflow only if needed to run migrations.

Allowed updates:

```text
Ensure api container can run alembic
Ensure DATABASE_URL is available to api container
Ensure backend dependencies include SQLAlchemy/Alembic/PostgreSQL driver
Add migration commands to README
```

P2-4 must not add new services to Docker Compose.

Existing services remain:

```text
api
postgres
minio
emqx
```

Not allowed:

```text
worker
redis
celery
separate auth service
separate migration service
separate web backend
```

---

# 35. Smoke Test Checklist

P2-4 is complete when:

```text
[ ] Docker stack starts
[ ] FastAPI backend starts
[ ] GET /health works
[ ] GET /api/v1/health works
[ ] Health response is unchanged
[ ] Alembic can upgrade head
[ ] Expected frozen tables are created
[ ] Forbidden tables are absent
[ ] Backend tests pass
[ ] No feature APIs are introduced
[ ] No auth implementation is introduced
[ ] No mobile implementation begins
[ ] No web implementation begins
```

Example commands:

```bash
docker compose up -d --build
docker compose ps
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/health
docker compose exec api alembic upgrade head
docker compose exec api pytest
```

Reset test:

```bash
docker compose down -v
docker compose up -d --build
docker compose exec api alembic upgrade head
docker compose exec api pytest
```

---

# 36. Acceptance Criteria

P2-4 implementation is accepted only if:

```text
SQLAlchemy Base metadata imports cleanly
Only frozen/approved models are imported
Alembic env.py is bound to Base metadata
Initial migration creates only allowed tables
No forbidden table exists after migration
Phone uniqueness rule is defined safely
P0 v1.1 user fields are included
Nullable farm/zone/tree hierarchy is preserved
UTC timestamp convention is used
Health endpoints remain unchanged
P2-3 foundation tests still pass
P2-4 database tests pass
No auth behavior exists
No feature routers exist
No feature services exist
No mobile/web work begins
```

---

# 37. Git Branch Rules

Use branches:

```text
main
develop
feature/p2-4-database-alembic-foundation
feature/database-model-foundation
feature/alembic-initial-migration
chore/database-migration-tests
docs/p2-4-database-foundation
```

Rules:

```text
Do not commit directly to main
Open PR into develop
Use one feature branch per logical work item if using multiple agents
Do not mix P2-5 auth work into P2-4 branches
Do not mix mobile/web work into P2-4 branches
```

---

# 38. Commit Message Rules

Recommended commit sequence:

```text
1. chore(db): prepare SQLAlchemy model foundation
2. feat(db): add frozen database models
3. feat(db): add Alembic initial migration foundation
4. chore(db): add migration and metadata tests
5. docs: add P2-4 database and migration guide
```

Commit guardrails:

```text
No auth commits
No API router commits
No mobile commits
No web commits
No forbidden table commits
No seed user commits
```

---

# 39. GitHub Issue Breakdown for P2-4

Create GitHub issues only for P2-4 scope:

```text
#1 Review frozen P0 database schema and P2-3 baseline before P2-4
#2 Confirm frozen table list and conditional role table handling
#3 Confirm upload_queue vs upload_jobs naming before migration
#4 Confirm physical primary key column naming id vs *_id
#5 Define SQLAlchemy enum boundary from frozen specs
#6 Add SQLAlchemy Base model imports for frozen tables
#7 Add Organization model
#8 Add User model with v1.1 additive fields
#9 Add Role and UserRole models only if confirmed
#10 Add Farm / Zone / Tree models
#11 Add Notebook Entry model
#12 Add Note Item model
#13 Add Upload Queue / UploadJob model with frozen table name
#14 Add Follow-Up model
#15 Add Notification model
#16 Configure Alembic env.py with Base metadata
#17 Create initial frozen schema migration
#18 Add database metadata and migration tests
#19 Add forbidden table check
#20 Update backend README database/migration section
#21 Run P2-4 smoke test
```

Do not create P2-4 issues for:

```text
auth
phone registration
phone login
JWT issuing
RBAC logic
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

---

# 40. What To Create Now

When Owner explicitly approves coding implementation for P2-4, create only:

```text
backend/app/core/enums.py
backend/app/models/
backend/app/db/migrations/
initial Alembic migration
database metadata tests
migration smoke tests
README database migration documentation
guardrail updates if needed
```

Create only models for:

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
roles / user_roles only if confirmed
```

---

# 41. What Not To Create Yet

Do not create yet:

```text
P2-5 Auth and Mobile Onboarding
auth router
register endpoint
login endpoint
JWT implementation
password hashing implementation
RBAC dependencies
scope dependencies
farm APIs
zone APIs
tree APIs
notebook APIs
note item APIs
follow-up APIs
notification APIs
file upload APIs
sync APIs
mobile app implementation
web app implementation
```

Do not create future platform modules:

```text
knowledge
RAG
vector
robot
commerce
permission
audit
QR registry
consultation entity
farm membership
```

---

# 42. API Gap / Revision Proposal Handling

If anything is missing, unclear, or inconsistent with frozen specs, do not invent behavior.

Create:

```text
API Gap / Revision Proposal
```

Store under:

```text
docs/api-gaps/
```

Use this template:

```markdown
# API Gap / Revision Proposal

Gap ID:
API-GAP-000X

Title:
<short title>

Discovered In:
P2-4 Database and Alembic Migration Foundation

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

## 42.1 Expected P2-4 API Gaps

P2-4 may need these gaps before coding:

```text
API-GAP-P2-4-001 — Physical primary key column naming: id vs *_id
API-GAP-P2-4-002 — users.deleted_at dependency in phone partial unique index
API-GAP-P2-4-003 — upload_queue vs upload_jobs naming
API-GAP-P2-4-004 — roles/user_roles database inclusion confirmation
API-GAP-P2-4-005 — exact enum values for notification_type and notification_status
API-GAP-P2-4-006 — exact enum values for analysis_status beyond not_started
API-GAP-P2-4-007 — exact enum values for consultation_status beyond pending/completed
```

## Comment

Gaps are not failures. They prevent silent architecture drift.

---

# 43. Freeze Readiness Checklist

P2-4 is ready for Owner freeze review when:

```text
[ ] Document control is complete
[ ] Purpose is clear
[ ] Scope is limited to database and Alembic foundation
[ ] Source of Truth list is complete
[ ] Relationship to P2-1 / P2-2 / P2-3 is clear
[ ] Non-goals are explicit
[ ] Existing P2-3 baseline is preserved
[ ] P2-4 allowed changes are defined
[ ] P2-4 forbidden changes are defined
[ ] Backend database package structure is defined
[ ] Frozen table list is defined
[ ] Frozen enum list is defined
[ ] User additive fields from v1.1 are included
[ ] SQLAlchemy model boundary is clear
[ ] Alembic migration boundary is clear
[ ] Initial migration scope is clear
[ ] Primary key strategy includes naming gap handling
[ ] Foreign key strategy is defined
[ ] Nullable hierarchy rules are preserved
[ ] Organization ownership rules are preserved
[ ] UTC timestamp rules are defined
[ ] JSONB boundary is defined
[ ] MinIO reference boundary is defined
[ ] Upload queue naming issue is handled
[ ] Follow-up and notification table boundary is confirmed
[ ] Role/user_roles boundary is conditional and safe
[ ] Index strategy is defined
[ ] Constraint strategy is defined
[ ] Seed data boundary is safe
[ ] Local reset workflow is defined
[ ] Migration testing foundation is defined
[ ] README update requirements are defined
[ ] Docker/local workflow requirements are defined
[ ] Smoke test checklist is defined
[ ] Acceptance criteria are clear
[ ] Git branch rules are defined
[ ] Commit message rules are defined
[ ] GitHub issues are P2-4 only
[ ] What to create now is clear
[ ] What not to create yet is clear
[ ] API Gap / Revision Proposal handling is defined
```

---

# Final Status

```text
ARI V1 — P2-4 Database and Alembic Migration Foundation v1.0

Status:
Draft Final / Ready for Owner Review

Implementation:
Not started in this document

Next document:
Do not create P2-5 yet
```

P2-4 preserves:

```text
One Platform
One Backend
One Database Architecture
One Mobile App
One Web App
One Domain Model
One RBAC System
```

P2-4 does not redesign ARI.

P2-4 does not add new architecture.

P2-4 does not implement auth, business APIs, mobile MVP, or web MVP.




***************************************************************
ARI V1 — P2-4 Database and Alembic Migration Foundation v1.0

Status: FROZEN ✅

ใช้เป็น Source of Truth สำหรับขั้นถัดไปใน P2 Coding Execution Phase
**************************************************************
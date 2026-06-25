# ARI V1 — P2-2 Monorepo & Local Development Setup v1.0

Project: ARI — Agricultural Intelligence Platform
Phase: P2 Coding Execution Phase
Document Number: P2-2
Document Type: Monorepo Setup + Local Development Environment Specification
Version: v1.0
Status: Draft / Ready for Owner Review
Freeze Status: Not Frozen
Prepared From: Frozen Source of Truth + P2-1 Coding Execution Authority
Coding Direction: Backend Foundation First → Database → Auth → Farm Structure → Notebook / Upload / Sync → Mobile MVP → Web MVP → E2E → Prototype Deployment

---

# 1. Document Control

## 1.1 Document Identity

```text
Document Title:
ARI V1 — P2-2 Monorepo & Local Development Setup v1.0

Project:
ARI — Agricultural Intelligence Platform

Phase:
P2 Coding Execution Phase

Document Number:
P2-2

Document Status:
Draft / Ready for Owner Review

Previous Frozen Document:
ARI V1 — P2-1 Coding Execution Plan & Sprint Backlog v1.0
Status: FROZEN
```

## 1.2 Document Purpose

This document defines the local repository foundation and development environment required before ARI V1 feature coding begins.

It defines:

```text
Monorepo setup
Local Docker stack
Initial backend skeleton
Health check endpoints
Environment template
Repository documentation
AI coding agent guardrails
Git workflow
Smoke test checklist
```

## 1.3 Document Boundary

This document does not implement backend features.

This document does not implement database schema migrations.

This document does not implement mobile screens.

This document does not implement web pages.

This document only prepares the safe coding foundation for later P2 documents.

## Comment

P2-2 is a setup document.

It exists to prevent accidental architecture expansion before feature coding begins.

---

# 2. Purpose

The purpose of P2-2 is to create a clean local development foundation for ARI V1.

The repository must be ready for coding agents and human developers to start implementation safely, without accidentally adding:

```text
new services
new entities
new RBAC roles
new database architecture
new mobile app variants
new web app variants
future AI / robot / commerce modules
```

P2-2 prepares only the coding environment.

Feature implementation begins later.

---

# 3. Scope

## 3.1 In Scope

P2-2 covers:

```text
Monorepo setup
Local repository structure
Local development tools
Local Docker stack
FastAPI backend skeleton
Health check endpoint
Environment template
README documentation
AI coding agent guardrails
Git branch rules
Commit message rules
Smoke test checklist
P2-2 GitHub issue breakdown
API Gap / Revision Proposal handling
```

## 3.2 P2-2 Deliverable

The intended deliverable is a repository foundation:

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

## 3.3 Scope Principle

P2-2 creates structure.

P2-2 does not create business logic.

P2-2 does not create feature modules.

P2-2 does not create production deployment.

---

# 4. Source of Truth

## 4.1 Frozen Source Documents

P2-2 must follow the frozen documents below:

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
```

## 4.2 Current Coding Authority

The direct coding authority for P2-2 is:

```text
ARI V1 — P2-1 Coding Execution Plan & Sprint Backlog v1.0
Status: FROZEN
```

## 4.3 Frozen Rules Preserved

P2-2 must preserve:

```text
One Platform
One Backend
One Database Architecture
One Mobile App
One Web App
One Domain Model
One RBAC System
```

## 4.4 No Redesign Rule

If any missing detail appears during setup, developers must not redesign ARI.

They must create:

```text
API Gap / Revision Proposal
```

and continue only with approved scope.

---

# 5. Non-Goals

P2-2 must not implement:

```text
Full database schema migrations
Full authentication
Phone registration
Phone login
User APIs
Farm APIs
Zone APIs
Tree APIs
Notebook APIs
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

## 5.1 Explicitly Forbidden

P2-2 must not introduce:

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

## 5.2 Deferrals

The following work is deferred:

```text
Backend feature foundation → Deferred to P2-3
Database and Alembic migrations → Deferred to P2-4
Auth and mobile onboarding → Deferred to P2-5
Farm structure backend → Deferred to P2-6
Notebook / upload / sync backend → Deferred to P2-7
Mobile MVP → Deferred to P2-8
Web MVP → Deferred to P2-9
E2E and prototype deployment → Deferred to P2-10
```

---

# 6. Local Development Assumptions

## 6.1 Development Environment

P2-2 assumes local development runs on a developer machine using Docker.

```text
Development = Local Docker Server
Pilot Prototype = Central Remote Server / Cloud VPS
Farm Local Server = Future Enhancement / Optional Hybrid Deployment
```

## 6.2 Local First, Not Production

The local stack is only for:

```text
developer setup
local smoke test
backend health check
infrastructure availability check
```

It is not:

```text
production deployment
pilot deployment
farm local server deployment
multi-farm production setup
```

## 6.3 Backend First Direction

P2-2 supports the P2 coding order:

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

## Comment

The repository must be ready for backend-first implementation, while still reserving `mobile/` and `web/` roots for later coding.

---

# 7. Required Local Tools

Developers should install:

```text
Git
Docker
Docker Compose
Python 3.12+
curl
make or shell-compatible terminal
```

Recommended but not mandatory for P2-2:

```text
VS Code
Postman / Insomnia
pgAdmin client
MinIO client
MQTT client
```

Future tools deferred:

```text
Flutter SDK → Deferred to P2-8
Android Studio / Xcode → Deferred to P2-8
Node.js / pnpm / npm for Web → Deferred to P2-9
Production deployment CLI tools → Deferred to P2-10
```

---

# 8. Repository Naming Convention

## 8.1 Repository Name

Recommended repository name:

```text
ari
```

Allowed display name:

```text
ARI V1
```

## 8.2 Root Folder

The local repository root must be:

```text
ari/
```

## 8.3 Naming Rules

Use:

```text
lowercase folders
kebab-case branch names
snake_case Python module names
clear P2 document numbers in docs
```

Do not use:

```text
apps/backend
apps/mobile
apps/web
```

## Comment

The frozen implementation documents use direct roots:

```text
backend/
mobile/
web/
```

Therefore P2-2 must not introduce an `apps/` structure.

---

# 9. Correct Monorepo Root Structure

The root structure must be:

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

## 9.1 Root Folder Meaning

```text
backend/        FastAPI backend implementation root
mobile/         Future Flutter mobile app root
web/            Future browser-based Web App root
infra/          Local infrastructure configuration
docs/           Frozen specs, execution docs, gap notes, decisions
scripts/        Local development helper scripts
docker-compose.yml
                Local Docker stack only
.env.example    Local environment template only
README.md       Repository setup and startup guide
```

## 9.2 Forbidden Root Structures

Do not create:

```text
apps/backend/
apps/mobile/
apps/web/
services/
microservices/
admin_backend/
web_backend/
farmer_app/
staff_app/
desktop_app/
electron_app/
```

---

# 10. Root File Structure

The root files required in P2-2 are:

```text
ari/
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
├── AGENTS.md
├── CLAUDE.md
└── CODEX.md
```

## 10.1 Root Files Purpose

```text
docker-compose.yml
Local development stack for api, postgres, minio, emqx

.env.example
Template for local environment variables with placeholder values only

.gitignore
Prevent local secrets, build artifacts, media, cache files from being committed

README.md
Human developer local setup guide

AGENTS.md
General AI coding agent guardrails

CLAUDE.md
Claude-specific coding guardrails

CODEX.md
Codex-specific coding guardrails
```

## 10.2 Secrets Rule

Never commit:

```text
.env
real database passwords
real JWT secrets
real MinIO credentials
real API keys
private certificates
production credentials
```

---

# 11. backend/ Initial Structure

P2-2 may create only the initial backend skeleton.

Required backend structure:

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
└── README.md
```

## 11.1 Allowed Backend Work in P2-2

P2-2 may define:

```text
FastAPI app initialization
Settings loading foundation
Root health route
/api/v1 health route
Database session placeholder
SQLAlchemy Base placeholder
Alembic placeholder only
Dockerfile for local API container
```

## 11.2 Not Allowed in P2-2

Do not create feature modules yet.

Do not create:

```text
backend/app/api/v1/auth.py
backend/app/api/v1/users.py
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

These are deferred to later P2 documents.

## 11.3 Forbidden Backend Services

Do not create:

```text
consultation_service.py
qr_registry_service.py
permission_service.py
knowledge_service.py
robot_service.py
commerce_service.py
```

## 11.4 Future Backend Module Placeholders

Future modules may be mentioned in documentation only.

They must not be implemented in P2-2.

```text
Auth → Deferred to P2-5
Users → Deferred to P2-5
Farm / Zone / Tree → Deferred to P2-6
Notebook / Note Items → Deferred to P2-7
Follow-Up / Notification → Deferred to P2-7
Upload / Sync / Files → Deferred to P2-7
```

---

# 12. mobile/ Initial Structure

P2-2 may create only the mobile placeholder root.

Minimum:

```text
mobile/
└── README.md
```

Optional placeholder:

```text
mobile/
├── README.md
└── .gitkeep
```

## 12.1 mobile/ README Purpose

The mobile README should state:

```text
Mobile App implementation is deferred to P2-8.
The future app must be one Flutter app.
Target platforms are Android and iOS only.
No separate farmer app.
No separate staff app.
No desktop app.
```

## 12.2 Not Allowed in P2-2

Do not implement:

```text
Flutter screens
Flutter navigation
local mobile database
upload queue
sync batch
phone registration
phone login
Ask AI workflow
media capture
```

Do not create:

```text
farmer_app/
staff_app/
desktop_app/
flutter_desktop/
```

---

# 13. web/ Initial Structure

P2-2 may create only the web placeholder root.

Minimum:

```text
web/
└── README.md
```

Optional placeholder:

```text
web/
├── README.md
└── .gitkeep
```

## 13.1 web/ README Purpose

The web README should state:

```text
Web App implementation is deferred to P2-9.
The future app must be one browser-based Web App.
Recommended stack is Next.js / React / TypeScript.
No native desktop app.
No Electron app.
No separate farmer/staff/admin web apps.
```

## 13.2 Not Allowed in P2-2

Do not implement:

```text
Next.js pages
React components
web auth flow
dashboard
farm list
farm detail
notebook pages
approval queue
knowledge candidate pages
```

Do not create:

```text
admin_web/
farmer_web/
staff_web/
desktop_app/
electron_app/
```

---

# 14. infra/ Structure

The required infra structure is:

```text
infra/
├── docker/
├── postgres/
├── minio/
└── emqx/
```

## 14.1 infra/ Purpose

```text
infra/docker/      local Docker helper configuration
infra/postgres/    local PostgreSQL / TimescaleDB configuration
infra/minio/       local MinIO configuration
infra/emqx/        local EMQX configuration
```

## 14.2 P2-2 Boundary

P2-2 infra is local-only.

Do not create production deployment configuration.

Do not create:

```text
kubernetes/
helm/
terraform/
ansible/
production/
vps/
farm-local-server/
cloud-run/
ecs/
eks/
gke/
```

## 14.3 Deployment Deferral

```text
Production / VPS deployment → Deferred to P2-10
Farm Local Server → Future Enhancement / Optional Hybrid Deployment
```

---

# 15. docs/ Structure

The required docs structure is:

```text
docs/
├── frozen/
├── execution/
├── api-gaps/
└── decisions/
```

## 15.1 docs/frozen/

Purpose:

```text
Store frozen Source of Truth documents.
```

Examples:

```text
P0 Domain Model
P0 Database Schema
P0 API Specification
P1-1 Backend Implementation Specification
P1-2 Mobile App Implementation Specification
P1-3 Web App Implementation Specification
P2-1 Coding Execution Plan
```

## 15.2 docs/execution/

Purpose:

```text
Store P2 coding execution documents.
```

P2-1 and P2-2 should be stored here:

```text
docs/execution/ARI-V1-P2-1-Coding-Execution-Plan-v1.0.md
docs/execution/ARI-V1-P2-2-Monorepo-Local-Development-Setup-v1.0.md
```

## 15.3 docs/api-gaps/

Purpose:

```text
Store API Gap / Revision Proposal notes found during coding.
```

Example:

```text
docs/api-gaps/API-GAP-0001-auth-me-membership-fields.md
```

## 15.4 docs/decisions/

Purpose:

```text
Store coding decisions that do not change architecture.
```

Allowed decision examples:

```text
Use port 8000 for local API
Use port 5432 for local PostgreSQL
Use port 9000 / 9001 for MinIO
Use port 18083 for EMQX Dashboard
```

Forbidden decision examples:

```text
Add permission service
Add farm membership table
Add QR registry
Add consultation entity
Add internal AI assistant
```

---

# 16. scripts/ Structure

The required scripts structure is:

```text
scripts/
├── dev/
├── db/
└── deploy/
```

## 16.1 scripts/dev/

May define placeholders:

```text
scripts/dev/start.sh
scripts/dev/stop.sh
scripts/dev/logs.sh
scripts/dev/health.sh
```

Purpose:

```text
start local stack
stop local stack
view local logs
check local health endpoints
```

## 16.2 scripts/db/

May define placeholders:

```text
scripts/db/reset-local.sh
scripts/db/check-postgres.sh
```

Purpose:

```text
local reset helper
database container check helper
```

Full database migration implementation is deferred.

```text
Database and Alembic migrations → Deferred to P2-4
```

## 16.3 scripts/deploy/

May exist as an empty placeholder only.

Production deployment scripts are not allowed in P2-2.

```text
E2E and prototype deployment → Deferred to P2-10
```

---

# 17. .env.example Requirements

P2-2 must create `.env.example`.

It must contain placeholder values only.

Do not include real credentials.

Required groups:

```text
App settings
Database settings
JWT settings
MinIO settings
EMQX settings
CORS settings
Logging settings
```

## 17.1 Required .env.example Template

```env
# ------------------------------------------------------------
# App settings
# ------------------------------------------------------------
APP_NAME=ARI Backend
APP_ENV=local
APP_DEBUG=true
API_V1_PREFIX=/api/v1
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# ------------------------------------------------------------
# Database settings
# ------------------------------------------------------------
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_DB=ari_local
POSTGRES_USER=ari_user
POSTGRES_PASSWORD=change_me_local_only
DATABASE_URL=postgresql+psycopg://ari_user:change_me_local_only@postgres:5432/ari_local

# ------------------------------------------------------------
# JWT settings
# ------------------------------------------------------------
JWT_SECRET_KEY=change_me_local_only
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60
REFRESH_TOKEN_EXPIRE_DAYS=30

# ------------------------------------------------------------
# MinIO settings
# ------------------------------------------------------------
MINIO_ENDPOINT=minio:9000
MINIO_ROOT_USER=ari_minio_user
MINIO_ROOT_PASSWORD=change_me_local_only
MINIO_BUCKET=ari-local
MINIO_SECURE=false

# ------------------------------------------------------------
# EMQX settings
# ------------------------------------------------------------
EMQX_HOST=emqx
EMQX_MQTT_PORT=1883
EMQX_DASHBOARD_PORT=18083
EMQX_USERNAME=ari_emqx_user
EMQX_PASSWORD=change_me_local_only

# ------------------------------------------------------------
# CORS settings
# ------------------------------------------------------------
CORS_ALLOW_ORIGINS=http://localhost:3000,http://localhost:5173
CORS_ALLOW_CREDENTIALS=true

# ------------------------------------------------------------
# Logging settings
# ------------------------------------------------------------
LOG_LEVEL=INFO
LOG_FORMAT=plain
```

## 17.2 Secret Rule

`.env.example` is safe to commit.

`.env` must never be committed.

---

# 18. docker-compose Local Stack

P2-2 local Docker stack must include:

```text
api
postgres
minio
emqx
```

Optional local-only services:

```text
pgadmin
minio-console
```

## 18.1 Required Services

```text
api
FastAPI backend local container

postgres
PostgreSQL / TimescaleDB local database

minio
Local object storage

emqx
Local MQTT broker
```

## 18.2 Forbidden Services

Do not introduce:

```text
worker service
permission service
AI service
RAG service
vector database
robot service
commerce service
separate backend service
```

## 18.3 Required Local Ports

Recommended local ports:

```text
api:       8000
postgres: 5432
minio:    9000
minio console: 9001
emqx mqtt: 1883
emqx dashboard: 18083
```

## 18.4 docker-compose.yml Scope

`docker-compose.yml` is for local development only.

It must not be treated as production deployment.

Production deployment is deferred:

```text
E2E and prototype deployment → Deferred to P2-10
```

## 18.5 Expected Local Compose Service Definition

P2-2 should define a local stack equivalent to:

```yaml
services:
  api:
    build:
      context: ./backend
    env_file:
      - .env
    ports:
      - "8000:8000"
    depends_on:
      - postgres
      - minio
      - emqx

  postgres:
    image: timescale/timescaledb:latest-pg16
    env_file:
      - .env
    ports:
      - "5432:5432"
    volumes:
      - ari_postgres_data:/var/lib/postgresql/data

  minio:
    image: minio/minio:latest
    env_file:
      - .env
    command: server /data --console-address ":9001"
    ports:
      - "9000:9000"
      - "9001:9001"
    volumes:
      - ari_minio_data:/data

  emqx:
    image: emqx/emqx:latest
    ports:
      - "1883:1883"
      - "18083:18083"
    volumes:
      - ari_emqx_data:/opt/emqx/data

volumes:
  ari_postgres_data:
  ari_minio_data:
  ari_emqx_data:
```

## Comment

This compose example defines only local infrastructure.

It does not add new ARI services.

---

# 19. PostgreSQL / TimescaleDB Local Setup

## 19.1 Required Local Database

Use:

```text
PostgreSQL / TimescaleDB
```

Recommended local image:

```text
timescale/timescaledb:latest-pg16
```

## 19.2 P2-2 Database Scope

P2-2 only confirms that the database container starts.

P2-2 does not implement full schema migrations.

## 19.3 Allowed in P2-2

Allowed:

```text
Database container starts
Database environment variables exist
Database connection string exists
Backend config can read database URL
Optional database reachability smoke test
```

## 19.4 Not Allowed in P2-2

Do not create:

```text
full schema migrations
users table
farms table
zones table
trees table
notebook_entries table
note_items table
follow_ups table
notifications table
upload_queue table
roles table
user_roles table
```

These are deferred:

```text
Database and Alembic migrations → Deferred to P2-4
```

## 19.5 Forbidden Tables

Do not create:

```text
qr_registry
consultations
farm_memberships
owner_registry
farmer_registry
member_registry
block_registry
permissions
knowledge
vector_documents
robot_jobs
commerce_orders
```

---

# 20. MinIO Local Setup

## 20.1 Required Local Object Storage

Use:

```text
MinIO
```

Purpose:

```text
local object storage placeholder for future media upload flow
```

## 20.2 P2-2 MinIO Scope

P2-2 only confirms that MinIO starts and the console is reachable.

P2-2 does not implement:

```text
file upload endpoint
presigned upload URL
file complete endpoint
media read URL
bucket lifecycle
thumbnail generation
```

These are deferred:

```text
Notebook / upload / sync backend → Deferred to P2-7
```

## 20.3 Local Ports

```text
MinIO API:     http://localhost:9000
MinIO Console: http://localhost:9001
```

## 20.4 Credential Rule

Use placeholder local-only credentials in `.env.example`.

Never commit real MinIO credentials.

---

# 21. EMQX Local Setup

## 21.1 Required Local MQTT Broker

Use:

```text
EMQX
```

Purpose:

```text
local MQTT broker foundation for future ARI messaging needs
```

## 21.2 P2-2 EMQX Scope

P2-2 only confirms that EMQX starts and the dashboard is reachable.

P2-2 does not implement:

```text
MQTT publishing
MQTT subscribing
device control
robot control
notification worker
background worker
```

## 21.3 Local Ports

```text
MQTT:       localhost:1883
Dashboard:  http://localhost:18083
```

## 21.4 Robot Boundary

EMQX in P2-2 does not mean robot control is implemented.

Robot control remains forbidden in P2-2.

---

# 22. FastAPI Backend Skeleton Setup

## 22.1 Backend Stack

The backend foundation uses:

```text
FastAPI
Python 3.12+
SQLAlchemy placeholder
Alembic placeholder
Docker
/api/v1
```

## 22.2 P2-2 Backend Responsibilities

P2-2 backend skeleton must support:

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

## 22.3 Not Implemented Yet

Do not implement:

```text
JWT auth
refresh token logic
phone registration
phone login
RBAC guards
database models
repositories
services
business rules
file upload
sync batch
```

Deferrals:

```text
Backend feature foundation → Deferred to P2-3
Database and Alembic migrations → Deferred to P2-4
Auth and mobile onboarding → Deferred to P2-5
```

## 22.4 Required API Mount

The backend must mount API v1 under:

```text
/api/v1
```

## 22.5 Backend README

`backend/README.md` must explain:

```text
How to start backend locally
How to run health check
What is implemented in P2-2
What is deferred
Forbidden backend modules
```

---

# 23. Health Check Endpoints

P2-2 must define these endpoints:

```text
GET /health
GET /api/v1/health
```

## 23.1 Expected Response

Both endpoints should return:

```json
{
  "status": "ok",
  "service": "ari-backend",
  "api": "/api/v1"
}
```

## 23.2 Root Health

```text
GET /health
```

Purpose:

```text
Confirm FastAPI process is running.
```

## 23.3 API v1 Health

```text
GET /api/v1/health
```

Purpose:

```text
Confirm /api/v1 router is mounted.
```

## 23.4 Database Reachability

Database reachability may be included as a local smoke test.

However, full DB schema implementation is deferred.

Allowed:

```text
Check database connection reachable
```

Not allowed:

```text
Create full schema
Run feature migrations
Seed users
Seed farms
Seed notebook data
```

---

# 24. Alembic Placeholder Only

P2-2 may include:

```text
backend/alembic.ini
backend/app/db/base.py
backend/app/db/session.py
```

## 24.1 Allowed

Allowed:

```text
Alembic config placeholder
SQLAlchemy Base placeholder
Database URL setting placeholder
Migration folder placeholder only if needed
```

## 24.2 Not Allowed

Do not create actual schema migrations in P2-2.

Do not create:

```text
versions/001_create_users.py
versions/002_create_farms.py
versions/003_create_notebook_entries.py
```

## 24.3 Deferral

```text
Database and Alembic migrations → Deferred to P2-4
```

---

# 25. Git Branch Rules

## 25.1 Main Branches

Required long-lived branches:

```text
main
develop
```

## 25.2 P2-2 Working Branches

Recommended P2-2 branches:

```text
feature/p2-2-monorepo-setup
feature/backend-health-check
chore/docker-local-stack
docs/agent-guardrails
```

## 25.3 Branch Rules

```text
main
Only frozen, reviewed, stable code

develop
Integration branch for accepted P2 work

feature/*
Feature or setup work branch

chore/*
Infrastructure or repository maintenance

docs/*
Documentation-only work
```

## 25.4 Merge Rule

P2-2 branches should merge into:

```text
develop
```

Only after smoke tests pass.

`main` should be updated only after owner review or freeze-ready confirmation.

---

# 26. Commit Message Rules

## 26.1 Required Commit Sequence

Use this sequence for P2-2:

```text
1. chore: initialize ARI V1 monorepo foundation
2. feat(backend): add FastAPI health check and config foundation
3. chore(infra): add local docker stack with postgres minio emqx
4. docs: add coding agent guardrails
5. docs: add P2-2 local development setup guide
```

## 26.2 Commit Style

Use conventional commits:

```text
chore:
feat:
fix:
docs:
test:
refactor:
```

## 26.3 Scope Examples

Allowed scopes:

```text
backend
infra
docs
scripts
repo
```

Examples:

```text
chore(repo): add root folder structure
feat(backend): add health endpoint
chore(infra): add docker compose local services
docs(agents): add AI coding guardrails
docs(execution): add P2-2 setup guide
```

## 26.4 Forbidden Commit Types in P2-2

Do not create commits for:

```text
auth implementation
database schema migration
notebook API
mobile screens
web pages
file upload flow
sync batch
production deployment
```

---

# 27. README Requirements

Root `README.md` must include:

```text
Project name
Repository purpose
Frozen architecture rules
Local prerequisites
Local startup workflow
Local shutdown workflow
Health check commands
Service URLs
What is included in P2-2
What is not included in P2-2
Forbidden services and modules
Link to docs/execution/P2-2
```

## 27.1 README Must State

```text
ARI V1 uses one backend, one database architecture, one mobile app, one web app, one domain model, and one RBAC system.
```

## 27.2 README Must Warn

Do not add:

```text
permission service
QR registry
consultation entity
farm membership table
knowledge graph
vector database
RAG
internal AI assistant
robot module
commerce module
desktop app
```

## 27.3 README Service URLs

README should list:

```text
Backend API:       http://localhost:8000
Root Health:       http://localhost:8000/health
API v1 Health:     http://localhost:8000/api/v1/health
PostgreSQL:        localhost:5432
MinIO API:         http://localhost:9000
MinIO Console:     http://localhost:9001
EMQX MQTT:         localhost:1883
EMQX Dashboard:    http://localhost:18083
```

---

# 28. AGENTS.md / CLAUDE.md / CODEX.md Guardrails

P2-2 must define:

```text
AGENTS.md
CLAUDE.md
CODEX.md
```

## 28.1 Purpose

These files instruct AI coding agents to follow frozen ARI rules.

They prevent coding agents from expanding scope.

## 28.2 Required Shared Guardrails

Each file must include:

```text
Do not redesign ARI.
Do not add new architecture.
Do not add new database tables.
Do not add new RBAC roles.
Do not create QR registry.
Do not create consultation entity.
Do not create farm_memberships.
Do not create permission service.
Do not create knowledge graph.
Do not create vector database.
Do not create RAG system.
Do not create internal AI assistant.
Do not create robot module.
Do not create commerce module.
Follow ARI V1 — P2-1 and P2-2.
If something is missing, mark API Gap / Revision Proposal.
```

## 28.3 AGENTS.md Required Content

`AGENTS.md` should be general for all coding agents.

It must define:

```text
Project rules
Source of Truth order
Allowed P2-2 files
Forbidden files
How to handle missing specs
How to create API Gap notes
Smoke test requirement
```

## 28.4 CLAUDE.md Required Content

`CLAUDE.md` should repeat the same guardrails for Claude-style agents.

It must explicitly warn:

```text
Do not infer missing ARI architecture.
Do not create services because they seem useful.
Do not convert consultation into a separate entity.
Do not convert QR into a registry.
```

## 28.5 CODEX.md Required Content

`CODEX.md` should repeat the same guardrails for Codex-style agents.

It must explicitly warn:

```text
Do not scaffold extra routers.
Do not scaffold feature models.
Do not add migrations.
Do not add worker services.
Do not add AI / robot / commerce modules.
```

---

# 29. Local Startup Workflow

The target local workflow is:

```text
1. Clone repo
2. Copy .env.example to .env
3. Start Docker stack
4. Check backend health
5. Check PostgreSQL container
6. Check MinIO console
7. Check EMQX console
8. Confirm no forbidden service exists
```

## 29.1 Example Commands

```bash
git clone <repo-url> ari
cd ari

cp .env.example .env

docker compose up -d --build

curl http://localhost:8000/health
curl http://localhost:8000/api/v1/health

docker compose ps
```

## 29.2 Expected Health Response

```json
{
  "status": "ok",
  "service": "ari-backend",
  "api": "/api/v1"
}
```

## 29.3 Local Service Checks

```text
PostgreSQL container should be running.
MinIO console should be reachable.
EMQX dashboard should be reachable.
API container should be running.
```

## 29.4 Forbidden Service Check

Confirm `docker compose ps` does not include:

```text
worker
permission
ai
rag
vector
robot
commerce
admin-backend
web-backend
```

---

# 30. Local Shutdown / Reset Workflow

## 30.1 Shutdown

Recommended command:

```bash
docker compose down
```

Purpose:

```text
Stop local containers while preserving volumes.
```

## 30.2 Reset Local Volumes

Recommended command:

```bash
docker compose down -v
```

Purpose:

```text
Remove local data volumes for clean setup.
```

## 30.3 Reset Warning

Resetting volumes deletes local development data.

In P2-2 this is acceptable because no production or pilot data should exist.

## 30.4 Not Allowed

Do not create production reset scripts in P2-2.

Do not create farm server reset scripts in P2-2.

---

# 31. Smoke Test Checklist

P2-2 is complete when:

```text
Repository structure exists
backend/ exists
mobile/ exists
web/ exists
infra/ exists
docs/ exists
scripts/ exists
.env.example exists
docker-compose.yml exists
PostgreSQL / TimescaleDB starts
MinIO starts
EMQX starts
FastAPI backend starts
GET /health works
GET /api/v1/health works
README explains local startup
AGENTS.md exists
CLAUDE.md exists
CODEX.md exists
No forbidden services are introduced
No forbidden database tables are introduced
No feature modules are implemented early
```

## 31.1 Health Check Test

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/health
```

Expected:

```json
{
  "status": "ok",
  "service": "ari-backend",
  "api": "/api/v1"
}
```

## 31.2 Docker Service Test

```bash
docker compose ps
```

Expected services:

```text
api
postgres
minio
emqx
```

Optional:

```text
pgadmin
```

Not expected:

```text
worker
permission-service
ai-service
rag-service
vector-db
robot-service
commerce-service
```

## 31.3 Repository Structure Test

Expected:

```text
backend/
mobile/
web/
infra/
docs/
scripts/
docker-compose.yml
.env.example
README.md
AGENTS.md
CLAUDE.md
CODEX.md
```

---

# 32. Acceptance Criteria

P2-2 is accepted when all of the following are true:

## 32.1 Repository Acceptance

```text
Root folder is ari/
Root structure matches approved P2-2 structure
No apps/ folder is used
backend/, mobile/, web/ are direct root folders
```

## 32.2 Backend Acceptance

```text
FastAPI backend skeleton exists
GET /health works
GET /api/v1/health works
API response matches required JSON
No feature routers are implemented
No feature services are implemented
No database models are implemented
```

## 32.3 Infrastructure Acceptance

```text
docker-compose.yml exists
api service exists
postgres service exists
minio service exists
emqx service exists
PostgreSQL / TimescaleDB starts
MinIO starts
EMQX starts
```

## 32.4 Documentation Acceptance

```text
README.md explains local startup
backend/README.md explains backend skeleton
mobile/README.md states mobile implementation is deferred to P2-8
web/README.md states web implementation is deferred to P2-9
docs/execution/ contains P2-2
AGENTS.md exists
CLAUDE.md exists
CODEX.md exists
```

## 32.5 Guardrail Acceptance

```text
No forbidden service exists
No forbidden module exists
No forbidden database table exists
No forbidden app split exists
No production deployment config exists
No feature work begins early
```

---

# 33. GitHub Issue Breakdown for P2-2

Create GitHub issues only for P2-2 scope.

## 33.1 Required Issues

```text
#1 Initialize ARI monorepo root structure
#2 Add backend initial FastAPI skeleton
#3 Add health endpoints
#4 Add root .env.example
#5 Add docker-compose local stack
#6 Add PostgreSQL / TimescaleDB local service
#7 Add MinIO local service
#8 Add EMQX local service
#9 Add docs/frozen and docs/execution structure
#10 Add scripts/dev placeholders
#11 Add AGENTS.md guardrails
#12 Add CLAUDE.md guardrails
#13 Add CODEX.md guardrails
#14 Add README local startup instructions
#15 Add P2-2 smoke test checklist
```

## 33.2 Issue Labels

Recommended labels:

```text
p2-2
setup
backend
infra
docs
guardrails
smoke-test
no-feature-code
```

## 33.3 Do Not Create P2-2 Issues For

```text
auth
migrations
phone registration
phone login
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
pilot deployment
```

These belong to later P2 documents.

---

# 34. What to Create Now

P2-2 should create only:

```text
ari/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   └── v1/
│   │   │       ├── __init__.py
│   │   │       ├── router.py
│   │   │       └── health.py
│   │   ├── core/
│   │   │   ├── __init__.py
│   │   │   └── config.py
│   │   └── db/
│   │       ├── __init__.py
│   │       ├── base.py
│   │       └── session.py
│   ├── alembic.ini
│   ├── Dockerfile
│   ├── pyproject.toml
│   └── README.md
├── mobile/
│   └── README.md
├── web/
│   └── README.md
├── infra/
│   ├── docker/
│   ├── postgres/
│   ├── minio/
│   └── emqx/
├── docs/
│   ├── frozen/
│   ├── execution/
│   ├── api-gaps/
│   └── decisions/
├── scripts/
│   ├── dev/
│   ├── db/
│   └── deploy/
├── docker-compose.yml
├── .env.example
├── .gitignore
├── README.md
├── AGENTS.md
├── CLAUDE.md
└── CODEX.md
```

## 34.1 Backend Create Now

Create only:

```text
FastAPI app entry
health endpoints
config foundation
database placeholder
Dockerfile
pyproject
README
```

## 34.2 Infrastructure Create Now

Create only:

```text
local Docker stack
postgres container
minio container
emqx container
local env template
```

## 34.3 Documentation Create Now

Create:

```text
P2-2 execution document
README local setup
AI agent guardrails
smoke test checklist
```

---

# 35. What Not to Create Yet

Do not create feature implementation.

## 35.1 Backend Not Yet

Do not create:

```text
auth router
user router
organization router
farm router
zone router
tree router
notebook router
note item router
follow-up router
notification router
upload queue router
file router
sync router
```

Do not create:

```text
models/
schemas/
repositories/
services/
dependencies/rbac.py
```

These begin later.

## 35.2 Database Not Yet

Do not create:

```text
real Alembic migration files
tables
seed data
production database config
```

## 35.3 Mobile Not Yet

Do not create:

```text
Flutter app
mobile screens
phone registration
phone login
offline storage
upload queue
sync logic
Ask AI workflow
```

Deferred:

```text
Mobile MVP → Deferred to P2-8
```

## 35.4 Web Not Yet

Do not create:

```text
Next.js app
dashboard
login page
farm pages
notebook pages
review pages
admin pages
```

Deferred:

```text
Web MVP → Deferred to P2-9
```

## 35.5 Production Not Yet

Do not create:

```text
production Docker Compose
VPS deployment
CI/CD production deploy
SSL setup
domain setup
farm local server setup
```

Deferred:

```text
E2E and prototype deployment → Deferred to P2-10
```

---

# 36. API Gap / Revision Proposal Handling

## 36.1 Rule

If developers discover a missing API detail, missing field, or unclear behavior, they must not silently invent implementation.

They must create:

```text
API Gap / Revision Proposal
```

## 36.2 Location

Store gap notes under:

```text
docs/api-gaps/
```

## 36.3 Naming Convention

Use:

```text
API-GAP-0001-short-title.md
API-GAP-0002-short-title.md
API-GAP-0003-short-title.md
```

## 36.4 Required API Gap Template

```markdown
# API Gap / Revision Proposal

Gap ID:
API-GAP-0001

Title:
<short title>

Discovered In:
P2-2 / P2-3 / P2-4 / etc.

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

## 36.5 P2-2 Expected Gaps

P2-2 should not normally create API gaps because it does not implement feature APIs.

If a gap is found, it must be documented only.

No implementation should proceed without approval.

---

# 37. Freeze Readiness Checklist

P2-2 is ready for owner freeze review when:

```text
[ ] P2-2 document is complete
[ ] Source of Truth list is correct
[ ] Scope is limited to monorepo and local setup
[ ] Non-goals are explicit
[ ] Required root structure uses backend/, mobile/, web/
[ ] backend/ skeleton is limited to health/config/db placeholders
[ ] mobile/ is placeholder only
[ ] web/ is placeholder only
[ ] infra/ is local-only
[ ] docs/ structure is defined
[ ] scripts/ structure is defined
[ ] .env.example groups are defined
[ ] docker-compose local services are limited to api/postgres/minio/emqx
[ ] PostgreSQL / TimescaleDB setup is local-only
[ ] MinIO setup is local-only
[ ] EMQX setup is local-only
[ ] GET /health is defined
[ ] GET /api/v1/health is defined
[ ] Alembic is placeholder only
[ ] Git branch rules are defined
[ ] Commit message rules are defined
[ ] README requirements are defined
[ ] AGENTS.md guardrails are defined
[ ] CLAUDE.md guardrails are defined
[ ] CODEX.md guardrails are defined
[ ] Local startup workflow is defined
[ ] Local shutdown / reset workflow is defined
[ ] Smoke test checklist is defined
[ ] Acceptance criteria are defined
[ ] GitHub issue breakdown is limited to P2-2
[ ] What to create now is explicit
[ ] What not to create yet is explicit
[ ] API Gap / Revision Proposal process is defined
[ ] No forbidden services are introduced
[ ] No forbidden entities are introduced
[ ] No forbidden database tables are introduced
[ ] No feature coding is started early
```

---

# Final P2-2 Boundary Statement

P2-2 creates the ARI V1 local development foundation only.

P2-2 authorizes:

```text
monorepo structure
local Docker stack
FastAPI health skeleton
environment template
documentation
AI coding agent guardrails
smoke test checklist
```

P2-2 does not authorize:

```text
feature APIs
database schema migrations
auth implementation
mobile implementation
web implementation
production deployment
new architecture
new services
new entities
new RBAC roles
```

After P2-2 is reviewed and frozen, the next document should be:

```text
ARI V1 — P2-3 Backend Feature Foundation v1.0
```

Status:

```text
ARI V1 — P2-2 Monorepo & Local Development Setup v1.0
Status: FROZEN
Freeze Confirmation: APPROVED BY OWNER
*******************************************

***************************************************
2026-06-25 : After Claude code build P2-2 completed
***************************************************
P2-2 Document: FROZEN
P2-2 Coding Foundation: IMPLEMENTED
P2-2 Smoke Test: PASS
# ARI V1 — P2-6 Farm Structure Backend v1.0

Project: ARI — Agricultural Intelligence Platform
Phase: P2 Coding Execution Phase
Document Number: P2-6
Document Type: Farm Structure Backend Specification / Execution Document
Version: v1.0
Status: Draft Final / Ready for Owner Review
Prepared From: Frozen Source of Truth + P2-1 / P2-2 / P2-3 / P2-4 / P2-5 Coding Execution Authority
Coding Direction: Backend Foundation First → Database → Auth → Farm Structure → Notebook / Upload / Sync → Mobile MVP → Web MVP → E2E → Prototype Deployment

---

# 1. Document Control

## 1.1 Document Identity

```text
Document Title:
ARI V1 — P2-6 Farm Structure Backend v1.0

Project:
ARI — Agricultural Intelligence Platform

Phase:
P2 Coding Execution Phase

Document Number:
P2-6

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

ARI V1 — P2-4 Database and Alembic Migration Foundation v1.0
Status: FROZEN
Coding Foundation: IMPLEMENTED LOCALLY
Smoke Test: PASS

ARI V1 — P2-5 Auth and Mobile Onboarding Backend v1.0
Status: FROZEN
Coding Foundation: IMPLEMENTED LOCALLY
Smoke Test: PASS
```

## 1.3 P2-5 Implementation Status Note

P2-5 local implementation status is recorded as:

```text
Auth endpoints implemented
Phone registration/login implemented
JWT access/refresh token implemented
Auth guards implemented
157/157 tests passed
alembic upgrade head: PASS
No forbidden scope detected
```

Commit / push / merge status is not assumed in this document.

```text
Owner Confirmation Required:
Confirm whether P2-5 has been committed, pushed, and merged before P2-6 coding implementation starts.
```

## 1.4 Document Boundary

This document defines the Farm Structure Backend implementation scope only.

This document is still a specification / execution document.

This document does not authorize actual coding implementation unless the Owner explicitly instructs implementation later.

This document does not create P2-7.

This document does not redesign ARI.

---

# 2. Purpose

The purpose of P2-6 is to define the backend implementation boundary for the existing frozen Farm Structure domain after Auth and Mobile Onboarding Backend.

P2-6 prepares the backend for:

```text
Farm APIs
Zone APIs
Tree APIs
Farm hierarchy validation
Organization scope validation
Farm scope validation
Owner farm creation
Owner multiple farms
Zone creation under farm
Tree creation under zone
Farm / Zone / Tree read and update
Basic farm list / zone list / tree list
Basic pagination / filtering
Optional farm location usage if already present
Simple organization/farm scope guards
Tests
Smoke checklist
API Gap / Revision Proposal handling
GitHub issue breakdown
```

P2-6 must preserve the frozen identity hierarchy:

```text
Organization
  ↓
Farm
    ↓
Zone
      ↓
Tree
```

P2-6 must not introduce new entities, new tables, new RBAC roles, permission service, farm membership table, QR registry, or location/GIS systems.

---

# 3. Scope

## 3.1 In Scope

P2-6 covers:

```text
Farm router
Zone router
Tree router

Farm schemas
Zone schemas
Tree schemas

Farm repository
Zone repository
Tree repository

Farm service
Zone service
Tree service

Farm hierarchy validation
Organization scope validation
Farm scope validation

Owner farm creation
Owner multiple farm support
Zone creation under farm
Tree creation under zone

Farm list/read/update
Zone list/read/update
Tree list/read/update

Basic pagination
Basic filtering
Basic sorting if already supported by foundation utilities

Optional farms.location field usage if already present

Simple scope guards:
- require_organization_access
- require_farm_access

Tests
Smoke checklist
API Gap / Revision Proposal handling
GitHub issue breakdown
```

## 3.2 Deliverable

The deliverable is a safe Farm Structure Backend execution specification.

Target result after P2-6 coding implementation is explicitly approved:

```text
GET /api/v1/farms works
GET /api/v1/farms/{farm_id} works
POST /api/v1/farms works for owner under own organization
PATCH /api/v1/farms/{farm_id} works within scope

GET /api/v1/zones works
GET /api/v1/zones/{zone_id} works
POST /api/v1/zones works under accessible farm for allowed user
PATCH /api/v1/zones/{zone_id} works within scope

GET /api/v1/trees works
GET /api/v1/trees/{tree_id} works
POST /api/v1/trees works under accessible zone/farm for allowed user
PATCH /api/v1/trees/{tree_id} works within scope

Pending membership users are blocked from protected farm structure access
Owner family / farm staff cannot create Farm / Zone / Tree
Owner can create multiple farms under own organization
Owner cannot create farm under another organization
Health endpoints remain unchanged
Alembic upgrade head remains PASS
No new database tables are introduced
No new RBAC roles are introduced
No Notebook / Upload / Sync implementation is introduced
Tests pass
```

## 3.3 Scope Principle

P2-6 implements only the Farm Structure Backend layer.

P2-6 may touch:

```text
Router Layer
Service Layer
Repository Layer
Dependency Layer
Schema Layer
Test Layer
```

P2-6 must use the existing frozen database tables:

```text
farms
zones
trees
```

P2-6 must not create or modify database schema unless the Owner explicitly approves a separate migration or revision.

---

# 4. Source of Truth

## 4.1 Frozen Source Documents

P2-6 must follow:

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
ARI V1 — P2-4 Database and Alembic Migration Foundation v1.0
ARI V1 — P2-5 Auth and Mobile Onboarding Backend v1.0
```

## 4.2 Frozen Architecture Rules

P2-6 must preserve:

```text
One Platform
One Backend
One Database Architecture
One Mobile App
One Web App
One Domain Model
One RBAC System
```

P2-6 must not introduce:

```text
Separate farmer app
Separate staff app
Separate admin backend
Separate web backend
New database architecture
New RBAC role
Permission service
Permission matrix engine
ABAC
Policy engine
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

If a frozen detail is missing, unclear, or inconsistent, developers must not invent behavior.

They must create:

```text
API Gap / Revision Proposal
```

and continue only with approved scope.

---

# 5. Relationship to P2-1 through P2-5

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

P2-6 corresponds to:

```text
Farm structure
```

P2-6 is still before:

```text
Notebook APIs
Note Item APIs
File Upload APIs
Upload Queue APIs
Offline Sync APIs
Mobile MVP
Web MVP
E2E
Prototype deployment
```

## 5.2 Relationship to P2-2

P2-2 created:

```text
Monorepo
Local Docker stack
Initial FastAPI skeleton
Health endpoints
Environment template
Repository documentation
AI coding agent guardrails
Git workflow
Smoke test checklist
```

P2-6 must preserve:

```text
GET /health
GET /api/v1/health
api
postgres
minio
emqx
```

P2-6 must not change local stack architecture.

## 5.3 Relationship to P2-3

P2-3 created backend feature foundation:

```text
Common response foundation
Common error foundation
Logging foundation
CORS foundation
Request ID middleware foundation
Configuration foundation
Database dependency placeholder
Repository base pattern
Service base pattern
Common schemas
Generic utilities
Foundation tests
```

P2-6 must use the existing foundation patterns.

P2-6 must not bypass:

```text
Router Layer
Service Layer
Repository Layer
Database Layer
```

## 5.4 Relationship to P2-4

P2-4 created the database and Alembic foundation:

```text
SQLAlchemy models
Frozen database tables
Alembic env
Initial frozen schema migration
Frozen Python enums
Indexes and constraints
Nullable hierarchy rules
UTC timestamp rules
User additive fields from P0 v1.1
Phone uniqueness
registered_at
```

P2-6 may read/write only:

```text
farms
zones
trees
```

P2-6 may read:

```text
organizations
users
roles / user_roles only if already confirmed
```

P2-6 must not create new migrations unless Owner explicitly approves.

## 5.5 Relationship to P2-5

P2-5 created:

```text
Phone registration
Phone login
JWT access token
JWT refresh token
GET /api/v1/auth/me
POST /api/v1/auth/logout boundary
Owner registration
Owner family registration
Farm staff registration
Farm ID join validation
Account status guard
Membership status guard
Basic auth dependencies
Password hashing
Phone normalization
```

P2-6 may use existing P2-5 dependencies:

```text
get_current_user
require_authenticated_user
require_active_account
require_active_membership
```

P2-6 may add simple scope guards:

```text
require_organization_access
require_farm_access
```

These guards must remain FastAPI dependency guards only.

They must not become:

```text
Permission service
Permission matrix
ABAC
Policy engine
Farm membership service
Approval workflow service
```

---

# 6. Current Backend State

## 6.1 Confirmed Local Services

```text
api
postgres
minio
emqx
```

## 6.2 Confirmed Health Endpoints

```text
GET /health
GET /api/v1/health
```

## 6.3 Confirmed Backend Foundation

```text
Common response foundation
Common error foundation
Logging foundation
CORS foundation
Request ID middleware foundation
Configuration foundation
Database dependency
Repository base pattern
Service base pattern
Common schemas
Generic utilities
Foundation tests
```

## 6.4 Confirmed Database Foundation

```text
Frozen SQLAlchemy models
Frozen Alembic migration
Frozen enums
Frozen tables
No forbidden tables
UTC timestamp rules
User additive onboarding fields
```

## 6.5 Confirmed Auth Foundation

```text
Auth router
Auth schemas
Auth service
Auth dependencies
Phone registration/login
JWT issuing
Current user retrieval
Account status guard
Membership status guard
```

---

# 7. Farm Structure Domain Boundary

## 7.1 Existing Domain Entities

P2-6 may use only the existing frozen Farm Structure entities:

```text
Farm
Zone
Tree
```

## 7.2 Required Hierarchy

```text
Organization
  ↓
Farm
    ↓
Zone
      ↓
Tree
```

## 7.3 Ownership Principle

```text
Organization owns data.
Users create data.
```

Farm records belong to Organization.

Zone records belong to Farm.

Tree records belong to Zone.

## 7.4 No New Entity Rule

P2-6 must not create:

```text
Farm Membership Entity
Owner Registry
Member Registry
Farmer Registry
Block Registry
Location Entity
GIS Entity
QR Registry
Permission Entity
Audit Entity
```

## 7.5 Zone as Block Rule

If UI or users refer to:

```text
Block
```

P2-6 must map this concept to:

```text
Zone
```

No Block API or Block table is allowed.

---

# 8. Farm API Scope

## 8.1 Allowed Endpoints

```http
GET /api/v1/farms
GET /api/v1/farms/{farm_id}
POST /api/v1/farms
PATCH /api/v1/farms/{farm_id}
```

Conditional only if frozen model and implemented status field support it:

```http
PATCH /api/v1/farms/{farm_id}/archive
```

If `archived` status is not clearly supported by the frozen enum/model, do not implement archive. Create API Gap.

## 8.2 GET /api/v1/farms

Purpose:

```text
Return farms visible to current user within allowed organization/farm scope.
```

Allowed query parameters:

```text
organization_id
status
page
page_size
sort_by
sort_order
q
is_simulator only if field already exists
```

Rules:

```text
Authenticated user required.
Active account required.
Active membership required for protected farm access.
User must not list farms outside accessible organization scope.
Owner sees farms under own organization.
owner_family/farm_staff may see approved farm scope only after membership_status = active.
primary_farm_id alone does not grant access.
```

If `is_simulator` field does not exist, do not implement simulator filter. Create API Gap.

## 8.3 GET /api/v1/farms/{farm_id}

Purpose:

```text
Return one farm if user has access to that farm.
```

Rules:

```text
Validate farm_id UUID.
Load farm.
Validate organization scope.
Validate farm access.
Return 404 if farm does not exist.
Return 403 or 404 consistently if farm exists but is outside scope.
```

## 8.4 POST /api/v1/farms

Purpose:

```text
Allow owner to create Farm under own Organization.
```

Owner request body:

```json
{
  "farm_name": "สวนทุเรียนคลองสิบ",
  "location": {
    "province": "จันทบุรี",
    "district": "ท่าใหม่",
    "subdistrict": "เขาบายศรี",
    "address": "ใกล้วัด เข้าซอย 2 กม.",
    "gps_latitude": 12.345678,
    "gps_longitude": 102.345678,
    "source": "device_gps"
  },
  "description": "สวนหลักของครอบครัว"
}
```

Required from user:

```text
farm_name
```

Optional from user:

```text
location only if farms.location exists in implemented schema
description
```

System generated / system assigned:

```text
farm_id
organization_id
created_by_user_id if field exists
status
created_at
updated_at if field exists
farm_code only if field already exists and approved behavior is clear
```

Owner must not manually provide:

```text
farm_id
organization_id
created_by_user_id
status
farm_code
created_at
updated_at
```

Authorization rules:

```text
farmer_status = owner
membership_status = active
account_status must pass active account guard
organization_id = current_user.organization_id
```

Owner rules:

```text
Owner may create multiple farms.
Owner primary_farm_id may be null.
Owner cannot create farm under another organization.
Owner cannot create Farm for another owner.
```

Blocked:

```text
owner_family cannot create Farm.
farm_staff cannot create Farm.
pending_farm_approval users cannot create Farm.
rejected/suspended/revoked users cannot create Farm.
```

## 8.5 PATCH /api/v1/farms/{farm_id}

Purpose:

```text
Update basic farm fields within allowed scope.
```

Allowed fields if present in frozen model:

```text
farm_name
location only if farms.location exists in implemented schema
description
status only if frozen status transition is clear
```

Rules:

```text
Validate farm_id UUID.
Validate farm exists.
Validate farm belongs to current user's accessible organization.
Only owner of own organization or approved admin/root/scoped role may update.
Do not allow organization_id change.
Do not allow created_by_user_id change.
Do not allow farm_id change.
Do not allow farm_code change unless Owner approves a separate rule.
```

If status transitions are unclear, restrict update to:

```text
farm_name
location
description
```

and create API Gap for status behavior.

## 8.6 PATCH /api/v1/farms/{farm_id}/archive

Conditional endpoint.

Allowed only if frozen schema clearly supports:

```text
status = archived
```

or equivalent archive behavior.

Rules:

```text
Do not hard delete farm.
Do not cascade delete zones/trees/notebook records.
Do not introduce deleted_at unless already frozen.
Do not add archive migration silently.
```

If unsupported, create:

```text
API-GAP-P2-6-001 — Farm archive status unclear or unsupported.
```

---

# 9. Zone API Scope

## 9.1 Allowed Endpoints

```http
GET /api/v1/zones
GET /api/v1/zones/{zone_id}
POST /api/v1/zones
PATCH /api/v1/zones/{zone_id}
```

## 9.2 GET /api/v1/zones

Purpose:

```text
Return zones visible to current user.
```

Allowed query parameters:

```text
farm_id
page
page_size
sort_by
sort_order
q
status only if field exists
```

Rules:

```text
Authenticated user required.
Active account required.
Active membership required.
If farm_id is provided, validate farm exists and user has farm access.
If farm_id is not provided, return zones under farms visible to user.
Do not return zones under inaccessible farms.
```

## 9.3 GET /api/v1/zones/{zone_id}

Purpose:

```text
Return one zone if user has access to parent farm.
```

Rules:

```text
Validate zone_id UUID.
Load zone.
Load parent farm.
Validate farm access.
Return 404 if zone does not exist.
Return 403 or 404 consistently if outside scope.
```

## 9.4 POST /api/v1/zones

Purpose:

```text
Create Zone under an accessible Farm.
```

Request body:

```json
{
  "farm_id": "uuid",
  "zone_name": "North Zone",
  "description": "optional"
}
```

Required:

```text
farm_id
zone_name
```

Optional:

```text
description
```

System generated:

```text
zone_id
created_at
updated_at if field exists
```

Rules:

```text
Validate farm_id UUID.
Validate farm exists.
Validate farm belongs to current user's accessible organization.
Only owner under own organization or approved admin/root/scoped role may create zone.
owner_family cannot create Zone.
farm_staff cannot create Zone.
Do not create Zone under inaccessible Farm.
```

## 9.5 PATCH /api/v1/zones/{zone_id}

Purpose:

```text
Update basic zone fields within allowed farm scope.
```

Allowed fields if present in frozen model:

```text
zone_name
description
status only if field exists and behavior is clear
```

Rules:

```text
Validate zone_id UUID.
Load zone and parent farm.
Validate farm access.
Do not allow farm_id reassignment unless explicitly approved later.
Do not allow zone_id change.
```

If moving a zone to another farm is needed later, create API Gap. Do not implement silently.

---

# 10. Tree API Scope

## 10.1 Allowed Endpoints

```http
GET /api/v1/trees
GET /api/v1/trees/{tree_id}
POST /api/v1/trees
PATCH /api/v1/trees/{tree_id}
```

## 10.2 GET /api/v1/trees

Purpose:

```text
Return trees visible to current user.
```

Allowed query parameters:

```text
zone_id
farm_id optional if implementation can safely join through zone
status
page
page_size
sort_by
sort_order
q
```

Rules:

```text
Authenticated user required.
Active account required.
Active membership required.
If zone_id is provided, validate zone exists and user has access to parent farm.
If farm_id is provided, validate farm access and return trees under zones in that farm.
Do not return trees under inaccessible farms.
```

## 10.3 GET /api/v1/trees/{tree_id}

Purpose:

```text
Return one tree if user has access to parent zone/farm.
```

Rules:

```text
Validate tree_id UUID.
Load tree.
Load parent zone.
Load parent farm.
Validate farm access.
Return 404 if tree does not exist.
Return 403 or 404 consistently if outside scope.
```

## 10.4 POST /api/v1/trees

Purpose:

```text
Create Tree under an accessible Zone.
```

Request body:

```json
{
  "zone_id": "uuid",
  "tree_code": "T-001",
  "status": "active"
}
```

Required:

```text
zone_id
tree_code
```

Optional if frozen model supports:

```text
status
```

System generated:

```text
tree_id
created_at
updated_at if field exists
```

Rules:

```text
Validate zone_id UUID.
Validate zone exists.
Validate parent farm access.
Only owner under own organization or approved admin/root/scoped role may create tree.
owner_family cannot create Tree.
farm_staff cannot create Tree.
Do not create Tree under inaccessible Zone.
Tree registration remains optional in P0.
```

## 10.5 PATCH /api/v1/trees/{tree_id}

Purpose:

```text
Update basic tree fields within allowed zone/farm scope.
```

Allowed fields if present in frozen model:

```text
tree_code
status
description only if field exists
```

Rules:

```text
Validate tree_id UUID.
Load tree, parent zone, parent farm.
Validate farm access.
Do not allow zone_id reassignment unless explicitly approved later.
Do not allow tree_id change.
```

If moving a tree to another zone is needed later, create API Gap. Do not implement silently.

---

# 11. Authorization Boundary

## 11.1 Existing P2-5 Guards

P2-6 may use:

```text
get_current_user
require_authenticated_user
require_active_account
require_active_membership
```

## 11.2 New P2-6 Simple Scope Guards

P2-6 may add:

```text
require_organization_access
require_farm_access
```

Optional if simple enough and needed:

```text
require_owner_farmer_status
require_farm_structure_write_access
```

These must remain FastAPI dependency guards.

## 11.3 Guard Responsibilities

### require_organization_access

Responsibilities:

```text
Validate organization exists.
Validate current user may access organization.
Allow root/admin/ari_staff only according to frozen role/scope rules.
Allow farmer owner only for own organization.
Block access to other organizations.
```

### require_farm_access

Responsibilities:

```text
Validate farm exists.
Validate farm belongs to accessible organization.
Validate membership_status = active for farm-scoped access.
Validate owner/approved user scope.
Block pending/rejected/suspended/revoked users.
```

### require_farm_structure_write_access

Responsibilities:

```text
Allow owner to create/update Farm/Zone/Tree within own organization.
Block owner_family.
Block farm_staff.
Allow admin/root/scoped roles only if existing RBAC guard permits.
Do not create new RBAC roles.
```

## 11.4 Not Allowed

P2-6 must not create:

```text
Permission service
Permission matrix engine
ABAC
Policy engine
Authorization microservice
Dedicated permission tables
Permission APIs
Farm membership service
Approval workflow service
```

---

# 12. Farmer Status / RBAC Rule

Frozen RBAC roles remain:

```text
farmer
ari_staff
farm_coordinator
agronomist
reviewer
admin
root
```

Do not create RBAC roles:

```text
owner
owner_family
farm_staff
```

These are:

```text
farmer_status values only
```

## 12.1 owner

```text
farmer_status = owner
membership_status = active
account_status = active_pending_verification or active
primary_farm_id may be null
```

Allowed in P2-6:

```text
Create Farm under own Organization
Create multiple Farms
List/read/update own Organization farms
Create Zone under own Farm
Create Tree under own Zone
```

Blocked:

```text
Create Farm under another Organization
Access another Organization
Create admin/root/ari_staff users
Bypass backend scope guards
```

## 12.2 owner_family

```text
farmer_status = owner_family
primary_farm_id = provided farm_id from onboarding/default context
```

Rules:

```text
Cannot create Farm
Cannot create Zone
Cannot create Tree
primary_farm_id does not grant farm access by itself
membership_status must be active before protected farm structure access
pending_farm_approval blocks farm structure access
```

## 12.3 farm_staff

```text
farmer_status = farm_staff
primary_farm_id = provided farm_id from onboarding/default context
```

Rules:

```text
Cannot create Farm
Cannot create Zone
Cannot create Tree
primary_farm_id does not grant farm access by itself
membership_status must be active before protected farm structure access
pending_farm_approval blocks farm structure access
```

---

# 13. Membership Approval Boundary

P2-6 must enforce membership access status.

P2-6 does not implement full member approval workflow unless already explicitly supported by existing User APIs.

## 13.1 Required Enforcement

Before approval:

```text
membership_status = pending_farm_approval
```

must block:

```text
Farm data read access
Farm/Zone/Tree creation
Farm/Zone/Tree update
Farm notebook access
Farm-scoped upload/sync
```

P2-6 only covers Farm/Zone/Tree blocking.

Notebook/upload/sync blocking remains for later documents.

## 13.2 Allowed Before Approval

Backend may allow:

```text
GET /api/v1/auth/me
POST /api/v1/auth/logout
status refresh
profile read if already implemented
```

## 13.3 Approval Endpoint Boundary

P2-6 does not implement full membership approval workflow.

If an existing User API already supports membership status update, it may be referenced as the preferred future/admin path:

```http
PATCH /api/v1/users/{user_id}
```

Allowed transition examples:

```json
{
  "membership_status": "active"
}
```

```json
{
  "membership_status": "rejected"
}
```

Allowed approvers only if already supported by existing RBAC guards:

```text
admin
root
ari_staff if explicitly permitted
```

If no approved endpoint exists, create:

```text
API-GAP-P2-6-002 — Membership approval endpoint shape missing.
```

Do not create:

```text
approval service
farm_membership table
member registry
owner registry
permission workflow engine
```

Possible future-approved approach must use existing:

```text
users.membership_status
users.primary_farm_id
existing RBAC guards
```

---

# 14. Farm Location Boundary

## 14.1 Allowed

`farms.location` may be used only if it already exists in the implemented P2-4 schema.

If `farms.location` JSONB exists:

```text
Accept location in POST /api/v1/farms.
Return location in FarmRead.
Allow location update in PATCH /api/v1/farms/{farm_id}.
```

Recommended structure:

```json
{
  "province": "",
  "district": "",
  "subdistrict": "",
  "address": "",
  "gps_latitude": 0,
  "gps_longitude": 0,
  "source": "device_gps"
}
```

## 14.2 Validation

Basic validation only:

```text
location must be nullable.
location must be JSON object if provided.
gps_latitude must be numeric and between -90 and 90 if provided.
gps_longitude must be numeric and between -180 and 180 if provided.
source must be string if provided.
```

Do not implement advanced GIS validation.

## 14.3 Missing Field Rule

If `farms.location` is missing from current database implementation, do not silently add migration.

Create:

```text
API-GAP-P2-6-003 — farms.location field missing or inconsistent.
```

## 14.4 Not Allowed

P2-6 must not create:

```text
location table
farm_location table
GIS service
Farm boundary mapping
Zone boundary mapping
Tree GPS mapping
Spatial indexing
Geofence service
Map tile service
```

---

# 15. Farm Code Boundary

## 15.1 Conditional Support Only

`farm_code` must not be required for P2-6 implementation unless it already exists in the implemented P2-4 database schema.

Rules:

```text
farm_id remains the canonical Farm identifier.
farm_code, if present, is display-only / read-only.
Do not add farm_code column silently.
Do not generate farm_code unless the field already exists or Owner approves a Revision Proposal.
Do not use farm_code as the canonical database identity.
```

## 15.2 Join Reference Rule

For P2-6 backend scope:

```text
farm_id remains the safe canonical join reference.
```

If later UX requires a human-friendly Farm Code, that must be handled only if the field already exists or through Owner-approved revision.

## 15.3 API Gap

Create:

```text
API-GAP-P2-6-007 — farm_code generation/storage unclear
```

Trigger:

```text
Farm Code is required for UX or member join flow but farm_code is missing or unclear in implemented schema.
```

Handling:

```text
Do not add farm_code column silently.
Do not add migration silently.
Continue with farm_id as canonical identifier.
Create Revision Proposal for farm_code if Owner wants human-friendly farm display/join code.
```

---

# 16. Repository / Service / Router Pattern

P2-6 must preserve the backend layered pattern:

```text
Router Layer
↓
Service Layer
↓
Repository Layer
↓
Database Layer
```

## 16.1 Router Layer

Routers may include:

```text
backend/app/api/v1/farms.py
backend/app/api/v1/zones.py
backend/app/api/v1/trees.py
```

Responsibilities:

```text
Define HTTP endpoints
Declare request/response schemas
Use dependency guards
Call service layer
Return standard response envelope
```

Routers must not:

```text
Run SQL directly
Implement hierarchy validation directly
Implement business rules directly
Bypass services
```

## 16.2 Service Layer

Services may include:

```text
backend/app/services/farm_service.py
backend/app/services/zone_service.py
backend/app/services/tree_service.py
```

Responsibilities:

```text
Apply frozen domain rules
Validate organization/farm/zone/tree hierarchy
Apply scope rules
Orchestrate repository calls
Handle conflicts
Handle not found / forbidden decisions
```

Services must not:

```text
Become permission service
Become approval workflow service
Create new domain modules
Call notebook/upload/sync logic
```

## 16.3 Repository Layer

Repositories may include:

```text
backend/app/repositories/farms.py
backend/app/repositories/zones.py
backend/app/repositories/trees.py
```

Responsibilities:

```text
SQLAlchemy query construction
CRUD for farms/zones/trees
Filtering
Pagination
Parent lookup joins
Uniqueness/conflict checks if supported
```

Repositories must not:

```text
Interpret JWT
Implement RBAC
Call external services
Contain HTTP-specific logic
```

## 16.4 Dependency Layer

Dependencies may include:

```text
backend/app/dependencies/scope.py
```

Allowed additions:

```text
require_organization_access
require_farm_access
```

Do not add:

```text
permissions.py if it implies permission engine
policy.py
abac.py
farm_membership.py
```

---

# 17. Schema Requirements

## 17.1 Farm Schemas

Allowed schemas:

```text
FarmCreate
FarmUpdate
FarmRead
FarmListParams
FarmListResponse
```

### FarmCreate

```text
farm_name: required
location: optional, only if farms.location exists
description: optional
```

Forbidden input fields for owner create:

```text
farm_id
organization_id
created_by_user_id
status
farm_code
created_at
updated_at
```

### FarmUpdate

```text
farm_name: optional
location: optional, only if farms.location exists
description: optional
status: optional only if frozen behavior is clear
```

Forbidden update fields:

```text
farm_id
organization_id
created_by_user_id
farm_code unless explicitly approved
created_at
```

### FarmRead

Return fields only if present in frozen model / implementation:

```text
farm_id
organization_id
farm_name
farm_code only if field exists
location
description
status
created_at
updated_at
```

## 17.2 Zone Schemas

Allowed schemas:

```text
ZoneCreate
ZoneUpdate
ZoneRead
ZoneListParams
ZoneListResponse
```

### ZoneCreate

```text
farm_id: required
zone_name: required
description: optional
```

### ZoneUpdate

```text
zone_name: optional
description: optional
status: optional only if field exists and behavior is clear
```

Forbidden update fields:

```text
zone_id
farm_id unless explicitly approved later
created_at
```

### ZoneRead

```text
zone_id
farm_id
zone_name
description
status if field exists
created_at
updated_at if field exists
```

## 17.3 Tree Schemas

Allowed schemas:

```text
TreeCreate
TreeUpdate
TreeRead
TreeListParams
TreeListResponse
```

### TreeCreate

```text
zone_id: required
tree_code: required
status: optional if frozen model supports
```

### TreeUpdate

```text
tree_code: optional
status: optional
description: optional only if field exists
```

Forbidden update fields:

```text
tree_id
zone_id unless explicitly approved later
created_at
```

### TreeRead

```text
tree_id
zone_id
tree_code
status
created_at
updated_at if field exists
```

## 17.4 Response Envelope

Use existing common response foundation.

Single item response:

```json
{
  "data": {}
}
```

List response:

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

Error response:

```json
{
  "error": {
    "code": "string",
    "message": "string"
  }
}
```

---

# 18. Validation Rules

## 18.1 UUID Validation

All path IDs and FK IDs must be valid UUID:

```text
farm_id
zone_id
tree_id
organization_id
```

## 18.2 Hierarchy Validation

```text
Farm must belong to Organization.
Zone must belong to Farm.
Tree must belong to Zone.
```

When checking tree access:

```text
Tree
↓
Zone
↓
Farm
↓
Organization
```

must be consistent.

When checking zone access:

```text
Zone
↓
Farm
↓
Organization
```

must be consistent.

## 18.3 Organization Scope Validation

Rules:

```text
current_user.organization_id must match target farm.organization_id for owner/farmer scope.
root/admin/ari_staff scope may be broader only if existing RBAC guard supports it.
Owner cannot manually override organization_id.
```

## 18.4 Farm Scope Validation

Rules:

```text
User must have access to parent farm before reading zones/trees.
Active membership required for protected farm structure access.
primary_farm_id is only default context, not access grant.
```

## 18.5 Create Validation

### Farm

```text
farm_name required
organization_id assigned from current_user
owner only for self-service farm creation
location only if farms.location exists
farm_code not accepted from client
```

### Zone

```text
farm_id required
zone_name required
parent farm must be accessible
```

### Tree

```text
zone_id required
tree_code required
parent zone/farm must be accessible
```

## 18.6 Update Validation

```text
Cannot move Farm to another Organization.
Cannot move Zone to another Farm unless approved later.
Cannot move Tree to another Zone unless approved later.
Cannot hard delete.
Cannot change immutable IDs.
Cannot change farm_code unless Owner approves a separate rule.
```

## 18.7 Pagination Validation

```text
page default = 1
page_size default = 20
page_size maximum = 100
sort_order allowed = asc / desc
```

If common pagination utility already exists, use it.

If pagination helper is missing, implement minimal local-safe helper or create API Gap depending on P2-3 foundation status.

---

# 19. Error Handling

P2-6 must use existing common error foundation.

## 19.1 Standard HTTP Errors

```text
400 Bad Request
401 Unauthorized
403 Forbidden
404 Not Found
409 Conflict
422 Validation Error
500 Internal Server Error
```

## 19.2 Suggested Error Codes

```text
invalid_uuid
not_authenticated
account_blocked
membership_not_active
farm_not_found
zone_not_found
tree_not_found
organization_not_accessible
farm_not_accessible
parent_farm_not_found
parent_zone_not_found
farm_create_forbidden
zone_create_forbidden
tree_create_forbidden
duplicate_farm_name
duplicate_zone_name
duplicate_tree_code
validation_error
internal_error
```

## 19.3 Not Found vs Forbidden

Recommended handling:

```text
404 when resource does not exist.
403 when resource exists but current user lacks scope.
```

If avoiding resource existence leakage is required later, create API Gap and standardize behavior.

## 19.4 Conflict Handling

Potential conflicts:

```text
Duplicate farm_name within organization if uniqueness exists.
Duplicate zone_name within farm if uniqueness exists.
Duplicate tree_code within zone if uniqueness exists.
```

If uniqueness constraints do not exist in frozen schema, do not invent database constraints silently.

Use service-level validation only if safe, and create API Gap for database constraint decision.

---

# 20. Database Boundary

## 20.1 Read/Write Tables

P2-6 may read/write only:

```text
farms
zones
trees
```

## 20.2 Read-Only Tables

P2-6 may read:

```text
organizations
users
roles
user_roles
```

only as needed for scope validation and only if already present in implemented schema.

## 20.3 No New Tables

P2-6 must not create:

```text
farm_memberships
permissions
permission_matrix
owner_registry
member_registry
farmer_registry
block_registry
qr_registry
locations
farm_locations
gis_layers
audit_logs
knowledge_assets
vectors
consultations
```

## 20.4 No Silent Migration Rule

If required fields are missing, do not create migration silently.

Create API Gap / Revision Proposal.

Examples:

```text
farms.location missing
farm_code missing
archived status missing
is_simulator missing
created_by_user_id missing
status enum unclear
unique constraints unclear
```

## 20.5 UTC Timestamp Rule

P2-6 must preserve UTC storage.

```text
Store timestamps in UTC.
Use existing datetime utility if available.
Do not introduce farm-local timezone logic.
```

---

# 21. API Gap / Revision Proposal Handling

## 21.1 Required Process

When a missing or unclear frozen detail appears:

```text
1. Stop expanding scope.
2. Implement only safe confirmed behavior.
3. Record API Gap / Revision Proposal.
4. Ask Owner for approval before schema/API expansion.
```

## 21.2 Expected P2-6 API Gaps

### API-GAP-P2-6-001 — Farm Archive Behavior

Trigger:

```text
PATCH /api/v1/farms/{farm_id}/archive is requested but archived status is missing or unclear.
```

Handling:

```text
Do not implement archive.
Do not hard delete.
Keep PATCH farm basic update only.
```

### API-GAP-P2-6-002 — Membership Approval Endpoint Shape

Trigger:

```text
Owner/Admin approval of pending_farm_approval users is required but no approved endpoint exists.
```

Handling:

```text
Do not create approval service.
Do not create farm_membership table.
Use users.membership_status only after approved revision.
```

### API-GAP-P2-6-003 — farms.location Missing

Trigger:

```text
Farm location is needed but farms.location JSONB is not in current schema.
```

Handling:

```text
Do not add migration silently.
Create revision proposal.
```

### API-GAP-P2-6-004 — Simulator Farm Filter Missing

Trigger:

```text
is_simulator filter is requested but field does not exist.
```

Handling:

```text
Do not add simulator field silently.
Return normal farm list.
Create gap if filter is required.
```

### API-GAP-P2-6-005 — Delete vs Archive

Trigger:

```text
Client asks for delete behavior.
```

Handling:

```text
Hard delete is not allowed.
Archive only if frozen status supports it.
Otherwise create gap.
```

### API-GAP-P2-6-006 — Farm/Zone/Tree Uniqueness

Trigger:

```text
Duplicate prevention behavior is required but database constraints are unclear.
```

Handling:

```text
Do not add constraints silently.
Use safe service-level validation only if existing fields support it.
Create gap for long-term DB constraint.
```

### API-GAP-P2-6-007 — farm_code Generation / Storage Unclear

Trigger:

```text
Farm Code is required for UX or member join flow but farm_code is missing or unclear in implemented schema.
```

Handling:

```text
Do not add farm_code column silently.
Do not add migration silently.
Do not generate farm_code unless field already exists or Owner approves Revision Proposal.
Continue with farm_id as canonical identifier.
Create Revision Proposal for farm_code if Owner wants human-friendly farm display/join code.
```

---

# 22. Testing Requirements

## 22.1 Test Categories

P2-6 implementation must include:

```text
Unit tests
Service tests
Repository tests
API tests
Authorization tests
Hierarchy validation tests
Error handling tests
Forbidden scope tests
Smoke tests
```

## 22.2 Farm API Tests

Required tests:

```text
Owner can create farm under own organization.
Owner can create multiple farms.
Owner cannot provide organization_id for self-service create.
Owner cannot provide farm_code for self-service create.
Owner cannot create farm under another organization.
owner_family cannot create farm.
farm_staff cannot create farm.
pending_farm_approval user cannot list/read protected farm data.
GET /farms returns only accessible farms.
GET /farms/{farm_id} blocks inaccessible farm.
PATCH /farms/{farm_id} updates allowed fields.
PATCH /farms/{farm_id} blocks organization_id change.
PATCH /farms/{farm_id} blocks farm_code change unless explicitly approved.
```

## 22.3 Zone API Tests

Required tests:

```text
Owner can create zone under own farm.
Owner cannot create zone under another user's farm.
owner_family cannot create zone.
farm_staff cannot create zone.
GET /zones filters by accessible farm_id.
GET /zones/{zone_id} validates parent farm access.
PATCH /zones/{zone_id} updates allowed fields.
PATCH /zones/{zone_id} cannot move zone to another farm.
```

## 22.4 Tree API Tests

Required tests:

```text
Owner can create tree under own zone.
Owner cannot create tree under inaccessible zone.
owner_family cannot create tree.
farm_staff cannot create tree.
GET /trees filters by accessible zone_id.
GET /trees/{tree_id} validates zone/farm access.
PATCH /trees/{tree_id} updates allowed fields.
PATCH /trees/{tree_id} cannot move tree to another zone.
```

## 22.5 Guard Tests

Required tests:

```text
require_authenticated_user returns 401 when token missing/invalid.
require_active_account returns 403 for blocked account_status.
require_active_membership returns 403 for pending/rejected/suspended/revoked.
require_organization_access blocks other organization.
require_farm_access blocks inaccessible farm.
```

## 22.6 Location Tests

If farms.location exists:

```text
POST /farms accepts valid location object.
PATCH /farms/{farm_id} accepts valid location update.
Invalid latitude is rejected.
Invalid longitude is rejected.
Non-object location is rejected.
```

If farms.location does not exist:

```text
Location is not accepted silently.
API Gap is recorded.
No migration is generated.
```

## 22.7 Farm Code Tests

If farm_code exists:

```text
FarmRead may return farm_code.
Client cannot manually set farm_code.
Client cannot update farm_code.
farm_code remains read-only.
```

If farm_code does not exist:

```text
Farm APIs still work using farm_id.
No farm_code migration is generated.
API Gap is recorded if UX requires farm_code.
```

## 22.8 Database Boundary Tests

Required tests:

```text
No new tables created.
Forbidden tables absent.
Alembic upgrade head passes.
Farm/Zone/Tree CRUD uses existing tables.
Health endpoints still pass.
```

Forbidden table checks must include:

```text
farm_memberships
permissions
owner_registry
member_registry
farmer_registry
block_registry
qr_registry
locations
farm_locations
audit_logs
knowledge_assets
vectors
consultations
```

## 22.9 Regression Tests

P2-6 must not break P2-5 auth tests.

Required regression:

```text
Auth registration still passes.
Auth login still passes.
GET /api/v1/auth/me still passes.
JWT guard still works.
157/157 previous tests or updated total test suite passes.
```

---

# 23. Smoke Test Checklist

After P2-6 coding implementation is explicitly approved and completed, run:

## 23.1 Environment Smoke

```bash
docker compose up -d
docker compose ps
```

Expected services:

```text
api
postgres
minio
emqx
```

## 23.2 Health Smoke

```bash
curl http://localhost:8000/health
curl http://localhost:8000/api/v1/health
```

Expected:

```text
PASS
```

## 23.3 Migration Smoke

```bash
cd backend
alembic upgrade head
```

Expected:

```text
PASS
```

## 23.4 Test Smoke

```bash
cd backend
pytest
```

Expected:

```text
PASS
```

## 23.5 Auth Regression Smoke

```text
Register owner
Login owner
GET /api/v1/auth/me
```

Expected:

```text
PASS
```

## 23.6 Farm Structure Smoke

```text
Owner creates Farm.
Owner creates second Farm.
Owner lists own Farms.
Owner reads own Farm.
Owner updates own Farm.
Owner creates Zone under own Farm.
Owner lists Zones by farm_id.
Owner creates Tree under own Zone.
Owner lists Trees by zone_id.
```

Expected:

```text
PASS
```

## 23.7 Negative Scope Smoke

```text
owner_family cannot create Farm.
farm_staff cannot create Farm.
pending_farm_approval user cannot read Farm.
owner cannot create Farm under another organization.
owner cannot create Zone under inaccessible Farm.
owner cannot create Tree under inaccessible Zone.
```

Expected:

```text
PASS
```

## 23.8 Conditional Boundary Smoke

If farms.location exists:

```text
Farm create/update accepts valid location.
Invalid latitude/longitude is rejected.
```

If farms.location does not exist:

```text
No migration is created.
API Gap is recorded.
```

If farm_code exists:

```text
farm_code is read-only.
```

If farm_code does not exist:

```text
Farm APIs still use farm_id.
No migration is created.
API Gap is recorded only if required.
```

## 23.9 Forbidden Scope Smoke

Verify absent:

```text
Notebook APIs
Note Item APIs
Follow-Up APIs
Notification APIs
File upload APIs
Upload queue processing
Offline sync
QR registry
QR API
Permission service
Permission table
Farm membership table
Owner registry
Member registry
Farmer registry
Block registry
Location table
Farm location table
GIS service
Audit table
Knowledge modules
Robot modules
Commerce modules
```

Expected:

```text
ABSENT
```

---

# 24. GitHub Issue Breakdown

## P2-6-01 — Farm Structure Scope Verification

Tasks:

```text
Review P0/P1/P2 frozen files.
Verify existing models for farms/zones/trees.
Verify P2-5 auth guards available.
Confirm no merge ambiguity before coding.
Record any API gaps.
```

Acceptance:

```text
Scope confirmed.
No coding outside P2-6 boundary.
```

## P2-6-02 — Farm Schemas

Tasks:

```text
Create FarmCreate.
Create FarmUpdate.
Create FarmRead.
Create Farm list response schema.
Preserve response envelope.
Respect location conditional boundary.
Respect farm_code conditional/read-only boundary.
```

Acceptance:

```text
Schemas match frozen model.
No organization_id input for owner farm create.
No farm_code input for owner farm create.
No unsupported fields added.
```

## P2-6-03 — Farm Repository

Tasks:

```text
Implement farm lookup.
Implement farm list with filters.
Implement create farm.
Implement update farm.
Implement parent organization checks.
Handle farm_code only if already present.
Handle location only if already present.
```

Acceptance:

```text
Repository uses farms table only.
No auth/RBAC logic inside repository.
No migration added.
```

## P2-6-04 — Farm Service

Tasks:

```text
Implement owner farm creation rule.
Implement owner multiple farms rule.
Implement organization scope validation.
Implement update validation.
Implement archive gap handling if unsupported.
Implement farm_code gap handling if unsupported.
Implement location gap handling if unsupported.
```

Acceptance:

```text
Owner can create multiple farms under own organization.
Owner cannot create farm under another organization.
owner_family/farm_staff cannot create farm.
No farm_code/location schema expansion without Owner approval.
```

## P2-6-05 — Farm Router

Tasks:

```text
Add GET /api/v1/farms.
Add GET /api/v1/farms/{farm_id}.
Add POST /api/v1/farms.
Add PATCH /api/v1/farms/{farm_id}.
Add archive endpoint only if supported.
```

Acceptance:

```text
Endpoints use auth/account/membership/scope guards.
Standard response envelope preserved.
```

## P2-6-06 — Zone Backend

Tasks:

```text
Create Zone schemas.
Create Zone repository.
Create Zone service.
Create Zone router.
Implement parent farm validation.
Implement zone create/update/list/read.
```

Acceptance:

```text
Zone belongs to Farm.
User must access parent Farm.
owner_family/farm_staff cannot create Zone.
```

## P2-6-07 — Tree Backend

Tasks:

```text
Create Tree schemas.
Create Tree repository.
Create Tree service.
Create Tree router.
Implement parent zone/farm validation.
Implement tree create/update/list/read.
```

Acceptance:

```text
Tree belongs to Zone.
Zone belongs to Farm.
User must access parent Farm.
owner_family/farm_staff cannot create Tree.
```

## P2-6-08 — Scope Guards

Tasks:

```text
Add require_organization_access.
Add require_farm_access.
Add minimal write guard if needed.
Test pending/rejected/suspended/revoked membership blocking.
```

Acceptance:

```text
Guards remain FastAPI dependencies.
No permission service/table/matrix created.
```

## P2-6-09 — Tests

Tasks:

```text
Farm API tests.
Zone API tests.
Tree API tests.
Guard tests.
Hierarchy validation tests.
Location conditional tests.
farm_code conditional tests.
Forbidden scope tests.
Regression auth tests.
```

Acceptance:

```text
All tests pass.
Previous P2-5 behavior preserved.
Forbidden scope absent.
```

## P2-6-10 — Docs and Smoke Checklist

Tasks:

```text
Update backend README if needed.
Update smoke checklist.
Record API gaps.
Record branch/commit summary after implementation.
```

Acceptance:

```text
Smoke checklist complete.
API gaps clearly documented.
No P2-7 scope included.
```

---

# 25. Acceptance Criteria

P2-6 is accepted only when all criteria below are true after coding implementation is explicitly approved:

## 25.1 Functional Acceptance

```text
Farm APIs implemented within scope.
Zone APIs implemented within scope.
Tree APIs implemented within scope.
Owner can create multiple farms under own organization.
Owner cannot create farm under another organization.
Owner can create zone under own farm.
Owner can create tree under own zone.
Basic list/read/update works for Farm/Zone/Tree.
Pagination/filtering works at basic level.
```

## 25.2 Authorization Acceptance

```text
Authenticated user required.
Active account required.
Active membership required for protected farm structure access.
pending_farm_approval blocked.
rejected/suspended/revoked blocked.
owner_family cannot create Farm/Zone/Tree.
farm_staff cannot create Farm/Zone/Tree.
primary_farm_id alone does not grant access.
Simple organization/farm scope guards work.
```

## 25.3 Architecture Acceptance

```text
Router → Service → Repository → Database pattern preserved.
No business logic in routers.
No SQL in routers.
No permission service created.
No new RBAC role created.
No new domain entity created.
No new backend app/service created.
```

## 25.4 Database Acceptance

```text
Only farms/zones/trees are written.
organizations/users may be read only for scope.
No new tables created.
No silent migration created.
Alembic upgrade head passes.
Forbidden tables absent.
```

## 25.5 Conditional Field Acceptance

```text
farms.location is used only if already present.
farm_code is used only if already present.
farm_code remains read-only if present.
No farm_code migration is created silently.
No location migration is created silently.
API gaps are recorded when required fields are missing or unclear.
```

## 25.6 Regression Acceptance

```text
Health endpoints pass.
Auth endpoints still pass.
GET /api/v1/auth/me still passes.
Existing tests still pass.
P2-5 auth guards still work.
```

## 25.7 Scope Acceptance

```text
No P2-7 code.
No Notebook APIs.
No Note Item APIs.
No File Upload APIs.
No Upload Queue processing.
No Offline Sync.
No Mobile implementation.
No Web implementation.
No QR API/service/registry.
No Knowledge module.
No Search Workspace implementation.
No Simulator Workspace implementation beyond safe existing farm filter.
No production deployment.
```

---

# 26. Explicit Non-Goals

P2-6 must not implement:

```text
P2-7
Notebook APIs
Note Item APIs
Follow-Up APIs
Notification APIs
File upload APIs
Upload queue processing
Offline sync
Mobile app
Web app
Knowledge Candidate
Knowledge Library
Search Workspace
Simulator Workspace beyond safe existing farm filter
QR registry
QR API
QR service
Permission service
Permission table
Permission matrix
ABAC
Farm membership table
Owner registry
Member registry
Farmer registry
Block registry
Location table
Farm location table
GIS service
Farm boundary mapping
Zone boundary mapping
Tree GPS mapping
Audit table
Production deployment
```

P2-6 must not hard delete:

```text
Farm
Zone
Tree
```

P2-6 must not silently add:

```text
new database columns
new enum values
new migrations
new tables
new RBAC roles
farm_code
location table
archive/deleted_at behavior
```

---

# 27. Ready for Owner Review

## 27.1 Review Status

```text
Document Status:
Draft Final / Ready for Owner Review
```

## 27.2 Owner Review Questions

Owner should review and confirm:

```text
1. Is P2-6 scope limited correctly to Farm / Zone / Tree backend?
2. Should PATCH /api/v1/farms/{farm_id}/archive remain conditional only?
3. Should farms.location be used only if already present?
4. Should farm_code remain conditional/read-only unless already implemented?
5. Should membership approval endpoint remain API Gap until separately approved?
6. Should owner_family and farm_staff remain blocked from all Farm/Zone/Tree creation?
7. Has P2-5 been committed, pushed, and merged?
```

## 27.3 Freeze Instruction

Do not mark this document frozen until Owner explicitly says:

```text
ok, freeze
```

After Owner freeze, this document becomes:

```text
ARI V1 — P2-6 Farm Structure Backend v1.0
Status: FROZEN
```

and may be used as coding authority for P2-6 implementation only.

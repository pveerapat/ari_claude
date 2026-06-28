# ARI V1 — P2-7 Notebook / Upload / Sync Backend v1.0

Project: ARI — Agricultural Intelligence Platform
Phase: P2 Coding Execution Phase
Document Number: P2-7
Document Type: Notebook / Upload / Sync Backend Specification / Execution Document
Version: v1.0
Status: Draft Final / Ready for Owner Review
Prepared From: Frozen Source of Truth + P2-1 / P2-2 / P2-3 / P2-4 / P2-5 / P2-6 Coding Execution Authority
Coding Direction: Backend Foundation First → Database → Auth → Farm Structure → Notebook / Upload / Sync → Mobile MVP → Web MVP → E2E → Prototype Deployment

---

# 1. Document Control

## 1.1 Document Identity

```text
Document Title:
ARI V1 — P2-7 Notebook / Upload / Sync Backend v1.0

Project:
ARI — Agricultural Intelligence Platform

Phase:
P2 Coding Execution Phase

Document Number:
P2-7

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

ARI V1 — P2-6 Farm Structure Backend v1.0
Status: FROZEN
Coding Foundation: IMPLEMENTED LOCALLY
Smoke Test: PASS
```

## 1.3 P2-6 Implementation Status Note

P2-6 implementation summary is recorded as:

```text
Farm APIs implemented
Zone APIs implemented
Tree APIs implemented
Farm / Zone / Tree hierarchy validation implemented
Organization / farm scope validation implemented
Owner farm creation implemented
Owner multiple farms supported
Owner family / farm staff blocked from Farm / Zone / Tree creation
Pending membership blocked from protected farm structure access
75 new tests added
232/232 tests passed
alembic upgrade head: PASS
GET /health: PASS
GET /api/v1/health: PASS
No new migrations
No forbidden scope detected
No P2-7 code implemented
```

Commit / push / merge status is not assumed in this document.

```text
Owner Confirmation Required:
Confirm whether P2-6 has been committed, pushed, and merged before P2-7 coding implementation starts.
```

## 1.4 P2-6 Open API Gaps Carried Forward

The following P2-6 gaps remain outside direct P2-7 scope unless they affect Notebook / Upload / Sync validation:

```text
API-GAP-P2-6-001 — Farm archive unclear: OPEN
API-GAP-P2-6-002 — Membership approval endpoint: OPEN
API-GAP-P2-6-004 — Simulator farm filter missing: OPEN
API-GAP-P2-6-005 — Delete vs Archive: OPEN
API-GAP-P2-6-006 — Uniqueness constraints: OPEN
API-GAP-P2-6-007 — farm_code missing: OPEN
```

P2-7 must not solve these silently.

If any of these affects P2-7 implementation, create a P2-7 API Gap reference and ask Owner for approval.

## 1.5 Document Boundary

This document defines the Notebook / Upload / Sync Backend implementation scope only.

This document is still a specification / execution document.

This document does not authorize actual coding implementation unless the Owner explicitly instructs implementation later.

This document does not create P2-8.

This document does not redesign ARI.

---

# 2. Purpose

The purpose of P2-7 is to define the backend implementation boundary for:

```text
Notebook Entries
Note Items
Follow-Ups
Notifications
Files / MinIO upload
Upload Queue
Offline Sync Batch
```

P2-7 prepares the backend for mobile and web MVP integration while preserving frozen ARI P0 scope.

P2-7 must preserve:

```text
Notebook Entry = Note Session
Note Item = Timeline Item
Consultation = Notebook Entry Type
Save Local ≠ Upload ≠ Analyze
```

P2-7 implements backend contracts only.

It does not implement mobile local storage, mobile UI, web UI, internal AI analysis, AI diagnosis, knowledge extraction, RAG, or future intelligence modules.

---

# 3. Scope

## 3.1 Required P2-7 Backend Modules

P2-7 must cover these backend modules:

```text
notebook_entries
note_items
follow_ups
notifications
files
upload_queue
sync
```

These modules are required because they map to frozen P0 API / database / backend implementation scope.

## 3.2 In Scope

P2-7 covers:

```text
Notebook Entry router
Notebook Entry schemas
Notebook Entry repository
Notebook Entry service

Note Item router
Note Item schemas
Note Item repository
Note Item service

Follow-Up router
Follow-Up schemas
Follow-Up repository
Follow-Up service

Notification router
Notification schemas
Notification repository
Notification service

Files router
Files schemas
Files service
MinIO presigned upload URL generation
Upload completion boundary
Upload failure reporting boundary

Upload Queue router
Upload Queue schemas
Upload Queue repository
Upload Queue service

Sync router
Sync schemas
Sync service
Sync batch validation
Per-item sync result mapping
client_id idempotency boundary

Notebook hierarchy validation
Organization scope validation
Farm / Zone / Tree scope validation
Created-by user validation
Timeline sequence_order handling

Basic filtering
Basic pagination
Keyword search only if already frozen and simple

Tests
Smoke checklist
API Gap / Revision Proposal handling
GitHub issue breakdown
```

## 3.3 Out of Scope Summary

P2-7 must not implement:

```text
P2-8
Mobile app
Web app
Internal AI assistant
Ask AI analysis engine
AI result generation
Knowledge Candidate entity
Knowledge Library entity
Knowledge graph
Vector database
RAG
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
GIS service
Audit table
Production deployment
Robot module
Commerce module
Advanced media processing
OCR
Speech-to-text
Image recognition
Disease diagnosis
Treatment recommendation
```

---

# 4. Source of Truth

P2-7 must follow:

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
ARI V1 — P2-6 Farm Structure Backend v1.0
```

P2-7 must preserve:

```text
One Platform
One Backend
One Database Architecture
One Mobile App
One Web App
One Domain Model
One RBAC System
```

If a detail is missing, unclear, or inconsistent, implementation must create:

```text
API Gap / Revision Proposal
```

Do not silently invent behavior.

---

# 5. Relationship to P2-1 through P2-6

## 5.1 Relationship to P2-1

P2-1 defines the coding direction:

```text
Backend foundation
Database migrations
Auth and onboarding
Farm structure
Notebook / upload / sync
Mobile MVP
Web MVP
E2E
Prototype deployment
Pilot
```

P2-7 corresponds to:

```text
Notebook / upload / sync
```

P2-7 remains before:

```text
Mobile MVP
Web MVP
E2E
Prototype deployment
Pilot
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

P2-7 must preserve:

```text
api
postgres
minio
emqx

GET /health
GET /api/v1/health
```

## 5.3 Relationship to P2-3

P2-3 created:

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

P2-7 must use existing foundation patterns.

P2-7 must not bypass:

```text
Router Layer
Service Layer
Repository Layer
Database Layer
```

## 5.4 Relationship to P2-4

P2-4 created:

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

P2-7 may use only existing frozen tables.

P2-7 must not add a database migration unless Owner explicitly approves.

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

P2-7 may use existing P2-5 dependencies:

```text
get_current_user
require_authenticated_user
require_active_account
require_active_membership
```

P2-7 must block protected notebook/upload/sync access when:

```text
membership_status = pending_farm_approval
```

## 5.6 Relationship to P2-6

P2-6 created:

```text
Farm schemas / repositories / services / routers
Zone schemas / repositories / services / routers
Tree schemas / repositories / services / routers
Simple farm structure scope helpers
Farm / Zone / Tree hierarchy validation
Organization / farm scope validation
```

P2-7 may reuse P2-6 hierarchy and scope helpers.

P2-7 must validate Notebook hierarchy references using existing Farm / Zone / Tree relationships.

P2-7 must not reimplement Farm / Zone / Tree features.

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

## 6.6 Confirmed Farm Structure Foundation

```text
Farm router/service/repository/schema
Zone router/service/repository/schema
Tree router/service/repository/schema
Organization scope helper
Farm scope helper
Hierarchy validation
Owner farm creation rule
Pending membership access block
```

---

# 7. Notebook Domain Boundary

## 7.1 Frozen Notebook Terms

P2-7 must preserve:

```text
Notebook Entry = Note Session
Note Item = Timeline Item
Consultation = Notebook Entry Type
```

## 7.2 Supported Notebook Entry Types

```text
note
consultation
```

## 7.3 Supported Note Item Types

```text
photo
video
voice
text
file
link
```

## 7.4 Required Notebook Principle

```text
Save Local
≠
Upload
≠
Analyze
```

Meaning:

```text
Save Local:
Mobile/client can store locally before upload.

Upload:
Backend receives records/files and stores metadata/references.

Analyze:
AI analysis is separate and not implemented by P2-7.
```

P2-7 backend supports upload/sync contracts only.

P2-7 does not implement:

```text
mobile local database
mobile offline UI
mobile background scheduler
internal AI analysis
AI diagnosis
treatment recommendation
knowledge extraction
```

---

# 8. Notebook Entry API Scope

## 8.1 Allowed Endpoints

P2-7 must implement:

```text
GET /api/v1/notebook-entries
GET /api/v1/notebook-entries/{entry_id}
POST /api/v1/notebook-entries
PATCH /api/v1/notebook-entries/{entry_id}
```

Conditional only if frozen API/model clearly supports status transition:

```text
PATCH /api/v1/notebook-entries/{entry_id}/status
```

Do not implement hard delete.

## 8.2 List Notebook Entries

Purpose:

```text
Return notebook entries visible to current authenticated user within organization/farm scope.
```

Allowed query parameters:

```text
page
page_size
farm_id
zone_id
tree_id
entry_type
entry_context
status
analysis_status if existing
consultation_status if existing
date_from
date_to
q if keyword search is implemented
sort_by
sort_order
```

Rules:

```text
Default sort should be created_at DESC.
Pagination should follow existing common schema pattern.
Farm / zone / tree filters must enforce scope.
Keyword search must remain simple keyword/filter search only.
```

Not allowed:

```text
semantic search
vector search
RAG search
LLM search
knowledge graph search
```

## 8.3 Get Notebook Entry Detail

Purpose:

```text
Return one notebook entry with access validation.
```

Rules:

```text
entry_id must exist.
Current user must have organization/farm scope access.
Current user must have active account and active membership.
Response may include note items only if API schema supports it.
```

## 8.4 Create Notebook Entry

Purpose:

```text
Create a Notebook Entry / Note Session.
```

Required backend rules:

```text
created_by_user_id must come from current authenticated user.
organization_id must be current user's organization or accessible organization.
farm_id / zone_id / tree_id may be null.
entry_type must be note or consultation.
entry_context must match frozen enum if provided.
created_at must store UTC.
status must use frozen enum if provided.
Hierarchy must be validated.
```

Backend must not trust client-supplied:

```text
created_by_user_id
organization access
farm access
role
membership_status
account_status
```

## 8.5 Patch Notebook Entry

Purpose:

```text
Update allowed mutable Notebook Entry fields.
```

Allowed updates may include only frozen fields such as:

```text
title if existing
summary if existing
entry_context
status if existing
analysis_status if existing
consultation_status if existing
learned_summary if existing
follow_up if existing
outcome if existing
location_name
gps_latitude
gps_longitude
location_note
source_type
source_name
source_note
farm_id
zone_id
tree_id
```

Rules:

```text
Do not allow created_by_user_id reassignment.
Do not allow organization_id change unless explicitly approved.
If hierarchy IDs change, validate full hierarchy again.
Do not implement hard delete.
```

## 8.6 Notebook Entry Delete / Archive Boundary

P2-7 must not implement hard delete.

Archive/status transition is allowed only if frozen status behavior is clear.

If archive/status behavior is unclear, create API Gap:

```text
API-GAP-P2-7-002 — Notebook Entry archive/status transition behavior
```

---

# 9. Notebook Hierarchy Validation

Notebook Entry may reference:

```text
organization_id required
created_by_user_id required
farm_id nullable
zone_id nullable
tree_id nullable
```

P2-7 must preserve nullable hierarchy rules.

Notebook Entry can represent:

```text
general note without farm
registered farm note
zone-level note
tree-level note
external observation
interview
consultation
```

If hierarchy IDs are provided, P2-7 must validate:

```text
farm belongs to organization
zone belongs to farm
tree belongs to zone
```

Default P2-7 rule:

```text
Require explicit parent IDs when child IDs are provided unless frozen source or existing service helper clearly supports safe inference.
```

If zone_id is provided without farm_id and behavior is unclear, create API Gap.

If tree_id is provided without zone_id/farm_id and behavior is unclear, create API Gap.

```text
API-GAP-P2-7-001 — Notebook hierarchy inference for zone_id/tree_id without explicit parent IDs
```

---

# 10. Note Item API Scope

## 10.1 Allowed Endpoints

P2-7 must implement:

```text
GET /api/v1/notebook-entries/{entry_id}/items
POST /api/v1/notebook-entries/{entry_id}/items
PATCH /api/v1/note-items/{item_id}
```

Conditional only if frozen API/model clearly supports delete:

```text
DELETE /api/v1/note-items/{item_id}
```

If delete behavior is unclear, create API Gap:

```text
API-GAP-P2-7-003 — Note Item delete behavior
```

## 10.2 List Note Items by Entry

Purpose:

```text
Return note items for one notebook entry in timeline order.
```

Rules:

```text
Parent notebook entry must exist.
Current user must have access to parent entry.
Default ordering must use sequence_order ASC.
```

## 10.3 Create Note Item

Purpose:

```text
Create a timeline item under a notebook entry.
```

Required validation:

```text
entry_id must exist.
item_type must be one of photo/video/voice/text/file/link.
sequence_order must be present or assigned safely by backend.
text_body allowed only for text item type.
link_url allowed only for link item type.
file_ref/local_path/file_path allowed only according to frozen schema.
duration_sec allowed for voice/video if supported.
checksum allowed if supported.
```

Timeline rule:

```text
sequence_order must preserve the order of evidence capture within one Notebook Entry.
```

If database uniqueness for sequence_order is not enforced or unclear, create API Gap:

```text
API-GAP-P2-7-004 — Note Item sequence_order uniqueness/auto-assignment rule
```

## 10.4 Patch Note Item

Purpose:

```text
Update allowed mutable fields of a note item.
```

Allowed updates may include:

```text
text_body
link_url
file_ref
file_path if existing
duration_sec
checksum
sequence_order
metadata fields if existing
status if existing
```

Rules:

```text
Do not move note item to another entry unless explicitly approved.
If sequence_order changes, maintain deterministic order.
If item_type changes, validate allowed fields again.
```

---

# 11. Consultation Boundary

## 11.1 Consultation Implementation Rule

Consultation is implemented as:

```text
Notebook Entry Type = consultation
```

Consultation is not a separate domain entity.

P2-7 must not create:

```text
consultations table
consultation model
consultation schema
consultation repository
consultation service
consultation router
/api/v1/consultations
```

## 11.2 Consultation Fields

Consultation-related fields must remain inside Notebook Entry logic only if already present in frozen schema/model:

```text
entry_type
entry_context
external_ai
ai_result_status
learned_summary
follow_up
outcome
consultation_status if existing
analysis_status if existing
```

## 11.3 AI Analysis Boundary

P2-7 does not generate AI results.

Allowed:

```text
Store external AI consultation metadata if frozen schema supports it.
Store learned_summary if provided by user/client and frozen schema supports it.
Store follow_up/outcome if frozen schema supports it.
```

Not allowed:

```text
call ChatGPT / Gemini / Claude
internal AI assistant
diagnosis engine
treatment recommendation
knowledge extraction
RAG
vector search
```

If consultation status/AI fields are inconsistent between schema and API, create API Gap:

```text
API-GAP-P2-7-005 — Consultation AI/status field alignment
```

---

# 12. Follow-Up API Scope

## 12.1 Required Endpoints

P2-7 must include Follow-Up APIs because follow_ups are frozen P0 scope.

Allowed endpoints:

```text
GET /api/v1/follow-ups
GET /api/v1/follow-ups/{follow_up_id}
POST /api/v1/follow-ups
PATCH /api/v1/follow-ups/{follow_up_id}
```

## 12.2 Follow-Up Rules

Follow-Up must reference Notebook Entry / consultation entry according to frozen schema.

Required validation:

```text
follow_up_day = 3 / 7 / 14
outcome = improved / same / worse / unknown
```

Allowed behavior:

```text
Create follow-up record.
List follow-ups visible to current user.
Get follow-up detail.
Record/update outcome.
Filter by status/date if frozen schema supports it.
```

Not allowed:

```text
calendar integration
push notification provider
AI follow-up recommendation
automatic treatment workflow
new scheduling engine
```

If follow-up scheduling fields are unclear, create API Gap:

```text
API-GAP-P2-7-013 — Follow-Up API and scheduling field boundary
```

---

# 13. Notification API Scope

## 13.1 Required Endpoints

P2-7 must include Notification APIs because notifications are frozen P0 scope.

Allowed endpoints:

```text
GET /api/v1/notifications
GET /api/v1/notifications/{notification_id}
PATCH /api/v1/notifications/{notification_id}/read
POST /api/v1/notifications/mark-all-read
```

Do not use:

```text
PATCH /api/v1/notifications/read-all
```

## 13.2 Notification Rules

Notification access is own-user scoped unless admin/root manage scope is already defined.

Allowed behavior:

```text
List notifications.
Get notification detail.
Mark one notification as read.
Mark all current user's notifications as read.
Create upload reminder notification if required and frozen.
Create follow-up reminder notification if required and frozen.
```

Not allowed:

```text
push notification provider integration
mobile notification UI
web notification UI
notification microservice
audit log system
event bus redesign
```

If notification generation behavior is unclear, create API Gap:

```text
API-GAP-P2-7-014 — Notification creation/read boundary
```

---

# 14. Upload / File API Scope

## 14.1 Required Endpoints

P2-7 must include:

```text
POST /api/v1/files/upload-url
POST /api/v1/files/complete
POST /api/v1/files/upload-failed
```

Do not invent:

```text
/files/presign-upload
/files/confirm-upload
/files/presign
/files/confirm
/upload/presign
/upload/complete
/media/upload
```

## 14.2 Create Upload URL

Purpose:

```text
Generate MinIO presigned upload URL for a file linked to a Notebook Entry / Note Item workflow.
```

Expected request fields:

```text
entry_id
item_type
file_name
content_type
file_size
checksum if supported
client_id if supported
```

Expected response fields:

```text
file_key
upload_url
expires_in
```

Required validation:

```text
entry_id required.
entry_id must be accessible to current user.
item_type must be photo/video/voice/file.
content_type must be valid.
file_size must be greater than 0.
User must have active account and active membership.
```

Not allowed item types for file upload URL:

```text
text
link
```

unless frozen API explicitly allows attachments through another field.

## 14.3 Complete Upload

Purpose:

```text
Confirm client completed file upload to MinIO.
```

Expected request fields:

```text
entry_id
file_key
upload_status = completed
checksum if supported
item_id if binding to existing note item is supported
client_id if supported
```

Rules:

```text
Backend must verify parent entry access.
Backend should verify object exists in MinIO if implementation helper exists.
Backend may bind file_key/file_ref to Note Item only according to frozen schema.
Backend must not store binary file content in PostgreSQL.
```

If binding uploaded file to Note Item is unclear, create API Gap:

```text
API-GAP-P2-7-007 — Uploaded file to Note Item binding behavior
```

## 14.4 Upload Failed

Purpose:

```text
Record/report upload failure from client and update upload_queue lifecycle.
```

Expected request fields:

```text
entry_id
file_key if already generated
queue_id if upload_queue record exists
client_id if supported
reason
```

Rules:

```text
Backend must validate parent entry or upload_queue access.
Backend may update upload_queue status to failed.
Backend may increment retry_count only if frozen schema supports it.
Backend must not create duplicate note item.
Backend must not create background retry scheduler.
Backend must not create new table.
```

## 14.5 MinIO Boundary

Allowed:

```text
Generate presigned upload URL.
Generate object key.
Verify object existence if supported.
Store object reference in database metadata.
Use checksum if frozen schema supports it.
```

Not allowed:

```text
direct mobile upload logic inside backend
mobile retry scheduler
background worker
video processing
image processing
thumbnail generation
virus scanning
OCR
speech-to-text
object detection
AI media analysis
```

If bucket name/key format is unclear, create API Gap:

```text
API-GAP-P2-7-008 — MinIO bucket and object key naming rule
```

---

# 15. Upload Queue Boundary

## 15.1 Naming Lock

Canonical database table:

```text
upload_queue
```

Canonical API path:

```text
/api/v1/upload-queue
```

Python internal names may use:

```text
UploadJob
upload_job.py
upload_jobs.py
```

only if they map to the existing `upload_queue` table.

P2-7 must not create:

```text
upload_jobs table
/api/v1/upload-jobs
separate upload job entity
```

If naming conflict exists in codebase, create API Gap:

```text
API-GAP-P2-7-009 — upload_queue vs upload_jobs naming alignment
```

## 15.2 Required Endpoints

P2-7 must include:

```text
POST /api/v1/upload-queue
GET /api/v1/upload-queue
GET /api/v1/upload-queue/{queue_id}
PATCH /api/v1/upload-queue/{queue_id}
POST /api/v1/upload-queue/{queue_id}/retry
```

## 15.3 Upload Queue Purpose

Upload Queue supports:

```text
Offline First synchronization
Upload lifecycle tracking
Client retry support
Idempotency boundary
```

Lifecycle:

```text
pending
↓
uploading
↓
completed
```

or:

```text
pending
↓
uploading
↓
failed
↓
retry
```

## 15.4 Upload Queue Validation

Required validation:

```text
client_id required if supported by frozen schema/API.
entry_id required if upload relates to notebook entry.
upload_entity_type required if frozen schema supports it.
upload_action required if frozen schema supports it.
status must be frozen enum value.
Current user must own or access the queue record.
```

## 15.5 Upload Queue Non-Goals

P2-7 must not implement:

```text
background upload worker
server-side media processing queue
distributed task queue
Celery/RQ worker
MQTT sync engine
automatic retry daemon
```

---

# 16. Offline Sync API Scope

## 16.1 Required Endpoint

P2-7 must include:

```text
POST /api/v1/sync/batch
```

## 16.2 Canonical Backend Payload

Canonical backend shape follows P0 API:

```json
{
  "device_id": "uuid",
  "client_batch_id": "uuid",
  "items": [
    {
      "client_id": "uuid",
      "entity_type": "notebook_entry",
      "action": "create",
      "payload": {}
    }
  ]
}
```

## 16.3 Mobile Payload Mismatch

P1-2 Mobile uses:

```json
{
  "client_batch_id": "uuid",
  "device_id": "uuid",
  "organization_id": "uuid",
  "operations": [
    {
      "client_id": "uuid",
      "operation_type": "create_notebook_entry",
      "entity_type": "notebook_entry",
      "payload": {},
      "created_at": "timestamp"
    }
  ]
}
```

This mismatch must be recorded as API Gap.

```text
API-GAP-P2-7-011 — Sync batch payload naming mismatch: P0 API uses items[] / action, P1-2 Mobile uses operations[] / operation_type
```

Default rule:

```text
Backend canonical implementation should follow P0 API items[] / action.
Do not support both shapes silently.
If Owner approves backward-compatible alias support, document it before implementation.
```

## 16.4 Sync Batch Purpose

Purpose:

```text
Accept multiple offline-created records from client and return per-item result mapping.
```

Supported entity types within P2-7:

```text
notebook_entry
note_item
follow_up
notification
upload_queue
```

Do not sync non-P2-7 entities unless frozen API explicitly requires it.

## 16.5 Expected Response Shape

```json
{
  "client_batch_id": "uuid",
  "results": [
    {
      "client_id": "uuid",
      "server_id": "uuid",
      "status": "completed"
    }
  ]
}
```

## 16.6 Sync Batch Rules

Allowed:

```text
Validate authenticated user.
Validate active account.
Validate active membership.
Validate organization/farm scope.
Accept notebook entry payloads if matching frozen schema.
Accept note item payloads if matching frozen schema.
Accept follow_up payloads if matching frozen schema.
Accept notification read operations if matching frozen schema.
Return per-item success/failure results.
Use client_id for idempotency.
Avoid duplicate creation if same user_id + client_id already exists.
Use explicit transaction strategy.
```

Recommended transaction policy:

```text
Each item should return its own result.
A failed item should not hide results for other items.
Database transaction handling may be per-item inside the batch unless existing service layer supports full batch transaction with partial result mapping.
```

If transaction policy is unclear, create API Gap:

```text
API-GAP-P2-7-012 — Sync batch transaction policy
```

## 16.7 Sync Non-Goals

P2-7 must not implement:

```text
mobile offline database
mobile conflict UI
CRDT
realtime sync
MQTT sync
multi-device merge engine
background sync worker
AI-based deduplication
full conflict resolution engine beyond frozen scope
```

---

# 17. Client ID / Idempotency Boundary

## 17.1 Required Idempotency Rule

Offline sync and upload retry must use:

```text
user_id + client_id
```

Rules:

```text
Do not regenerate client_id on retry.
Do not duplicate records after retry.
Map local_id to server_id after success.
Reuse same client_id, local_item_id, and sequence_order for failed upload retry.
```

## 17.2 Database Field Boundary

If current database model does not contain client_id fields on required tables, P2-7 must not add migration silently.

Create API Gap / Revision Proposal:

```text
API-GAP-P2-7-017 — client_id/device_id physical database support
```

## 17.3 Allowed Behavior

Allowed:

```text
Use existing client_id fields if present.
Check duplicate user_id + client_id if supported.
Return existing server_id when duplicate retry is detected.
```

Not allowed:

```text
Create duplicate notebook entry on retry.
Create duplicate note item on retry.
Create duplicate upload_queue row on retry if client_id exists.
Add new column without Owner approval.
```

---

# 18. Authorization Boundary

## 18.1 Existing Guards

P2-7 may use existing P2-5 and P2-6 guards:

```text
get_current_user
require_authenticated_user
require_active_account
require_active_membership
require_organization_access
require_farm_access
```

## 18.2 New Simple Guards Allowed

P2-7 may add simple dependency helpers only if needed:

```text
require_notebook_entry_access
require_note_item_access
require_follow_up_access
require_notification_access
require_upload_queue_access
```

These must remain FastAPI dependency guards only.

They are not:

```text
permission service
permission matrix
ABAC
policy engine
```

## 18.3 Resource Access Rules

Notebook Entry:

```text
User can access own notebook entry within own organization/farm scope.
ARI staff / coordinator / agronomist / reviewer access follows frozen RBAC + organization/farm scope.
Admin/root access follows frozen RBAC.
```

Note Item:

```text
Access follows parent notebook entry access.
```

Follow-Up:

```text
Access follows parent notebook entry / consultation entry access.
```

Notification:

```text
Access is own-user scoped unless admin/root manage scope is already frozen.
```

File Upload:

```text
Access follows parent notebook entry or note item access.
```

Upload Queue:

```text
Access follows creator/current user and related entity scope.
```

Sync Batch:

```text
Every item in batch must pass user/account/membership/scope validation.
```

## 18.4 Forbidden Authorization Additions

Do not create:

```text
permissions table
permission service
permission matrix engine
farm_membership table
approval service
audit table
```

---

# 19. Membership Boundary

Frozen farmer_status values:

```text
owner
owner_family
farm_staff
```

These are not RBAC roles.

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

Protected notebook/upload/sync access requires:

```text
account_status allows access
membership_status = active
```

Before approval:

```text
membership_status = pending_farm_approval
```

must block protected farm-scoped notebook/upload/sync access.

Rules:

```text
Owner may create/use notebook entries under own organization and accessible farms.
Owner family / farm staff may use notebook/upload/sync only after active membership.
Pending users may authenticate but cannot access protected farm-scoped P2-7 APIs.
```

---

# 20. Repository / Service / Router Pattern

## 20.1 Router Layer

Routers are responsible for:

```text
HTTP endpoint declaration
Request schema validation
Dependency injection
Authentication guard usage
Authorization guard usage
Calling service methods
Returning response schemas
```

Routers must not:

```text
query SQL directly
implement hierarchy rules directly
implement MinIO logic directly
manage transactions directly unless existing pattern requires it
```

## 20.2 Service Layer

Services are responsible for:

```text
Frozen domain rules
Hierarchy validation
Organization/farm scope validation
Created-by validation
Timeline sequence_order rules
Follow-up rules
Notification rules
Upload lifecycle rules
Sync item orchestration
Idempotency handling
Transaction orchestration
Calling repositories
Calling MinIO helper/client
```

Services must remain simple and P0-focused.

Do not create:

```text
consultation_service.py
knowledge_service.py
agent_service.py
permission_service.py
audit_service.py
commerce_service.py
robot_service.py
```

## 20.3 Repository Layer

Repositories are responsible for:

```text
SQLAlchemy query construction
CRUD operations
Filtering
Pagination
Row-level lookup
Database constraint interaction
```

Repositories must not:

```text
interpret JWT
implement RBAC
call MinIO
call external AI
call MQTT for sync
```

## 20.4 Suggested Module Files

P2-7 may add/use:

```text
backend/app/api/v1/notebook_entries.py
backend/app/api/v1/note_items.py
backend/app/api/v1/follow_ups.py
backend/app/api/v1/notifications.py
backend/app/api/v1/files.py
backend/app/api/v1/upload_queue.py
backend/app/api/v1/sync.py

backend/app/schemas/notebook_entry.py
backend/app/schemas/note_item.py
backend/app/schemas/follow_up.py
backend/app/schemas/notification.py
backend/app/schemas/file.py
backend/app/schemas/upload_queue.py
backend/app/schemas/sync.py

backend/app/repositories/notebook_entries.py
backend/app/repositories/note_items.py
backend/app/repositories/follow_ups.py
backend/app/repositories/notifications.py
backend/app/repositories/upload_queue.py

backend/app/services/notebook_service.py
backend/app/services/note_item_service.py
backend/app/services/follow_up_service.py
backend/app/services/notification_service.py
backend/app/services/file_service.py
backend/app/services/upload_queue_service.py
backend/app/services/sync_service.py
```

---

# 21. Schema Requirements

## 21.1 Notebook Entry Schemas

Suggested schemas:

```text
NotebookEntryCreate
NotebookEntryUpdate
NotebookEntryRead
NotebookEntryListItem
NotebookEntryListResponse
NotebookEntryStatusUpdate only if frozen status transition exists
```

Fields must map only to frozen model fields.

Do not add required fields that are not frozen.

## 21.2 Note Item Schemas

Suggested schemas:

```text
NoteItemCreate
NoteItemUpdate
NoteItemRead
NoteItemListResponse
```

Fields must support frozen item types:

```text
photo
video
voice
text
file
link
```

## 21.3 Follow-Up Schemas

Suggested schemas:

```text
FollowUpCreate
FollowUpUpdate
FollowUpRead
FollowUpListResponse
FollowUpOutcomeUpdate
```

Must validate:

```text
follow_up_day = 3 / 7 / 14
outcome = improved / same / worse / unknown
```

## 21.4 Notification Schemas

Suggested schemas:

```text
NotificationRead
NotificationListResponse
NotificationMarkReadResponse
NotificationMarkAllReadResponse
```

## 21.5 File Schemas

Suggested schemas:

```text
FileUploadUrlRequest
FileUploadUrlResponse
FileCompleteRequest
FileCompleteResponse
FileUploadFailedRequest
FileUploadFailedResponse
```

## 21.6 Upload Queue Schemas

Suggested schemas:

```text
UploadQueueCreate
UploadQueueUpdate
UploadQueueRead
UploadQueueListResponse
UploadQueueRetryResponse
```

## 21.7 Sync Schemas

Suggested schemas:

```text
SyncBatchRequest
SyncBatchItem
SyncBatchResult
SyncBatchResponse
```

Canonical fields:

```text
device_id
client_batch_id
items[]
client_id
entity_type
action
payload
```

## 21.8 Schema Non-Goals

Do not add schemas for:

```text
ConsultationCreate as separate entity
ConsultationRead as separate entity
PermissionMatrix
AuditLog
KnowledgeCandidate as database entity
VectorSearch
RAGQuery
AIAnalysisRequest
```

---

# 22. Validation Rules

## 22.1 Common Validation

```text
All IDs must be valid UUIDs unless existing code uses another frozen ID format.
All enum values must match frozen Python enums.
All timestamps stored by backend must use UTC.
Pagination must respect foundation limits.
Unknown fields should be rejected unless common schema pattern allows them.
```

## 22.2 Notebook Validation

```text
entry_type must be note or consultation.
organization_id required.
created_by_user_id comes from current user.
farm_id nullable.
zone_id nullable.
tree_id nullable.
If farm_id exists, farm must belong to organization.
If zone_id exists, zone must belong to farm.
If tree_id exists, tree must belong to zone.
```

## 22.3 Note Item Validation

```text
entry_id required.
entry_id must be accessible.
item_type must be photo/video/voice/text/file/link.
sequence_order required or assigned by backend.
link_url allowed only for link item type.
text_body allowed only for text item type.
file_ref/file_path allowed only for media/file item types.
checksum used only if existing field supports it.
```

## 22.4 Follow-Up Validation

```text
parent notebook entry must exist.
parent notebook entry must be accessible.
follow_up_day must be 3 / 7 / 14.
outcome must be improved / same / worse / unknown if outcome is provided.
```

## 22.5 Notification Validation

```text
notification_id must exist.
current user must own notification unless admin/root manage scope is frozen.
mark-all-read applies to current user's notifications only unless admin/root manage scope is frozen.
```

## 22.6 Upload Validation

```text
entry_id required.
User must access parent notebook entry.
item_type must support upload.
content_type must be valid.
file_size must be > 0.
file_key must belong to expected organization/entry prefix if key format is implemented.
```

## 22.7 Sync Validation

```text
device_id required if frozen request requires it.
client_batch_id required if frozen request requires it.
items must be non-empty.
Each item must contain client_id, entity_type, action, payload.
entity_type must be allowed.
action must be create/update/mark_read only if supported.
Each payload must pass the same service validation as normal endpoint create/update.
```

---

# 23. Error Handling

P2-7 must use existing common error foundation.

Expected error types:

```text
400 bad_request
401 unauthorized
403 forbidden
404 not_found
409 conflict
422 validation_error
500 internal_error
```

Recommended error cases:

```text
notebook_entry_not_found
note_item_not_found
follow_up_not_found
notification_not_found
upload_queue_not_found
invalid_entry_type
invalid_item_type
invalid_sequence_order
invalid_hierarchy
organization_scope_denied
farm_scope_denied
membership_not_active
account_not_active
file_upload_not_allowed
file_not_found_in_storage
duplicate_client_id
sync_item_failed
```

Error responses must follow existing standard envelope.

Do not leak:

```text
MinIO internal credentials
database exception details
JWT internals
stack traces
```

---

# 24. Database Boundary

## 24.1 Read/Write Tables

P2-7 may read/write:

```text
notebook_entries
note_items
follow_ups
notifications
upload_queue
```

## 24.2 Read-Only / Scope Tables

P2-7 may read:

```text
organizations
users
farms
zones
trees
roles / user_roles only if already confirmed
```

## 24.3 Forbidden Tables

P2-7 must not create:

```text
consultations
qr_registry
farm_memberships
permissions
audit_logs
reviews
knowledge
knowledge_assets
vectors
robot_commands
commerce_orders
media_processing_jobs
sync_conflicts
device_registry
upload_jobs
```

## 24.4 Migration Boundary

P2-7 must not add a migration by default.

If any required field is missing from existing frozen schema, create:

```text
API Gap / Revision Proposal
```

Do not silently add a column/table.

---

# 25. API Gap / Revision Proposal Handling

If implementation finds missing/unclear/inconsistent frozen details, create:

```text
docs/api-gaps/API-GAP-P2-7.md
```

Expected P2-7 API Gaps:

```text
API-GAP-P2-7-001 — Notebook hierarchy inference for zone_id/tree_id without explicit parent IDs
API-GAP-P2-7-002 — Notebook Entry archive/status transition behavior
API-GAP-P2-7-003 — Note Item delete behavior
API-GAP-P2-7-004 — Note Item sequence_order uniqueness/auto-assignment rule
API-GAP-P2-7-005 — Consultation AI/status field alignment
API-GAP-P2-7-006 — File upload endpoint naming conflict
API-GAP-P2-7-007 — Uploaded file to Note Item binding behavior
API-GAP-P2-7-008 — MinIO bucket and object key naming rule
API-GAP-P2-7-009 — upload_queue vs upload_jobs naming alignment
API-GAP-P2-7-010 — Upload Queue endpoint naming conflict
API-GAP-P2-7-011 — Sync batch payload naming mismatch: P0 API uses items[] / action, P1-2 Mobile uses operations[] / operation_type
API-GAP-P2-7-012 — Sync batch transaction policy
API-GAP-P2-7-013 — Follow-Up API and scheduling field boundary
API-GAP-P2-7-014 — Notification creation/read boundary
API-GAP-P2-7-015 — Media read URL endpoint for Web media viewer
API-GAP-P2-7-016 — Checksum/dedup behavior
API-GAP-P2-7-017 — client_id/device_id physical database support
```

Rules:

```text
Do not block safe implementation for unrelated gaps.
Do not implement guessed behavior.
Do not add migrations without Owner approval.
Do not rename frozen endpoints silently.
Do not support both sync payload shapes silently.
```

---

# 26. Testing Requirements

## 26.1 Unit Tests

Required test groups:

```text
NotebookEntryService tests
NoteItemService tests
FollowUpService tests
NotificationService tests
FileService tests
UploadQueueService tests
SyncService tests
Hierarchy validation tests
Membership guard tests
Sequence order tests
client_id idempotency tests if client_id exists
```

## 26.2 Repository Tests

Required test groups:

```text
notebook_entries repository CRUD
note_items repository CRUD
follow_ups repository CRUD
notifications repository CRUD
upload_queue repository CRUD
filtering / pagination
created_at ordering
client_id uniqueness/idempotency if supported
```

## 26.3 API Tests

Required test groups:

```text
GET /api/v1/notebook-entries
GET /api/v1/notebook-entries/{entry_id}
POST /api/v1/notebook-entries
PATCH /api/v1/notebook-entries/{entry_id}

GET /api/v1/notebook-entries/{entry_id}/items
POST /api/v1/notebook-entries/{entry_id}/items
PATCH /api/v1/note-items/{item_id}

GET /api/v1/follow-ups
GET /api/v1/follow-ups/{follow_up_id}
POST /api/v1/follow-ups
PATCH /api/v1/follow-ups/{follow_up_id}

GET /api/v1/notifications
GET /api/v1/notifications/{notification_id}
PATCH /api/v1/notifications/{notification_id}/read
POST /api/v1/notifications/mark-all-read

POST /api/v1/files/upload-url
POST /api/v1/files/complete
POST /api/v1/files/upload-failed

POST /api/v1/upload-queue
GET /api/v1/upload-queue
GET /api/v1/upload-queue/{queue_id}
PATCH /api/v1/upload-queue/{queue_id}
POST /api/v1/upload-queue/{queue_id}/retry

POST /api/v1/sync/batch
```

## 26.4 Authorization Tests

Required cases:

```text
Unauthenticated user is rejected.
Inactive account is rejected.
Pending membership is rejected.
User cannot access another organization notebook entry.
User cannot access unauthorized farm notebook entry.
Parent entry access controls note item access.
Parent entry access controls follow-up access.
Notification access is own-user scoped.
Parent entry access controls file upload access.
Upload queue access is scoped.
Sync batch item access is scoped.
```

## 26.5 Forbidden Scope Tests

Tests or grep checks must confirm absence of:

```text
consultations table
consultation router
consultation service
qr_registry
permission service
farm_memberships
knowledge service
vector service
RAG
internal AI assistant
media processing worker
upload_jobs table
```

---

# 27. Smoke Test Checklist

Before marking P2-7 implementation complete:

```text
[ ] docker compose starts api/postgres/minio/emqx.
[ ] GET /health returns success.
[ ] GET /api/v1/health returns success.
[ ] alembic upgrade head passes.
[ ] Existing P2-5 auth tests still pass.
[ ] Existing P2-6 farm/zone/tree tests still pass.
[ ] Notebook Entry list/read/create/update tests pass.
[ ] Note Item list/create/update tests pass.
[ ] sequence_order behavior is tested.
[ ] Consultation uses entry_type=consultation only.
[ ] No consultation entity/module/router exists.
[ ] Follow-Up APIs pass.
[ ] follow_up_day = 3 / 7 / 14 validation passes.
[ ] outcome validation passes.
[ ] Notification APIs pass.
[ ] POST /api/v1/notifications/mark-all-read passes.
[ ] File upload URL endpoint returns presigned URL using MinIO config.
[ ] File complete endpoint validates scope.
[ ] File upload-failed endpoint updates allowed lifecycle only.
[ ] Upload queue lifecycle tests pass.
[ ] Upload queue API path is /api/v1/upload-queue only.
[ ] No upload_jobs table/API exists.
[ ] Sync batch returns per-item results.
[ ] Sync canonical payload uses items[] / action.
[ ] Sync payload mismatch is recorded as API Gap.
[ ] client_id idempotency tested if field is supported.
[ ] Pending membership blocked from protected notebook/upload/sync endpoints.
[ ] No new tables created.
[ ] No new migrations unless Owner approved.
[ ] No new RBAC roles introduced.
[ ] API Gap document updated for unresolved details.
[ ] Backend tests pass.
```

---

# 28. GitHub Issue Breakdown

Recommended issue set:

```text
P2-7-001 Notebook Entry schemas/repository/service/router
P2-7-002 Notebook Entry hierarchy and scope validation
P2-7-003 Notebook Entry API tests
P2-7-004 Note Item schemas/repository/service/router
P2-7-005 Note Item sequence_order validation
P2-7-006 Note Item API tests
P2-7-007 Consultation boundary inside Notebook Entry
P2-7-008 Follow-Up schemas/repository/service/router
P2-7-009 Follow-Up validation and tests
P2-7-010 Notification schemas/repository/service/router
P2-7-011 Notification mark-read / mark-all-read tests
P2-7-012 MinIO file upload URL service
P2-7-013 File upload complete/failure endpoints
P2-7-014 Upload Queue repository/service/router
P2-7-015 Upload Queue lifecycle tests
P2-7-016 Sync batch schema/service/router
P2-7-017 Sync idempotency and per-item result tests
P2-7-018 Membership/account guard tests for notebook/upload/sync
P2-7-019 API Gap document for P2-7
P2-7-020 Smoke test and README/API docs update
P2-7-021 Forbidden scope guard tests
```

Issue implementation order:

```text
1. Confirm P2-6 commit/push/merge status.
2. Inspect existing frozen models/enums for notebook_entries/note_items/follow_ups/notifications/upload_queue.
3. Create/update API Gap doc before guessing unclear behavior.
4. Implement Notebook Entry backend.
5. Implement Note Item backend.
6. Implement Follow-Up backend.
7. Implement Notification backend.
8. Implement Files upload-url/complete/upload-failed boundary.
9. Implement Upload Queue boundary.
10. Implement Sync batch boundary.
11. Run forbidden scope checks.
12. Run smoke tests.
```

---

# 29. Acceptance Criteria

P2-7 is acceptable when:

```text
Notebook Entry APIs work within frozen scope.
Note Item APIs work within frozen scope.
Consultation remains Notebook Entry Type only.
Follow-Up APIs work within frozen scope.
Notification APIs work within frozen scope.
POST /api/v1/notifications/mark-all-read works.
File upload URL, complete, and upload-failed APIs work.
Upload Queue works only against frozen upload_queue table/API.
Upload Queue API path is /api/v1/upload-queue only.
No /api/v1/upload-jobs API exists.
Sync batch works with per-item result mapping.
Sync canonical request uses items[] / action unless Owner approves alias support.
Sync payload mismatch with P1-2 Mobile is recorded as API Gap.
client_id idempotency is implemented if physical fields exist.
If client_id fields are missing, API Gap / Revision Proposal is created.
Membership and account guards protect all P2-7 endpoints.
Organization/farm/zone/tree hierarchy validation is enforced.
Nullable farm/zone/tree rules are preserved.
sequence_order behavior is deterministic and tested.
No hard delete is implemented unless explicitly frozen/approved.
No new tables are introduced.
No unapproved migrations are introduced.
No new RBAC roles are introduced.
No permission service is introduced.
No consultation service/entity/router is introduced.
No internal AI analysis is introduced.
No mobile UI is introduced.
No web UI is introduced.
No P2-8 work is introduced.
All previous P2 tests still pass.
New P2-7 tests pass.
Health endpoints remain unchanged.
alembic upgrade head remains PASS.
API Gap document records unresolved details.
```

---

# 30. Explicit Non-Goals

P2-7 must not implement:

```text
P2-8
Mobile app
Web app
Internal AI assistant
Ask AI analysis engine
AI result generation
Knowledge Candidate
Knowledge Library
Knowledge graph
Vector database
RAG
Search Workspace beyond basic keyword/filter if frozen
Simulator Workspace
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
GIS service
Farm boundary mapping
Zone boundary mapping
Tree GPS mapping
Audit table
Production deployment
Robot module
Commerce module
Advanced media processing
OCR
Speech-to-text
Image recognition
Disease diagnosis
Treatment recommendation
Video processing
Image thumbnail generation
Virus scanning
Background upload worker
CRDT
Realtime sync
MQTT sync engine
Multi-device merge engine
upload_jobs table
consultations table
```

---

# 31. Ready for Owner Review

## 31.1 Review Questions for Owner

Before freezing P2-7, Owner should confirm:

```text
1. Has P2-6 been committed, pushed, and merged?
2. Should Notebook Entry archive/status transition be implemented now or kept as API Gap?
3. Should Note Item delete be implemented, or deferred?
4. Confirm File Upload endpoints:
   - POST /api/v1/files/upload-url
   - POST /api/v1/files/complete
   - POST /api/v1/files/upload-failed
5. Confirm Upload Queue endpoint path:
   - /api/v1/upload-queue
6. Confirm no /api/v1/upload-jobs API.
7. Confirm sync canonical backend payload:
   - items[] / action
8. Confirm whether backend should also accept P1-2 Mobile alias:
   - operations[] / operation_type
9. Confirm client_id physical database support before coding idempotency.
10. Confirm Follow-Up APIs are included in P2-7.
11. Confirm Notification APIs are included in P2-7.
12. Confirm Media Read URL for Web viewer remains API Gap / later Web concern.
```

## 31.2 Freeze Instruction

This document is:

```text
Draft Final / Ready for Owner Review
```

Do not mark as frozen until Owner explicitly says:

```text
ok, freeze
```

---

# End of Document

ARI V1 — P2-7 Notebook / Upload / Sync Backend v1.0
Status: Draft Final / Ready for Owner Review


**************************************
ARI V1 — P2-7 Notebook / Upload / Sync Backend v1.0
Status: FROZEN
**************************************
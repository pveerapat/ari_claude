# ARI V1 — P2-8 Mobile App MVP Implementation v1.0

Project: ARI — Agricultural Intelligence Platform
Phase: P2 Coding Execution Phase
Document Number: P2-8
Document Type: Mobile App MVP Implementation Specification / Execution Document
Version: v1.0
Status: Draft Final / Ready for Owner Review
Freeze Status: NOT FROZEN
Prepared From: Frozen Source of Truth + P2-1 through P2-7 Coding Execution Authority

---

# 1. Document Control

## 1.1 Document Identity

```text
Document Title:
ARI V1 — P2-8 Mobile App MVP Implementation v1.0

Project:
ARI — Agricultural Intelligence Platform

Phase:
P2 Coding Execution Phase

Document Number:
P2-8

Document Status:
Draft Final / Ready for Owner Review

Freeze Status:
NOT FROZEN
```

## 1.2 Important Status Rule

This document is not frozen.

Do not mark this document as frozen unless Owner explicitly says:

```text
ok, freeze
```

Until then, this document is for Owner review only.

Do not proceed to actual coding implementation from this document until Owner approval / freeze.

---

# 2. Purpose

The purpose of P2-8 is to define the Flutter Mobile App MVP implementation scope after P2-7 Notebook / Upload / Sync Backend completion.

P2-8 defines:

```text
Mobile app implementation boundary
Mobile architecture boundary
Environment / API client boundary
Auth and session flow
Registration and onboarding flow
Membership boundary
Permission onboarding
Home screen and farm selector
Farm / Zone / Tree mobile flow
Notebook and note item mobile flow
File upload flow
Upload queue flow
Offline sync flow
Follow-up flow
Notification flow
Ask AI Now safe boundary
QR / ID boundary
Nightly upload / local reminder boundary
Local storage boundary
State management boundary
Error handling
Testing requirements
Smoke checklist
API Gap / Mobile Gap handling
GitHub issue breakdown
Acceptance criteria
Explicit non-goals
```

P2-8 must prepare a safe implementation target for Claude Code after Owner review.

P2-8 must not redesign ARI.

P2-8 must not create P2-9.

P2-8 must not authorize backend changes.

---

# 3. Frozen Source of Truth

P2-8 must follow these frozen documents:

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
ARI V1 — P2-7 Notebook / Upload / Sync Backend v1.0
```

P2-8 must preserve these invariants:

```text
One Platform
One Backend
One Database Architecture
One Mobile App
One Web App
One Domain Model
One RBAC System
```

---

# 4. Relationship to P2-1 through P2-7

## 4.1 Relationship to P2-1

P2-1 defines the coding execution order.

P2-8 corresponds to:

```text
Mobile App MVP Implementation
```

P2-8 comes after:

```text
P2-5 Auth and Mobile Onboarding Backend
P2-6 Farm Structure Backend
P2-7 Notebook / Upload / Sync Backend
```

P2-8 comes before:

```text
P2-9 Web App MVP
E2E integration
Prototype deployment
Pilot execution
```

## 4.2 Relationship to P2-2

P2-2 created the monorepo and reserved:

```text
mobile/
```

for the mobile app.

P2-8 must use the existing `mobile/` folder.

Do not create separate apps such as:

```text
owner_app/
farmer_app/
staff_app/
desktop_app/
web_app/
```

## 4.3 Relationship to P2-3

P2-3 created backend feature foundation.

P2-8 consumes existing backend APIs only.

P2-8 must not bypass backend layers.

## 4.4 Relationship to P2-4

P2-4 created the database and Alembic migration foundation.

P2-8 must not create:

```text
new database table
new database column
new enum
new migration
```

If a missing field is discovered, create API Gap / Mobile Gap.

## 4.5 Relationship to P2-5

P2-5 created Auth and Mobile Onboarding backend support.

P2-8 must implement mobile client flows for:

```text
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/refresh
GET /api/v1/auth/me
POST /api/v1/auth/logout
```

P2-8 must not create new auth endpoints.

P2-8 must not change JWT lifecycle.

If the implemented backend endpoint differs from the frozen P2-5 contract, create Mobile/API Gap.

## 4.6 Relationship to P2-6

P2-6 created Farm / Zone / Tree backend support.

P2-8 must implement mobile UI/client flows for:

```text
Farm list/detail/create/update where backend allows
Zone list/detail/create/update where backend allows
Tree list/detail/create/update where backend allows
```

P2-8 must respect backend authorization.

## 4.7 Relationship to P2-7

P2-7 created backend support for:

```text
Notebook Entries
Note Items
Follow-Ups
Notifications
Files / MinIO upload
Upload Queue
Offline Sync Batch
```

P2-8 must implement mobile client flows for these existing endpoints.

P2-8 must align sync with P2-7 backend canonical format:

```text
items[] / action
```

P2-8 must not silently support the older P1-2 mobile format:

```text
operations[] / operation_type
```

unless Owner explicitly approves a revision.

---

# 5. Current Backend State After P2-7

Backend is expected to support:

```text
Auth / Mobile Onboarding
Farm / Zone / Tree
Notebook Entries
Note Items
Follow-Ups
Notifications
Files / MinIO upload
Upload Queue
Offline Sync Batch
```

Confirmed backend endpoint set for P2-8 mobile consumption:

```text
GET /health
GET /api/v1/health

POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/refresh
GET /api/v1/auth/me
POST /api/v1/auth/logout

Farm / Zone / Tree APIs from P2-6

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

P2-8 must not call:

```text
/api/v1/upload-jobs
```

---

# 6. Known API Gaps Carried Into P2-8

P2-8 must consider these existing gaps from P2-7:

```text
API-GAP-P2-7-001 — zone_id without farm_id: infer parent or require explicit?
API-GAP-P2-7-005 — consultation_status in spec but missing from DB schema
API-GAP-P2-7-011 — Mobile uses operations[] / operation_type, but P0/P2-7 backend uses items[] / action
API-GAP-P2-7-017 — client_id column absent on notebook_entries and note_items
```

P2-8 must not resolve these through backend modification.

P2-8 may define safe mobile behavior and record Mobile/API Gap handling only.

---

# 7. Mobile MVP Boundary

## 7.1 Target Platform

```text
Flutter Mobile App
Android
iOS
```

## 7.2 One Mobile App Rule

P2-8 must implement one Flutter mobile app only.

Allowed:

```text
Role-aware screens
Membership-aware access states
Owner onboarding path
Owner family onboarding path
Farm staff onboarding path
```

Not allowed:

```text
separate owner app
separate farmer app
separate staff app
separate ARI staff app
Flutter Web
Flutter Desktop
Electron
native Android-only rewrite
native iOS-only rewrite
```

## 7.3 MVP Priority

P2-8 should prioritize:

```text
Register
Login
Restore session
Select farm context
Capture notebook evidence
Save locally
Upload files
Retry failed uploads
Sync batch
Review notebook
Track follow-ups
Read notifications
```

P2-8 must not attempt to implement future ARI intelligence platform scope.

---

# 8. Mobile Architecture Boundary

## 8.1 Required Initial Inspection

Before implementation, Claude Code must inspect:

```text
mobile/
mobile/pubspec.yaml
mobile/lib/
mobile/test/
mobile/android/
mobile/ios/
```

If `mobile/` is empty or skeleton only, implement minimal Flutter app structure defined in this document.

If existing mobile structure exists and is compatible with frozen scope, adapt to it.

Do not rewrite unrelated architecture.

## 8.2 Allowed Mobile Architecture

Allowed:

```text
Flutter app
API client
Auth/session store
Feature modules
Local storage for offline queue
Upload queue manager
Sync client
Permission service wrapper
Repository/provider/state-management layer consistent with existing project
```

## 8.3 Recommended Structure

```text
mobile/
├── pubspec.yaml
├── analysis_options.yaml
├── README.md
├── lib/
│   ├── main.dart
│   ├── app.dart
│   ├── core/
│   │   ├── config/
│   │   ├── auth/
│   │   ├── network/
│   │   ├── storage/
│   │   ├── permissions/
│   │   ├── sync/
│   │   ├── upload/
│   │   ├── errors/
│   │   └── utils/
│   ├── shared/
│   │   ├── widgets/
│   │   ├── models/
│   │   └── providers/
│   ├── features/
│   │   ├── auth/
│   │   ├── onboarding/
│   │   ├── home/
│   │   ├── farm_context/
│   │   ├── farm_structure/
│   │   ├── notebook/
│   │   ├── media_capture/
│   │   ├── upload_queue/
│   │   ├── sync/
│   │   ├── follow_ups/
│   │   ├── notifications/
│   │   ├── ask_ai/
│   │   ├── qr_id/
│   │   └── profile/
│   └── generated/
├── test/
│   ├── unit/
│   ├── widget/
│   ├── integration/
│   ├── auth/
│   ├── onboarding/
│   ├── farm_structure/
│   ├── notebook/
│   ├── upload_flow/
│   ├── offline_sync/
│   └── notifications/
├── android/
└── ios/
```

## 8.4 Forbidden Architecture

Do not introduce:

```text
micro-frontend
desktop architecture
web architecture
native Android-only rewrite
native iOS-only rewrite
separate farmer app
separate owner app
separate staff app
permission engine
QR registry module
consultation entity module
knowledge module
robot module
commerce module
```

---

# 9. Environment / API Client Boundary

## 9.1 Environment Configuration

P2-8 may define mobile environment configuration for:

```text
local backend base URL
Android emulator backend URL
iOS simulator backend URL
physical device backend URL
API timeout
upload timeout
sync timeout
debug logging flag
```

Example environment keys:

```text
ARI_API_BASE_URL
ARI_UPLOAD_TIMEOUT_SECONDS
ARI_SYNC_TIMEOUT_SECONDS
ARI_ENABLE_DEBUG_LOGS
```

Do not store secrets in committed files.

## 9.2 API Client Requirements

The mobile API client must:

```text
Use /api/v1 base path.
Attach Authorization: Bearer <access_token>.
Use refresh token flow when access token expires and refresh endpoint is available.
Parse standard success response.
Parse standard error envelope.
Handle 401 unauthorized.
Handle 403 forbidden.
Handle 422 validation error.
Handle no-internet state.
Handle timeout.
Avoid leaking token or secrets into logs.
```

## 9.3 API Client Non-Goals

P2-8 must not implement:

```text
GraphQL client
direct database client
direct MinIO metadata client
backend admin client
separate API gateway
new backend endpoint
```

---

# 10. Auth / Session Flow

## 10.1 Allowed Auth Scope

Allowed:

```text
Phone registration
Phone login
Refresh token flow using existing backend endpoint
Secure token storage
GET /api/v1/auth/me session restore
Logout boundary
```

## 10.2 Register by Phone Flow

Required fields:

```text
phone
name
password
farmer_status
farm_id only for owner_family / farm_staff
```

Allowed farmer_status values:

```text
owner
owner_family
farm_staff
```

Rules:

```text
phone is the mobile login identity.
password must never be logged.
registration requires internet.
mobile must use backend validation result.
mobile must not create local-only user accounts.
```

## 10.3 Login by Phone Flow

Required fields:

```text
phone
password
```

Rules:

```text
first login requires internet.
after successful login, mobile may support offline local use.
backend/API actions must show No Internet when offline.
```

## 10.4 Refresh Token Flow

P2-8 mobile must support:

```text
POST /api/v1/auth/refresh
```

Rules:

```text
Use existing P2-5 backend refresh endpoint only.
Store refresh token securely if returned by backend.
When access token expires and internet is available, attempt refresh.
If refresh succeeds, retry original request once.
If refresh fails, clear auth session and show login required.
Do not create new backend endpoint.
Do not change token lifetime.
Do not implement custom mobile-only token lifecycle.
```

If the implemented backend endpoint is missing, differs from frozen P2-5, or token lifecycle behavior is inconsistent, create:

```text
MOBILE-GAP-P2-8-001 — Refresh token behavior for mobile session renewal
```

## 10.5 Session Restore Flow

On app launch:

```text
1. Load secure access token if present.
2. If token exists, call GET /api/v1/auth/me when internet is available.
3. If auth/me succeeds, restore user/session state.
4. If auth/me returns 401 and refresh token exists, attempt POST /api/v1/auth/refresh.
5. If refresh succeeds, call auth/me again.
6. If refresh fails, clear session and show login.
7. If offline and a previous valid local session exists, allow local-only capture and local queue review.
8. If offline and no valid local session exists, show login required / internet required.
```

## 10.6 Logout Boundary

Logout must:

```text
Call POST /api/v1/auth/logout when online if endpoint is available.
Clear local access token.
Clear refresh token.
Keep unsynced local drafts unless Owner later approves destructive cleanup.
Return user to login screen.
```

---

# 11. Registration / Onboarding Flow

## 11.1 Farmer Status Selection

Mobile must show:

```text
owner
owner_family
farm_staff
```

Important rule:

```text
farmer_status is not an RBAC role.
```

Mobile must not translate farmer_status into its own permission matrix.

Backend remains the authorization authority.

## 11.2 Owner Onboarding

Owner flow:

```text
1. User selects owner.
2. User registers by phone.
3. Backend creates/assigns organization_id.
4. Mobile stores session.
5. Mobile shows permission onboarding.
6. Mobile prompts owner to create first farm if no farm exists.
7. Owner may create multiple farms.
8. Mobile shows Farm Selector after farms exist.
```

Owner may create:

```text
Farm
Zone
Tree
```

only where backend allows.

## 11.3 Owner Family / Farm Staff Onboarding

Owner family / farm staff flow:

```text
1. User selects owner_family or farm_staff.
2. User enters Farm ID.
3. User registers by phone.
4. Backend resolves organization_id from Farm ID.
5. Backend sets membership_status = pending_farm_approval.
6. Mobile shows Pending Farm Approval screen.
7. Mobile blocks protected farm-scoped functions until membership_status = active.
```

Mobile must not implement approval workflow.

If approval endpoint is missing or unclear, document a gap and keep pending screen.

---

# 12. Membership Boundary

Mobile must respect backend fields:

```text
farmer_status
membership_status
account_status
primary_farm_id
organization_id
```

## 12.1 Pending Membership

When:

```text
membership_status = pending_farm_approval
```

mobile must:

```text
Show pending approval state.
Allow profile/logout.
Allow session restore.
Block Add Note.
Block Farm Notebook.
Block Upload Queue.
Block Sync.
Block protected Farm/Zone/Tree features.
Avoid fake local farm creation.
```

## 12.2 Active Membership

When:

```text
membership_status = active
```

mobile may show protected farm-scoped functions according to backend access.

## 12.3 Account Status

When account status is not active or not allowed by backend:

```text
show blocked account state
hide protected actions
allow logout
do not bypass backend
```

## 12.4 No Local Permission Matrix

Mobile must not implement:

```text
permission service
permission matrix
ABAC
policy engine
farm membership engine
```

Mobile may implement UI visibility only as a convenience.

Backend remains the source of truth.

---

# 13. Permission Onboarding

P2-8 must implement permission onboarding for:

```text
Location
Camera
Microphone
Photos / Files
Notifications
```

## 13.1 General Permission Rules

```text
Request once after registration/login where appropriate.
Each feature must still check permission before use.
If denied, show clear fallback.
Do not permanently block the whole app if permission is denied.
Do not request unrelated permissions.
Do not treat mobile permission as backend authorization.
```

## 13.2 Location Permission

Used for:

```text
Create Farm GPS/time auto-fill if available.
Notebook entry location metadata if supported by mobile form and backend payload.
```

If denied:

```text
Allow manual farm location entry where backend supports it.
Allow note capture without GPS when frozen fields allow nullable location.
Show explanation.
```

## 13.3 Camera Permission

Required for:

```text
photo capture
video capture
QR / ID scan if optional QR helper is implemented
```

If denied:

```text
Show permission explanation.
Allow text/link/file items if available.
```

## 13.4 Microphone Permission

Required for:

```text
voice capture
video with audio if platform requires
```

If denied:

```text
Show permission explanation.
Allow photo/text/link/file items where possible.
```

## 13.5 Photos / Files Permission

Required for:

```text
file attachment
existing media selection
```

If denied:

```text
Allow direct camera capture if camera permission exists.
Allow text/link items.
```

## 13.6 Notification Permission

Required only for local/mobile reminders if implemented.

If denied:

```text
Backend notification list must still work.
Local notification reminder may be disabled.
Show explanation.
```

Do not create push notification provider in P2-8.

---

# 14. Home Screen Boundary

Home screen must preserve the fixed four primary buttons:

```text
Ask AI Now
Add Note
Farm Notebook
Notifications
```

## 14.1 Top Farm Selector

Home screen must include Farm Selector when user has accessible farms.

Farm Selector must:

```text
Show current active farm.
Allow switching among accessible farms.
Use primary_farm_id as default if available.
Fall back to first accessible farm only if backend response and UX make it safe.
Show no-farm state for owner before farm creation.
Show pending approval state for pending users.
```

If default farm behavior is unclear, create:

```text
MOBILE-GAP-P2-8-002 — Farm selector default farm behavior
```

## 14.2 Profile / Account Status

Profile area must show:

```text
name
phone
farmer_status
membership_status
account_status
active farm if selected
logout
```

Do not show RBAC role editing in mobile P2-8.

---

# 15. Farm / Zone / Tree Mobile Flow

## 15.1 Farm List

Mobile must call existing backend farm list endpoint.

Rules:

```text
Show farms accessible to current user.
Show empty state if none.
Show create farm button only for owner where backend allows.
Do not show inaccessible farms.
```

## 15.2 Farm Detail

Farm detail may show:

```text
farm name
location if available
description if available
status if available
zones
tree summary if available
```

## 15.3 Create Farm

Owner create farm flow:

```text
Farm name required.
Location may be auto-filled from phone GPS if permission granted.
Auto-filled location must be editable before save.
Submit to existing backend Farm API.
Use backend response as source of truth.
```

Do not generate farm_code unless field exists and backend supports it.

If user-friendly farm code is required later, create Mobile/API Gap.

## 15.4 Zone List / Detail / Create

Zone flow:

```text
List zones under selected farm.
Show zone detail.
Owner may create zone where backend allows.
owner_family and farm_staff cannot create zone.
Do not allow moving zone to another farm unless backend explicitly supports it.
```

## 15.5 Tree List / Detail / Create

Tree flow:

```text
List trees under selected zone or farm where backend supports it.
Show tree detail.
Owner may create tree where backend allows.
owner_family and farm_staff cannot create tree.
Tree registration remains optional.
```

---

# 16. Notebook Mobile Flow

## 16.1 Domain Rules

Preserve:

```text
Notebook Entry = Note Session
Note Item = Timeline Item
Consultation = Notebook Entry Type
```

Supported Notebook Entry types:

```text
note
consultation
```

Supported Note Item types:

```text
photo
video
voice
text
file
link
```

Preserve:

```text
Save Local
≠
Upload
≠
Analyze
```

## 16.2 Add Note Flow

Add Note must support:

```text
select active farm context if available
optional zone selection
optional tree selection
entry_type = note by default
entry_type = consultation only when user starts Ask AI / consultation flow boundary
title/summary if mobile form supports it
local draft save
timeline item capture
manual upload
sync batch upload
```

## 16.3 Consultation Note Boundary

Consultation is:

```text
Notebook Entry Type
```

Not allowed:

```text
consultation entity
consultation table
consultation router
consultation service
```

If `consultation_status` is required by UI but missing from backend/database, document:

```text
API-GAP-P2-7-005 — consultation_status in spec but missing from DB schema
```

Mobile must not add backend field.

## 16.4 Notebook List

Notebook list must:

```text
Show server notebook entries when online.
Show local unsynced drafts.
Clearly label local-only / pending upload / uploaded / failed.
Filter by active farm where safe.
Allow empty state.
Allow pull-to-refresh where simple.
```

## 16.5 Notebook Detail

Notebook detail must show:

```text
entry information
farm/zone/tree context when available
note item timeline
upload status
sync status
follow-up link if related
```

---

# 17. Note Item Capture Flow

## 17.1 Timeline Rule

Every note item must preserve:

```text
sequence_order
```

Rules:

```text
sequence_order starts at 1 for each local entry.
sequence_order increments by capture order.
Do not change sequence_order on retry.
Do not reorder items during upload unless user explicitly reorders and local state records it.
```

## 17.2 Photo Capture

Photo capture must:

```text
Check camera permission.
Save file locally first.
Create local note item with item_type = photo.
Assign local_item_id.
Assign client_id where applicable.
Add upload queue record.
```

## 17.3 Video Capture

Video capture must:

```text
Check camera and microphone permission where required.
Save file locally first.
Create local note item with item_type = video.
Assign local_item_id.
Assign client_id where applicable.
Add upload queue record.
```

## 17.4 Voice Capture

Voice capture must:

```text
Check microphone permission.
Save file locally first.
Create local note item with item_type = voice.
Assign local_item_id.
Assign client_id where applicable.
Add upload queue record.
```

## 17.5 Text Item

Text item must:

```text
Save text locally.
Create local note item with item_type = text.
Preserve sequence_order.
Sync metadata through normal endpoint or sync batch.
```

## 17.6 File Item

File item must:

```text
Check Photos / Files permission if platform requires.
Save local file reference.
Create local note item with item_type = file.
Add upload queue record.
Use presigned upload flow.
```

## 17.7 Link Item

Link item must:

```text
Accept URL input.
Save local note item with item_type = link.
Do not require file upload.
Sync metadata through normal endpoint or sync batch.
```

Do not create a separate external link entity.

---

# 18. File Upload Flow

## 18.1 Required Flow

Mobile file upload must follow:

```text
1. Save local file.
2. Create or keep local note item metadata.
3. Request upload URL:
   POST /api/v1/files/upload-url
4. Upload binary directly to MinIO presigned URL.
5. Complete upload:
   POST /api/v1/files/complete
6. Mark local upload queue item as completed.
7. Map local file/note item to server response if returned.
```

## 18.2 Upload Failed Flow

If upload fails:

```text
1. Keep local file.
2. Keep same client_id.
3. Keep same local_item_id.
4. Keep same sequence_order.
5. Mark upload queue item as failed.
6. Report failure:
   POST /api/v1/files/upload-failed
   if enough backend-required fields exist.
7. Allow manual retry.
```

## 18.3 Upload Object Key Gap

If object key format or file-to-note-item binding is unclear, create:

```text
MOBILE-GAP-P2-8-003 — Mobile file object key and note item binding behavior
```

## 18.4 Mobile Preview Gap

If backend does not provide read URL / media preview URL for uploaded media, mobile may:

```text
show local preview for local files
show metadata-only server items
show placeholder for remote media
```

Create:

```text
MOBILE-GAP-P2-8-004 — Media read URL for mobile preview
```

Do not invent new media read endpoint.

---

# 19. Upload Queue Flow

## 19.1 Upload Queue UI

Upload queue screen must show:

```text
pending uploads
uploading uploads
failed uploads
completed uploads if useful
retry action
local file existence status
entry/note item reference
error reason if available
```

## 19.2 Manual Upload

Manual upload must:

```text
check internet connectivity
check active session
check active membership
process pending/failed queue items
show progress
preserve local ids
preserve client ids
```

## 19.3 Retry Rule

On retry:

```text
Do not regenerate client_id.
Do not regenerate local_id.
Do not regenerate local_item_id.
Do not change sequence_order.
Do not create duplicate user-visible notebook entries.
Do not create duplicate note items as much as backend supports.
```

## 19.4 Backend Upload Queue API

Mobile may use existing backend upload_queue endpoints:

```text
POST /api/v1/upload-queue
GET /api/v1/upload-queue
GET /api/v1/upload-queue/{queue_id}
PATCH /api/v1/upload-queue/{queue_id}
POST /api/v1/upload-queue/{queue_id}/retry
```

Do not call:

```text
/api/v1/upload-jobs
```

---

# 20. Offline Sync Flow

## 20.1 Required Sync Contract

P2-8 mobile must align with P2-7 backend canonical payload:

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

P2-8 must not use the old P1-2 mobile shape:

```text
operations[] / operation_type
```

unless Owner explicitly approves.

## 20.2 Supported Sync Entity Types

Mobile may sync only entity types supported by P2-7 backend:

```text
notebook_entry
note_item
follow_up
notification
upload_queue
```

Do not sync unsupported entities through `/sync/batch`.

## 20.3 Local ID Mapping

Mobile must preserve:

```text
local_id
local_item_id
client_id
client_batch_id
device_id
sequence_order
```

After successful sync:

```text
map local_id → server_id
map local_item_id → server_item_id
mark local record as synced
keep local audit of mapping for retry safety
```

## 20.4 client_id Limitation

If backend lacks physical `client_id` columns on `notebook_entries` and `note_items`, mobile must document limitation:

```text
Backend may not fully prevent duplicate notebook entries or note items across retry.
Mobile must still preserve client_id locally and submit it when API accepts it.
Backend change requires Owner-approved revision.
```

Reference:

```text
API-GAP-P2-7-017 — client_id column absent on notebook_entries and note_items
```

## 20.5 Conflict Handling Boundary

Allowed:

```text
show sync failed
show backend validation error
allow retry
allow user to edit local draft and retry
```

Not allowed:

```text
CRDT
multi-device merge engine
AI deduplication
complex conflict resolver
realtime sync
MQTT sync engine
```

---

# 21. Follow-Up Flow

## 21.1 Follow-Up List

Mobile must show:

```text
due follow-ups
upcoming follow-ups
completed follow-ups if backend returns them
empty state
no internet state
```

## 21.2 Follow-Up Detail

Follow-up detail must show:

```text
related notebook entry / consultation if available
follow_up_day
due date if returned
outcome
notes
status if available
```

## 21.3 Outcome Update

Supported outcome values follow frozen backend/domain values.

Expected display:

```text
improved
same
worse
unknown
```

Mobile must use existing backend PATCH endpoint.

Do not invent new outcome values.

## 21.4 3 / 7 / 14 Day Display

Mobile may display follow-up periods:

```text
3 days
7 days
14 days
```

Do not create backend scheduler.

Do not create push notification provider.

---

# 22. Notification Flow

## 22.1 Notification List

Mobile must call:

```text
GET /api/v1/notifications
```

Show:

```text
notification message
status/read state
created date
type if returned
empty state
```

## 22.2 Notification Detail

Mobile must call:

```text
GET /api/v1/notifications/{notification_id}
```

Show notification content.

## 22.3 Mark Read

Mobile must call:

```text
PATCH /api/v1/notifications/{notification_id}/read
```

## 22.4 Mark All Read

Mobile must call:

```text
POST /api/v1/notifications/mark-all-read
```

## 22.5 Notification Permission Boundary

Backend notification API is separate from mobile OS notification permission.

If OS notification permission is denied:

```text
Backend notification list still works.
Local reminder notification does not show.
```

Do not create push provider.

---

# 23. Ask AI Now Boundary

P1-2 Mobile includes Ask AI Now as one of the four Home buttons.

For P2-8:

```text
Ask AI Now is UI / navigation boundary only unless an existing frozen backend or external-AI flow is already implemented and explicitly approved.
```

Allowed:

```text
Show Ask AI Now button.
Show safe placeholder / disabled state if backend flow is not available.
Allow user to create consultation-type Notebook Entry only if it maps to existing notebook entry API.
Show explanatory text that internal ARI AI is not implemented in P2-8.
```

Not allowed:

```text
internal AI engine
AI diagnosis engine
treatment recommendation engine
knowledge extraction
RAG
vector search
direct OpenAI/Gemini/Claude call from mobile unless Owner explicitly approves
```

If Ask AI Now cannot be connected safely to existing backend/API, create:

```text
MOBILE-GAP-P2-8-005 — Ask AI Now backend/API boundary
```

---

# 24. QR / ID Boundary

P2-8 may include QR / ID helper UI only as an optional mobile convenience if it can be implemented without backend change.

QR / ID in P2-8 is representation only.

It is not a domain entity.

It is not a backend registry.

## 24.1 Allowed QR / ID Behavior

Allowed:

```text
Scan existing ARI ID payload if already available:
- ari://farm/{farm_id}
- ari://zone/{zone_id}
- ari://tree/{tree_id}

Parse existing Farm / Zone / Tree ID.
Navigate to existing Farm / Zone / Tree detail through approved backend APIs.
Display existing Farm / Zone / Tree ID as text.
Display existing Farm / Zone / Tree ID as locally generated QR if package is already available or safely approved.
Use QR scan as optional shortcut for Farm / Zone / Tree selection.
```

## 24.2 Not Allowed

P2-8 must not implement:

```text
qr_registry table
QR registry service
QR registry API
QR ownership system
QR permission system
Owner QR
Block QR
New backend QR endpoint unless already approved/frozen
New QR database field
Separate QR domain entity
```

## 24.3 QR Must Be Optional

P2-8 mobile must continue to work without QR.

Core MVP flows must not depend on QR.

Required core selection methods remain:

```text
Farm list / selector
Zone list
Tree list
Manual Farm ID entry for owner_family / farm_staff onboarding
```

## 24.4 QR Gap Handling

If QR package choice, QR payload format, scan behavior, or backend QR endpoint availability is unclear, create:

```text
MOBILE-GAP-P2-8-016 — QR / ID scan and display boundary
```

Do not solve by backend change.

---

# 25. Nightly Upload / Local Reminder Boundary

P1-2 allows nightly upload default at 20:00.

For P2-8, this must be treated carefully as mobile-side behavior only.

Allowed:

```text
Show user-facing reminder preference for 20:00 if technically safe.
Show local reminder to open app and upload.
Run upload when app is open and online.
Queue remains persistent when app is closed.
Manual upload/retry always available.
```

Conditionally allowed only if platform/package behavior is verified:

```text
background task scheduling
background upload
local notification reminder
```

Not allowed:

```text
backend scheduler
server worker
push notification provider
guaranteed background upload claim
silent OS-level background uploads without platform review
```

If exact scheduling mechanism is unclear, create:

```text
MOBILE-GAP-P2-8-006 — Nightly upload mobile OS scheduling behavior
```

---

# 26. Local Storage Boundary

## 26.1 Required Local Data

Mobile must persist:

```text
secure auth token
refresh token if supported by backend
current user snapshot
active farm context
farm/zone/tree cache
local notebook drafts
local note items
local media file references
upload queue
sync queue
local_id to server_id mapping
device_id
client_batch_id history
client_id per local record
```

## 26.2 Secure Storage

Auth tokens must be stored in secure mobile storage.

Do not store tokens in plain text shared preferences.

Do not log tokens.

## 26.3 Local Database Package Choice

Before implementation, inspect existing `pubspec.yaml`.

If a local database package already exists, use the existing repo-consistent package.

If no local storage package exists, recommended minimal options are:

```text
Option A:
sqflite for local structured offline queue and mappings

Option B:
Hive/Isar only if already used or explicitly approved

Option C:
shared_preferences only for non-secret simple settings, not for offline queue
```

Recommendation for P2-8 if no package exists:

```text
Use the simplest durable local database option that supports structured queue records, local/server ID mapping, and offline retry.
Document the chosen package in mobile README.
Do not add heavy architecture.
```

If package choice cannot be resolved safely, create:

```text
MOBILE-GAP-P2-8-007 — Local storage package selection
```

---

# 27. State Management Boundary

Before implementation, inspect existing `pubspec.yaml` and `lib/` patterns.

If state management already exists, use the existing repo-consistent pattern.

If no state management package exists, recommended simple approach:

```text
ChangeNotifier-based providers
```

Use state management for:

```text
auth session
onboarding state
permission state
active farm context
notebook draft state
upload queue state
sync state
follow-up state
notification state
network status
```

Do not introduce heavy architecture solely by preference.

Do not introduce:

```text
micro-frontend state architecture
desktop state architecture
custom permission engine
domain event bus
CQRS
multi-app state split
```

If package choice is unclear, create:

```text
MOBILE-GAP-P2-8-008 — State management package selection
```

---

# 28. Error Handling / Empty States

P2-8 must implement basic error states:

```text
No internet
Pending membership
Upload failed
Retry available
Backend validation error
Unauthorized / session expired
Forbidden / no access
Not found
Empty farm list
Empty zone list
Empty tree list
Empty notebook
Empty notifications
Empty follow-ups
Permission denied
QR scan failed / unsupported QR payload if optional QR is implemented
```

## 28.1 No Internet State

When offline:

```text
Allow local capture after prior valid login.
Allow local draft review.
Allow upload queue review.
Disable backend actions.
Show No Internet for login/register/backend refresh if no connection.
```

## 28.2 Backend Validation Error

Show backend validation error in user-friendly form.

Do not show:

```text
stack trace
database error
MinIO credential
JWT internals
raw server exception
```

## 28.3 Session Expired

When backend returns 401:

```text
attempt POST /api/v1/auth/refresh if refresh token exists and internet is available
if refresh succeeds, retry original request once
if refresh fails, show login required
preserve unsynced local drafts
```

---

# 29. Testing Requirements

## 29.1 Test Categories

P2-8 implementation must include:

```text
Flutter unit tests
Widget tests
Integration tests where feasible
API client tests with mocked responses
Auth flow tests
Refresh token flow tests
Onboarding flow tests
Membership state tests
Farm selector tests
Farm/Zone/Tree UI tests
Notebook local draft tests
Note item sequence_order tests
Upload queue tests
File upload flow tests with mocked presigned URL
Sync payload builder tests
client_id retry preservation tests
Permission flow tests with mocked permission service
QR / ID optional boundary tests if QR helper is implemented
Error state tests
Forbidden scope tests
Smoke tests
```

## 29.2 Required Unit Tests

Required:

```text
Auth token store saves/loads/clears token.
Refresh token store saves/loads/clears token.
Session restore handles success.
Session restore handles 401.
Session restore attempts refresh when possible.
Refresh failure clears session and preserves unsynced local drafts.
Registration payload includes correct farmer_status.
owner_family/farm_staff registration requires Farm ID.
Pending membership blocks protected routes.
Farm selector picks primary_farm_id if available.
Note item sequence_order increments correctly.
Retry does not regenerate client_id.
Retry does not regenerate local_item_id.
Retry does not change sequence_order.
Sync payload builder outputs items[] / action.
Sync payload builder does not output operations[] / operation_type.
Upload queue preserves failed item for retry.
Permission denied fallback state is shown.
QR parser accepts allowed ari://farm, ari://zone, ari://tree payloads if QR helper is implemented.
QR parser rejects unsupported payloads if QR helper is implemented.
```

## 29.3 Required Widget Tests

Required:

```text
Login screen renders phone/password.
Register screen renders farmer_status selection.
Farm ID field appears for owner_family/farm_staff.
Pending approval screen blocks protected actions.
Home screen renders four buttons only.
Farm selector renders selected farm.
Add Note screen can add text item.
Notebook detail renders timeline order.
Upload queue screen renders failed item with retry.
Notifications screen renders mark-all-read action.
Follow-up screen renders outcome update controls.
Optional QR / ID scan entry point does not replace required manual/list selection flows.
```

## 29.4 Required Integration / Smoke-Oriented Tests

Where feasible:

```text
Register/login against local backend test environment.
Refresh session through existing backend refresh endpoint.
Create farm as owner.
Block create farm as owner_family/farm_staff.
Create notebook entry locally.
Add note items locally.
Upload file with mocked or local MinIO presigned URL flow.
Sync batch sends canonical payload.
Read notifications.
Mark notification read.
Update follow-up outcome.
Optional QR / ID scan navigates to existing Farm / Zone / Tree detail without backend QR registry.
```

---

# 30. Smoke Test Checklist

P2-8 implementation is acceptable only when this smoke checklist passes:

```text
[ ] mobile/ Flutter project exists and builds.
[ ] Android debug build starts.
[ ] iOS build/simulator starts if development machine supports it.
[ ] App uses one Flutter mobile app only.
[ ] No Flutter Web / desktop target is introduced as project scope.
[ ] API base URL can be configured for local backend.
[ ] GET /health or GET /api/v1/health can be checked from mobile/debug tool.
[ ] Register by phone works.
[ ] Login by phone works.
[ ] POST /api/v1/auth/refresh works if backend endpoint is present.
[ ] GET /api/v1/auth/me restores session.
[ ] Logout clears local session.
[ ] Pending farm approval screen appears for pending users.
[ ] Pending users cannot access Add Note / Farm Notebook / Upload / Sync.
[ ] Owner can create farm where backend allows.
[ ] Owner can create zone/tree where backend allows.
[ ] owner_family cannot create farm/zone/tree.
[ ] farm_staff cannot create farm/zone/tree.
[ ] Home screen has four primary buttons.
[ ] Farm selector displays accessible farms.
[ ] Add Note can save local draft.
[ ] Note item timeline preserves sequence_order.
[ ] Photo/video/voice/text/file/link item flows are present.
[ ] Permission denied fallback works.
[ ] Upload queue shows pending/failed/retry states.
[ ] File upload calls upload-url → MinIO URL → complete.
[ ] Upload failed can be reported.
[ ] Sync batch uses items[] / action.
[ ] Sync batch does not use operations[] / operation_type.
[ ] client_id is preserved on retry.
[ ] local_id to server_id mapping is stored after success.
[ ] Follow-up list/detail/outcome update works where backend supports it.
[ ] Notification list/detail/mark read/mark all read works.
[ ] Optional QR / ID feature, if implemented, uses existing IDs only.
[ ] Optional QR / ID feature does not create QR registry/API/service.
[ ] No backend files are modified except documentation/config references if explicitly allowed.
[ ] No backend migration is created.
[ ] No new backend API is introduced.
[ ] No internal AI assistant is implemented.
[ ] No permission service is implemented.
[ ] No QR registry is implemented.
[ ] No farm_memberships table is introduced.
[ ] No consultation entity/table/router is introduced.
[ ] Tests pass.
```

---

# 31. API Gap / Mobile Gap Handling

If implementation finds missing, unclear, or inconsistent details, create:

```text
docs/api-gaps/API-GAP-P2-8.md
```

or:

```text
docs/api-gaps/MOBILE-GAP-P2-8.md
```

Do not silently resolve by backend changes.

## 31.1 Expected P2-8 Gap Areas

```text
MOBILE-GAP-P2-8-001 — Refresh token behavior for mobile session renewal
MOBILE-GAP-P2-8-002 — Farm selector default farm behavior
MOBILE-GAP-P2-8-003 — Mobile file object key and note item binding behavior
MOBILE-GAP-P2-8-004 — Media read URL for mobile preview
MOBILE-GAP-P2-8-005 — Ask AI Now backend/API boundary
MOBILE-GAP-P2-8-006 — Nightly upload mobile OS scheduling behavior
MOBILE-GAP-P2-8-007 — Local storage package selection
MOBILE-GAP-P2-8-008 — State management package selection
MOBILE-GAP-P2-8-009 — Notification permission vs backend notification API
MOBILE-GAP-P2-8-010 — Pending membership UI copy and allowed actions
MOBILE-GAP-P2-8-011 — Offline login behavior after token expiry
MOBILE-GAP-P2-8-012 — Farm ID vs future farm_code display/join UX
MOBILE-GAP-P2-8-013 — zone_id/tree_id parent inference in mobile note forms
MOBILE-GAP-P2-8-014 — consultation_status display behavior
MOBILE-GAP-P2-8-015 — client_id limitation when backend lacks physical column
MOBILE-GAP-P2-8-016 — QR / ID scan and display boundary
```

## 31.2 Carried Forward API Gaps

P2-8 must reference, not resolve silently:

```text
API-GAP-P2-7-001 — zone_id without farm_id
API-GAP-P2-7-005 — consultation_status missing from DB schema
API-GAP-P2-7-011 — Sync batch payload naming mismatch
API-GAP-P2-7-017 — client_id column absent on notebook_entries and note_items
```

## 31.3 Gap Template

```markdown
# API Gap / Mobile Gap / Revision Proposal

Gap ID:
MOBILE-GAP-P2-8-00X

Title:
<short title>

Discovered In:
P2-8 Mobile App MVP Implementation

Related Frozen Document:
<document name>

Current Frozen Behavior:
<what frozen spec currently says>

Missing / Ambiguous Detail:
<what is missing or unclear>

Mobile Impact:
<why this matters for mobile>

Backend Impact:
<none / requires Owner-approved backend revision>

Proposed Handling:
<option A / option B / defer>

Scope Risk:
Does this introduce backend change?
Does this introduce new entity?
Does this introduce new table?
Does this introduce new role?
Does this introduce new architecture?

Recommendation:
<recommended action>

Status:
Draft / Owner Review / Approved / Rejected
```

---

# 32. GitHub Issue Breakdown

Recommended P2-8 implementation issues:

```text
P2-8-001 Mobile project inspection and setup
P2-8-002 Mobile environment and API client foundation
P2-8-003 Secure token storage and session manager
P2-8-004 Auth screens: phone login/register/logout
P2-8-005 GET /auth/me session restore
P2-8-006 POST /auth/refresh mobile token renewal
P2-8-007 Farmer status onboarding
P2-8-008 Owner onboarding and create farm flow
P2-8-009 owner_family/farm_staff Farm ID join and pending screen
P2-8-010 Permission onboarding
P2-8-011 Home screen with four buttons and farm selector
P2-8-012 Profile/account status screen
P2-8-013 Farm list/detail/create UI
P2-8-014 Zone list/detail/create UI
P2-8-015 Tree list/detail/create UI
P2-8-016 Notebook local draft model and storage
P2-8-017 Add Note flow
P2-8-018 Note item timeline and sequence_order
P2-8-019 Photo/video capture integration
P2-8-020 Voice capture integration
P2-8-021 Text/file/link item capture
P2-8-022 Upload queue UI and local retry state
P2-8-023 File upload presigned URL flow
P2-8-024 Sync batch client using items[] / action
P2-8-025 client_id/local_id/server_id mapping
P2-8-026 Follow-up list/detail/outcome update
P2-8-027 Notification list/detail/mark read/mark all read
P2-8-028 Ask AI Now safe boundary/placeholder
P2-8-029 QR / ID optional helper boundary
P2-8-030 Nightly upload/local reminder boundary
P2-8-031 Error and empty states
P2-8-032 Mobile tests and smoke checklist
P2-8-033 P2-8 API/Mobile gap document
P2-8-034 Mobile README update
```

---

# 33. Acceptance Criteria

P2-8 is ready for implementation after Owner review when:

```text
[ ] Document status is Draft Final / Ready for Owner Review.
[ ] Scope is limited to Flutter Mobile App for Android/iOS.
[ ] P2-8 does not authorize backend implementation.
[ ] P2-8 does not authorize backend migration.
[ ] P2-8 does not authorize new backend API.
[ ] P2-8 does not authorize P2-9.
[ ] Source of Truth list is complete.
[ ] Relationship to P2-1 through P2-7 is clear.
[ ] Auth/session flow uses P2-5 endpoints only.
[ ] POST /api/v1/auth/refresh is included as existing P2-5 auth endpoint.
[ ] Membership boundary uses backend fields only.
[ ] farmer_status is not treated as RBAC role.
[ ] Permission onboarding is defined.
[ ] Home screen four-button rule is preserved.
[ ] Farm / Zone / Tree mobile flow follows P2-6 backend.
[ ] Notebook / Note Item mobile flow follows P0/P1-2/P2-7.
[ ] Save Local ≠ Upload ≠ Analyze is preserved.
[ ] File upload uses upload-url → MinIO → complete flow.
[ ] Upload queue and retry rules preserve client_id/local IDs.
[ ] Offline sync uses P2-7 canonical items[] / action.
[ ] P2-8 does not silently support operations[] / operation_type.
[ ] Ask AI Now is kept as safe UI/navigation boundary.
[ ] QR / ID is representation-only and optional.
[ ] QR registry/API/service is not introduced.
[ ] Nightly upload is mobile-only and does not create backend scheduler.
[ ] Local storage boundary is defined.
[ ] State management boundary is defined.
[ ] Error/empty states are defined.
[ ] Tests are defined.
[ ] Smoke checklist is defined.
[ ] API Gap / Mobile Gap handling is defined.
[ ] Explicit Non-Goals are complete.
```

---

# 34. Explicit Non-Goals

P2-8 must not implement:

```text
P2-9
Web App
Desktop App
Electron App
Flutter Desktop
Flutter Web

Backend implementation
Backend migration
New backend table
New backend API
Backend scheduler
Push notification provider

Internal AI assistant
Ask AI backend engine
AI diagnosis engine
Treatment recommendation engine
Knowledge extraction
Knowledge Candidate entity
Knowledge Library entity
Knowledge graph
Vector database
RAG
Semantic search
LLM search

Search Workspace
Simulator Workspace
Knowledge Workspace

QR registry
QR API
QR service
QR ownership system
QR permission system
Owner QR
Block QR

Permission service
Permission matrix
ABAC
Policy engine
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
```

---

# 35. Self-Check Before Owner Review

## 35.1 P1-2 Mobile Cross-Check

```text
PASS — Android/iOS only.
PASS — One Flutter Mobile App preserved.
PASS — Phone registration/login preserved.
PASS — Owner / owner_family / farm_staff onboarding preserved.
PASS — Permission onboarding preserved.
PASS — Offline local capture preserved.
PASS — Notebook timeline preserved.
PASS — Ask AI Now kept as safe boundary.
PASS — QR / ID kept as optional representation-only helper.
PASS — Web/Desktop out of scope.
```

## 35.2 P2-5 Auth Cross-Check

```text
PASS — Uses existing auth/register, auth/login, auth/refresh, auth/me, auth/logout.
PASS — Does not create new auth backend endpoint.
PASS — Does not change JWT lifecycle.
PASS — Refresh token behavior included as existing P2-5 endpoint.
PASS — farmer_status remains non-RBAC onboarding field.
```

## 35.3 P2-6 Farm Structure Cross-Check

```text
PASS — Owner can create Farm/Zone/Tree where backend allows.
PASS — owner_family/farm_staff creation blocked.
PASS — pending_farm_approval blocks protected farm-scoped functions.
PASS — No farm_memberships table introduced.
PASS — Farm ID remains canonical join reference.
PASS — farm_code uncertainty carried as gap if needed.
```

## 35.4 P2-7 Notebook / Upload / Sync Cross-Check

```text
PASS — Mobile uses existing P2-7 endpoints.
PASS — No backend changes required.
PASS — No backend migration required.
PASS — No upload_jobs API used.
PASS — Sync aligned to items[] / action.
PASS — operations[] / operation_type not silently supported.
PASS — client_id/local_id retry rules preserved.
PASS — client_id physical DB limitation documented.
```

## 35.5 Architecture / Scope Cross-Check

```text
PASS — No new backend service.
PASS — No new database table.
PASS — No new domain entity.
PASS — No new RBAC role.
PASS — No permission service.
PASS — No QR registry.
PASS — No consultation entity.
PASS — No internal AI assistant.
PASS — No knowledge graph/vector/RAG.
PASS — No web/desktop scope.
PASS — Save Local ≠ Upload ≠ Analyze preserved.
```

---

# 36. Ready for Owner Review

```text
Document:
ARI V1 — P2-8 Mobile App MVP Implementation v1.0

Status:
Draft Final / Ready for Owner Review

Freeze Status:
NOT FROZEN

Owner Decision Required:
Review and approve scope before coding implementation.

Freeze Command:
Only mark this document as FROZEN if Owner explicitly says:

ok, freeze
```

After freeze, P2-8 may be used to create a Claude Code implementation prompt for Mobile App MVP implementation.

Until freeze, this document is not an implementation authorization.

---
*************************************** 2026-06-29
ARI V1 — P2-8 Mobile App MVP Implementation v1.0
Status: FROZEN
***************************************
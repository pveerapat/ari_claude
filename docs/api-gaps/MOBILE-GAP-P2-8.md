# MOBILE-GAP-P2-8 — Mobile App MVP Implementation Gaps

Phase: P2-8 Mobile App MVP Implementation
Status: OPEN
Created: 2026-06-29

---

## MOBILE-GAP-P2-8-001 — Refresh token behavior for mobile session renewal

Gap ID: MOBILE-GAP-P2-8-001
Discovered In: P2-8 Mobile App MVP Implementation
Related Frozen Document: ARI V1 — P2-5 Auth and Mobile Onboarding Backend v1.0

Current Frozen Behavior:
POST /api/v1/auth/refresh exists per P2-5. Token lifetime and refresh token format are not fully specified in frozen docs.

Missing / Ambiguous Detail:
- Does POST /api/v1/auth/refresh require `refresh_token` in the body, or a Bearer header?
- Is refresh_token returned in login/register response body or only in cookies?
- What is the refresh token lifetime?
- What happens on concurrent refresh requests from multiple mobile sessions?

Mobile Impact:
Mobile session restore (P2-8 §10.4) depends on this behavior. If refresh token is not returned in login body, mobile cannot persist it securely.

Backend Impact: None — mobile adapts to existing backend behavior.

Proposed Handling:
Option A: Refresh token in response body (current mobile implementation assumes this).
Option B: Cookie-based — requires platform cookie handling.

Scope Risk:
- Does this introduce backend change? No
- Does this introduce new entity? No
- Does this introduce new table? No
- Does this introduce new role? No
- Does this introduce new architecture? No

Recommendation: Owner to confirm P2-5 refresh token response format.
Status: Draft

---

## MOBILE-GAP-P2-8-002 — Farm selector default farm behavior

Gap ID: MOBILE-GAP-P2-8-002
Discovered In: P2-8 Mobile App MVP Implementation
Related Frozen Document: ARI V1 — P2-6 Farm Structure Backend v1.0

Current Frozen Behavior:
primary_farm_id is returned in GET /auth/me user object.

Missing / Ambiguous Detail:
When primary_farm_id is null and multiple farms exist, which farm should be default-selected?
Current implementation: first farm in list response.

Mobile Impact:
User sees unexpected active farm if primary_farm_id is null but multiple farms exist.

Backend Impact: None.

Proposed Handling:
Option A: Use first farm from list (current).
Option B: Always require explicit user selection when primary_farm_id is null.

Scope Risk: None.

Recommendation: Owner to confirm default farm selection rule.
Status: Draft

---

## MOBILE-GAP-P2-8-003 — Mobile file object key and note item binding behavior

Gap ID: MOBILE-GAP-P2-8-003
Discovered In: P2-8 Mobile App MVP Implementation
Related Frozen Document: ARI V1 — P2-7 Notebook / Upload / Sync Backend v1.0
Reference: API-GAP-P2-7-007 — Uploaded file to Note Item binding behavior

Current Frozen Behavior:
POST /api/v1/files/upload-url returns presigned URL and file_id.
POST /api/v1/files/complete receives file_id and marks it complete.

Missing / Ambiguous Detail:
- Does POST /files/complete accept notebook_entry_id and note_item_id to bind the file to a note item?
- What is the exact response shape from /files/upload-url?
- Is `file_id` or `id` used in the response?
- Is `object_key` returned and required for /files/complete?

Mobile Impact:
File upload flow (upload_manager.dart) assumes file_id and object_key in response.
If response shape differs, upload completion will fail silently.

Backend Impact: None — mobile adapts.

Proposed Handling:
Option A: Mock presigned URL flow in tests (current approach).
Option B: Owner confirms exact response shape from P2-7 implementation.

Scope Risk: None.

Recommendation: Owner to confirm /files/upload-url and /files/complete response shapes.
Status: Draft

---

## MOBILE-GAP-P2-8-004 — Media read URL for mobile preview

Gap ID: MOBILE-GAP-P2-8-004
Discovered In: P2-8 Mobile App MVP Implementation
Related Frozen Document: ARI V1 — P0 API Specification v1.0
Reference: API-GAP-P2-7-015 — Media read URL endpoint for Web media viewer

Current Frozen Behavior:
No read URL / media preview endpoint is defined in P2-7 frozen scope.

Missing / Ambiguous Detail:
After file upload, mobile has no way to fetch the media back for preview.

Mobile Impact:
After upload, note items show "saved locally" or placeholder text for media.
Local preview (before upload) works using local file path.
Remote preview (after upload) is not available.

Backend Impact: Requires Owner-approved new endpoint in future phase.

Proposed Handling:
Option A: Show local preview for local files; metadata-only for server items (current).
Option B: Owner approves read URL endpoint in P2-9.

Scope Risk:
- New endpoint would be required in future phase — not P2-8 scope.

Recommendation: Document gap. Defer to future Owner-approved mobile revision / post-P2-8 mobile enhancement.
Status: Draft

---

## MOBILE-GAP-P2-8-005 — Ask AI Now backend/API boundary

Gap ID: MOBILE-GAP-P2-8-005
Discovered In: P2-8 Mobile App MVP Implementation
Related Frozen Document: ARI V1 — P1-2 Mobile App Implementation Specification v1.0

Current Frozen Behavior:
Ask AI Now is one of the four home screen buttons.
No AI backend is implemented in P2-7 or earlier.

Missing / Ambiguous Detail:
No safe AI backend flow exists to connect Ask AI Now to in P2-8.

Mobile Impact:
Ask AI Now screen is a UI/navigation placeholder.
It allows creating consultation-type Notebook Entry (via existing notebook API).
It does NOT call LLM, RAG, vector search, or external AI service.

Backend Impact: AI backend is future scope.

Proposed Handling:
Current: Show placeholder + consultation note entry point.
Future: Owner to approve and define AI backend flow for P2-9+.

Scope Risk: None. No forbidden scope introduced.

Recommendation: Confirmed safe. Keep as placeholder.
Status: Resolved (within P2-8 scope)

---

## MOBILE-GAP-P2-8-006 — Nightly upload mobile OS scheduling behavior

Gap ID: MOBILE-GAP-P2-8-006
Discovered In: P2-8 Mobile App MVP Implementation
Related Frozen Document: ARI V1 — P1-2 Mobile App Implementation Specification v1.0

Current Frozen Behavior:
P1-2 mentions nightly upload default 20:00.

Missing / Ambiguous Detail:
Background upload/scheduling on Android and iOS has significant platform restrictions.
WorkManager (Android) and BGTaskScheduler (iOS) have battery/connectivity limitations.
Neither platform guarantees background execution time.

Mobile Impact:
P2-8 implements upload-when-open-and-online only.
Manual upload/retry is always available.
Persistent queue survives app close.
No guaranteed background upload is claimed.

Backend Impact: None — nightly upload is mobile-side only.

Proposed Handling:
Option A: Add flutter_background_fetch or workmanager package in future phase (P2-9).
Option B: Local notification reminder at 20:00 using flutter_local_notifications.

Scope Risk:
- Backend scheduler: not introduced.
- Push notification provider: not introduced.

Recommendation: Defer background scheduling to future Owner-approved mobile revision / post-P2-8 mobile enhancement.
Status: Draft

---

## MOBILE-GAP-P2-8-007 — Local storage package selection

Gap ID: MOBILE-GAP-P2-8-007
Discovered In: P2-8 Mobile App MVP Implementation

Current Frozen Behavior:
No local DB package was pre-selected in P2-2 mobile skeleton.

Missing / Ambiguous Detail:
Three viable options: sqflite, Hive/Isar, or SharedPreferences (insufficient for queue).

Mobile Impact:
P2-8 selected `sqflite` as the minimal durable structured database.

Reason for sqflite selection:
- Most widely supported Flutter SQLite package
- Supports relational queries for upload queue, ID mapping, local drafts
- No code generation required (unlike Isar)
- SharedPreferences is insufficient for structured queue records

Scope Risk: None. Package selection is mobile-only.

Recommendation: Confirm sqflite is acceptable.
Status: Resolved (sqflite selected)

---

## MOBILE-GAP-P2-8-008 — State management package selection

Gap ID: MOBILE-GAP-P2-8-008
Discovered In: P2-8 Mobile App MVP Implementation

Current Frozen Behavior:
No state management package pre-selected in P2-2 mobile skeleton.

Missing / Ambiguous Detail:
Options: ChangeNotifier + provider, Bloc, Riverpod, GetX.

Mobile Impact:
P2-8 uses `provider` with ChangeNotifier-based pattern.

Reason for provider selection:
- Recommended in P2-8 spec §27
- Simple, minimal overhead
- Flutter official recommendation for moderate complexity
- No code generation required

Scope Risk: None.

Recommendation: Confirmed. provider + ChangeNotifier used throughout.
Status: Resolved (provider selected)

---

## MOBILE-GAP-P2-8-009 — Notification permission vs backend notification API

Gap ID: MOBILE-GAP-P2-8-009
Discovered In: P2-8 Mobile App MVP Implementation

Current Frozen Behavior:
GET /api/v1/notifications returns notifications from backend.
Mobile OS notification permission controls local/push notifications only.

Missing / Ambiguous Detail:
If OS notification permission is denied, backend notification LIST still works.
No push notification provider is implemented in P2-8.

Mobile Impact:
Backend notification list is always available regardless of OS permission.
Local notification reminder requires OS permission.
P2-8 does not implement push notification provider.

Backend Impact: None.

Recommendation: Resolved within scope. Document for future push implementation.
Status: Resolved

---

## MOBILE-GAP-P2-8-010 — Pending membership UI copy and allowed actions

Gap ID: MOBILE-GAP-P2-8-010
Discovered In: P2-8 Mobile App MVP Implementation

Missing / Ambiguous Detail:
Exact copy and action list for pending_farm_approval screen.
Which specific routes/features should be blocked vs allowed?

Current Implementation:
Blocked: Add Note, Farm Notebook, Upload Queue, Sync, Farm/Zone/Tree creation.
Allowed: Profile, Logout, Session restore, Check approval status.

Recommendation: Owner to confirm copy and blocked/allowed list.
Status: Draft

---

## MOBILE-GAP-P2-8-011 — Offline login behavior after token expiry

Gap ID: MOBILE-GAP-P2-8-011
Discovered In: P2-8 Mobile App MVP Implementation

Missing / Ambiguous Detail:
If user is offline and access token has expired, but refresh token also expired or network unavailable — what should mobile do?

Current Implementation:
Session restore flow: if offline and prior valid session token exists, allow local access.
If completely offline and no cached user object, show login required.

Backend Impact: None.

Recommendation: Owner to confirm acceptable offline behavior.
Status: Draft

---

## MOBILE-GAP-P2-8-012 — Farm ID vs future farm_code display/join UX

Gap ID: MOBILE-GAP-P2-8-012
Discovered In: P2-8 Mobile App MVP Implementation
Reference: P2-6 farm structure

Missing / Ambiguous Detail:
Farm ID is a UUID — difficult for users to share verbally.
P1-2 mentions "farm_code" for owner_family/farm_staff join flow.
farm_code is not in frozen P2-6 backend schema.

Mobile Impact:
owner_family/farm_staff enter Farm ID (UUID) to join.
UUID is difficult to type on mobile.

Backend Impact: farm_code field would require Owner-approved migration.

Proposed Handling:
Option A: Keep UUID-based Farm ID entry (current).
Option B: Owner approves farm_code addition in P2-9 backend.

Recommendation: Document gap. Defer farm_code to future Owner-approved mobile revision / post-P2-8 mobile enhancement.
Status: Draft

---

## MOBILE-GAP-P2-8-013 — zone_id/tree_id parent inference in mobile note forms

Gap ID: MOBILE-GAP-P2-8-013
Discovered In: P2-8 Mobile App MVP Implementation
Reference: API-GAP-P2-7-001 — zone_id without farm_id inference

Current Frozen Behavior:
Backend requires explicit farm_id with zone_id; explicit zone_id with tree_id.
Inference is not implemented.

Mobile Impact:
Add Note form must pass farm_id explicitly when providing zone_id.
Mobile must carry farm_id context from active farm selector.

Backend Impact: None — mobile adapts to explicit parent ID requirement.

Recommendation: Mobile always passes farm_id from active context. Resolved within P2-8.
Status: Resolved

---

## MOBILE-GAP-P2-8-014 — consultation_status display behavior

Gap ID: MOBILE-GAP-P2-8-014
Discovered In: P2-8 Mobile App MVP Implementation
Reference: API-GAP-P2-7-005 — consultation_status in spec but missing from DB schema

Current Frozen Behavior:
Consultation is a Notebook Entry type (entry_type = 'consultation').
consultation_status field is in spec but NOT in frozen DB schema.

Mobile Impact:
consultation_status cannot be displayed on mobile because it does not exist in backend response.
Notebook Entry analysis_status field is used as a proxy where available.

Backend Impact: consultation_status requires Owner-approved migration.

Proposed Handling:
Mobile does not show consultation_status. Uses analysis_status or omits status display.

Recommendation: Defer consultation_status display to future Owner-approved revision.
Status: Draft

---

## MOBILE-GAP-P2-8-015 — client_id limitation when backend lacks physical column

Gap ID: MOBILE-GAP-P2-8-015
Discovered In: P2-8 Mobile App MVP Implementation
Reference: API-GAP-P2-7-017 — client_id column absent on notebook_entries and note_items

Current Frozen Behavior:
Backend notebook_entries and note_items tables do not have client_id columns.

Mobile Impact:
Mobile preserves client_id locally (in local_notebook_entries and local_note_items SQLite tables).
Mobile submits client_id in sync batch payload.
Backend may not store or use client_id — so duplicate prevention on backend is limited.
Mobile itself does not duplicate entries as long as client_id/local_id is preserved.

Backend Impact: client_id column requires Owner-approved migration.

Proposed Handling:
Mobile-side deduplication: never regenerate client_id on retry.
Backend deduplication: not available in P2-8 — risk of duplicate entries on retry.

Recommendation: Document limitation. Backend change deferred to Owner approval.
Status: Draft

---

## MOBILE-GAP-P2-8-016 — QR / ID scan and display boundary

Gap ID: MOBILE-GAP-P2-8-016
Discovered In: P2-8 Mobile App MVP Implementation

Current Frozen Behavior:
QR / ID is optional helper UI only.
Allowed: ari://farm/{id}, ari://zone/{id}, ari://tree/{id} representation.
Not allowed: QR registry, QR API, QR service.

Missing / Ambiguous Detail:
- Which QR scanner package to use? (qr_code_scanner, mobile_scanner, etc.)
- QR scanner packages not included in P2-8 base pubspec.yaml.
- Camera-based QR scan UI not implemented in P2-8.

Mobile Impact:
P2-8 implements manual ARI ID entry and URI parsing only.
Camera QR scan requires additional package selection and Owner approval.

Backend Impact: None.

Implemented Boundary (P2-8):
- QR/ID Helper screen: manual text entry of ARI IDs only
- URI parser accepts ari://farm/{id}, ari://zone/{id}, ari://tree/{id} — navigates to that entity
- No QR registry, QR API, or QR service of any kind is implemented
- No camera QR scanning is implemented (no qr_code_scanner / mobile_scanner package included)
- No new backend entity, table, or endpoint is introduced

Proposed Handling for Future:
Option A: Add mobile_scanner in a future phase after Owner approves package.
Option B: Keep manual ID entry as the only QR input method.

Core MVP flows do not depend on QR.

Recommendation: Defer camera QR scanning to future Owner-approved mobile revision / post-P2-8 mobile enhancement.
Status: Draft

---

## MOBILE-GAP-P2-8-017 — Health endpoint URL convention and ApiClient base URL

Gap ID: MOBILE-GAP-P2-8-017
Discovered In: P2-8 Mobile App MVP Implementation
Related Frozen Document: ARI V1 — P2-5 Auth and Mobile Onboarding Backend v1.0

Clarification (not a blocking gap):

Two health endpoints exist on the ARI backend:
- Root health:  GET /health            → `${apiBaseUrl}/health`
- API health:   GET /api/v1/health     → `${apiBaseUrl}/api/v1/health`

ApiClient always prefixes all paths with `${AppConfig.apiV1}` (= `${apiBaseUrl}/api/v1`).

Consequence:
- `apiClient.get('/health')` → calls `${apiBaseUrl}/api/v1/health` — this is the API v1 health endpoint
- The root health `GET /health` is NOT reachable through ApiClient
- To call root health, use `http.Client.get(Uri.parse('${AppConfig.apiBaseUrl}/health'))` directly

Recommendation:
For connectivity checks in mobile, `GET /api/v1/health` via ApiClient is sufficient.
If the root health endpoint is ever needed separately (e.g., load balancer health probe),
call it outside of ApiClient using `http.get(Uri.parse('${AppConfig.apiBaseUrl}/health'))`.

Status: Clarified (informational — no backend change needed)

---

## Carried Forward API Gaps (from P2-7)

The following P2-7 gaps are referenced in P2-8 mobile handling but NOT resolved:

- API-GAP-P2-7-001 — zone_id without farm_id: Mobile always passes explicit farm_id.
- API-GAP-P2-7-005 — consultation_status missing from DB schema: Mobile does not show it.
- API-GAP-P2-7-011 — Sync batch payload naming mismatch: Mobile uses items[]/action only.
- API-GAP-P2-7-017 — client_id column absent: Mobile preserves client_id locally, limitation documented above.

# API-GAP-P2-7 — Notebook / Upload / Sync Backend

Phase: P2-7 Implementation
Status: OPEN
Created: 2026-06-29

---

## API-GAP-P2-7-001 — Notebook hierarchy inference for zone_id/tree_id without explicit parent IDs

**Status:** OPEN

**Description:**
When a client provides `zone_id` without `farm_id`, or `tree_id` without `zone_id`,
the frozen spec does not define whether the backend should infer the parent IDs
from the child entity or require explicit parent IDs in the request.

**Current Implementation:**
Explicit parent IDs are required. If `zone_id` is provided without `farm_id`,
a 422 error is returned. If `tree_id` is provided without `zone_id`, a 422 error
is returned.

**Owner Decision Needed:**
- Allow inference (look up zone's farm_id automatically)?
- Require explicit parent IDs (current behavior)?

---

## API-GAP-P2-7-002 — Notebook Entry archive/status transition behavior

**Status:** OPEN

**Description:**
The API spec mentions `PATCH /api/v1/notebook-entries/{entry_id}/archive` for
archiving entries. However, the frozen `notebook_entries` schema does not include
an `archived_at` or `is_archived` column, nor a `status` field.

**Current Implementation:**
`PATCH /api/v1/notebook-entries/{entry_id}` supports updating `analysis_status`
and other fields. No dedicated archive endpoint is implemented.

**Owner Decision Needed:**
- Add `archived_at` column to `notebook_entries`?
- Use `analysis_status` field as a proxy for archive state?
- Implement `/archive` endpoint?

---

## API-GAP-P2-7-003 — Note Item delete behavior

**Status:** OPEN

**Description:**
The API spec includes `DELETE /api/v1/note-items/{item_id}`. The frozen domain
model states "Evidence First" principle and "Hard Delete Not Recommended."

**Current Implementation:**
No DELETE endpoint is implemented. Physical deletion of media from MinIO
would also need to be handled.

**Owner Decision Needed:**
- Implement soft delete (add `deleted_at` column)?
- Skip DELETE entirely?
- Physical delete for text/link items only?

---

## API-GAP-P2-7-004 — Note Item sequence_order uniqueness/auto-assignment rule

**Status:** RESOLVED (P2-7 Decision)

**Description:**
The frozen spec does not define whether `sequence_order` must be unique per entry
or whether duplicate sequence orders are allowed.

**Current Implementation:**
If `sequence_order` is not provided, it is auto-assigned as `max(sequence_order) + 1`
for the entry. Provided values are accepted as-is. No uniqueness constraint is enforced
at the database level (per frozen schema).

**Owner Decision Needed:**
- Enforce uniqueness constraint on (entry_id, sequence_order)?

---

## API-GAP-P2-7-005 — Consultation AI/status field alignment

**Status:** OPEN

**Description:**
The P0 API spec references `consultation_status` as a field on Notebook Entries
(for filtering and in the response). However, the frozen `notebook_entries` SQLAlchemy
model (from P2-4) does not include a `consultation_status` column.

Available consultation-related fields in the model:
- `external_ai` (ExternalAI enum: chatgpt/gemini/claude/other) → exposed as `ai_provider` in API
- `ai_usefulness_status` (String: useful/not_useful/later)
- `learned_summary` (Text)

**Current Implementation:**
`ai_provider`, `ai_usefulness_status`, and `learned_summary` are supported.
`consultation_status` is NOT exposed in the API because no corresponding column exists.

**Owner Decision Needed:**
- Add `consultation_status` column to `notebook_entries` via migration?
- Map `consultation_status` to `ai_usefulness_status`?

---

## API-GAP-P2-7-006 — File upload endpoint naming conflict

**Status:** RESOLVED (P2-7 Decision)

**Description:**
Frozen canonical endpoint names:
- `POST /api/v1/files/upload-url`
- `POST /api/v1/files/complete`
- `POST /api/v1/files/upload-failed`

Alternative names that are NOT supported (rejected by frozen spec):
- `/files/presign-upload`
- `/files/confirm-upload`
- `/files/presign`
- `/files/confirm`
- `/upload/presign`
- `/upload/complete`
- `/media/upload`

**Current Implementation:**
Only frozen canonical names are implemented.

---

## API-GAP-P2-7-007 — Uploaded file to Note Item binding behavior

**Status:** OPEN

**Description:**
After `POST /api/v1/files/complete`, the backend receives confirmation that a file
was successfully uploaded to MinIO. The frozen spec does not define whether the
backend should automatically bind the file to a Note Item, or whether the client
must explicitly call `POST /api/v1/notebook-entries/{entry_id}/items` with the
`file_path` set to the `file_key`.

**Current Implementation:**
`POST /api/v1/files/complete` only confirms the upload — it does NOT automatically
create a Note Item. The client must create the Note Item manually.

**Owner Decision Needed:**
- Auto-create Note Item on complete?
- Client handles Note Item creation separately?

---

## API-GAP-P2-7-008 — MinIO bucket and object key naming rule

**Status:** OPEN

**Description:**
The object key format is inferred from the P0 API spec example:
`organizations/{org_id}/entries/{entry_id}/{file_name}`

No formal bucket naming standard is defined in frozen docs.

**Current Implementation:**
Object key format: `organizations/{org_id}/entries/{entry_id}/{file_name}`
Bucket: configured via `MINIO_BUCKET` environment variable (default: `ari-local`).

**Owner Decision Needed:**
- Confirm object key format?
- Confirm bucket naming conventions?
- Multi-bucket vs single-bucket strategy?

---

## API-GAP-P2-7-009 — upload_queue vs upload_jobs naming alignment

**Status:** RESOLVED (P2-7 Decision)

**Description:**
The P2-4 SQLAlchemy model class is named `UploadJob` (in `models/upload_job.py`)
but maps to the `upload_queue` table (`__tablename__ = "upload_queue"`).

**Current Implementation:**
Python internal naming uses `UploadJob` / `UploadQueueRepository`. The API path
is `/api/v1/upload-queue`. No `upload_jobs` table or `/api/v1/upload-jobs` endpoint
is created.

---

## API-GAP-P2-7-010 — Upload Queue endpoint naming conflict

**Status:** RESOLVED (P2-7 Decision)

**Description:**
Confirmed canonical API path: `/api/v1/upload-queue`

Not supported:
- `/api/v1/upload-jobs`

**Current Implementation:**
Only `/api/v1/upload-queue` is implemented.

---

## API-GAP-P2-7-011 — Sync batch payload naming mismatch

**Status:** OPEN (Owner Decision Required)

**Description:**
The P0 API spec uses:
```json
{
  "items": [{ "client_id": "...", "entity_type": "...", "action": "...", "payload": {} }]
}
```

The P1-2 Mobile spec uses:
```json
{
  "operations": [{ "client_id": "...", "operation_type": "create_notebook_entry", ... }]
}
```

**Current Implementation:**
Only the `items[] / action` format (P0 API spec) is supported.
Requests using `operations[]` will receive a 422 validation error.

**Owner Decision Needed:**
- Accept both formats via aliasing?
- Require mobile to use the P0 API format?
- Issue a breaking change revision?

---

## API-GAP-P2-7-012 — Sync batch transaction policy

**Status:** OPEN

**Description:**
When processing a batch with multiple items, it is unclear whether:
- All items should succeed or all fail together (atomic batch)
- Each item is processed independently (partial success allowed)

**Current Implementation:**
Items are processed independently. Per-item results are returned. If the
database commit fails for any reason, all items in the batch are marked
as failed. Individual item failures do not roll back other items' state
prior to the commit.

**Owner Decision Needed:**
- Confirm partial success policy?
- All-or-nothing batch atomicity?

---

## API-GAP-P2-7-013 — Follow-Up API and scheduling field boundary

**Status:** OPEN

**Description:**
The frozen domain model defines follow-up periods as 3/7/14 days.
It is unclear whether the backend should:
- Store a `due_date` (created_at + follow_up_day)
- Send push notifications automatically
- Allow scheduling system to trigger reminders

**Current Implementation:**
Only `follow_up_day` (integer: 3/7/14), `outcome`, `notes`, and `recorded_at`
are stored. No scheduling, push notification, or due date calculation is implemented.

**Owner Decision Needed:**
- Add `due_date` field?
- Integrate with push notification system?

---

## API-GAP-P2-7-014 — Notification creation/read boundary

**Status:** OPEN

**Description:**
The public API only exposes read and mark-read operations for notifications.
There is no public `POST /api/v1/notifications` endpoint for creating notifications.

**Current Implementation:**
Notifications are intended to be created internally by backend events.
No public creation endpoint exists. The `NotificationRepository.create` method
is not exposed via any API endpoint.

**Owner Decision Needed:**
- Should an admin/ari_staff endpoint for creating notifications exist?
- Which backend events should trigger notification creation?

---

## API-GAP-P2-7-015 — Media read URL endpoint for Web media viewer

**Status:** OPEN

**Description:**
The P1-3 Web App may require a presigned download URL to display media files
stored in MinIO. No `GET /api/v1/files/{file_key}/download-url` endpoint exists.

**Current Implementation:**
Not implemented. Only upload-related endpoints exist.

**Owner Decision Needed:**
- Add `GET /api/v1/files/download-url?file_key=...`?
- Expose MinIO directly (public bucket)?

---

## API-GAP-P2-7-016 — Checksum/dedup behavior

**Status:** OPEN

**Description:**
The `note_items.checksum` column exists in the frozen schema. It is unclear
whether the backend should:
- Calculate checksum server-side
- Accept client-provided checksum
- Use checksum for deduplication

**Current Implementation:**
`checksum` field exists in the NoteItem model but is not populated by the
current upload flow. No deduplication logic is implemented.

**Owner Decision Needed:**
- Who calculates the checksum?
- Is checksum used for dedup?

---

## API-GAP-P2-7-017 — client_id/device_id physical database support

**Status:** OPEN (Migration Required if Owner Approves)

**Description:**
The P0 API spec requires `client_id` for idempotency on notebook entries and
note items. The `upload_queue` table has a `client_id` column. However:
- `notebook_entries` table does NOT have a `client_id` column
- `note_items` table does NOT have a `client_id` column
- No `device_id` column exists on any entity table

**Current Implementation:**
`upload_queue.client_id` is used for upload queue idempotency.
For sync batch, `client_id` idempotency on notebook entries uses the
upload_queue as a lookup proxy. Full idempotency is NOT guaranteed
for direct `POST /api/v1/notebook-entries` calls.

**Owner Decision Needed:**
- Add `client_id` column to `notebook_entries` via Alembic migration?
- Add `client_id` column to `note_items`?
- Add `device_id` to relevant tables?

**Required Migration (if approved):**
```sql
ALTER TABLE notebook_entries ADD COLUMN client_id VARCHAR(255) NULL;
ALTER TABLE note_items ADD COLUMN client_id VARCHAR(255) NULL;
CREATE UNIQUE INDEX uq_notebook_entries_client_id ON notebook_entries(client_id) WHERE client_id IS NOT NULL;
```

---

## Summary of Decisions Required

| Gap ID | Priority | Decision Type |
|--------|----------|---------------|
| API-GAP-P2-7-001 | HIGH | Hierarchy inference policy |
| API-GAP-P2-7-002 | MEDIUM | Archive/status field |
| API-GAP-P2-7-003 | MEDIUM | Note Item delete |
| API-GAP-P2-7-004 | LOW | Resolved in P2-7 |
| API-GAP-P2-7-005 | HIGH | consultation_status field |
| API-GAP-P2-7-006 | LOW | Resolved in P2-7 |
| API-GAP-P2-7-007 | MEDIUM | File-to-NoteItem binding |
| API-GAP-P2-7-008 | LOW | MinIO naming |
| API-GAP-P2-7-009 | LOW | Resolved in P2-7 |
| API-GAP-P2-7-010 | LOW | Resolved in P2-7 |
| API-GAP-P2-7-011 | HIGH | Sync payload format |
| API-GAP-P2-7-012 | MEDIUM | Batch transaction policy |
| API-GAP-P2-7-013 | MEDIUM | Follow-up scheduling |
| API-GAP-P2-7-014 | LOW | Notification creation |
| API-GAP-P2-7-015 | MEDIUM | Media download URL |
| API-GAP-P2-7-016 | LOW | Checksum/dedup |
| API-GAP-P2-7-017 | HIGH | client_id in DB schema |

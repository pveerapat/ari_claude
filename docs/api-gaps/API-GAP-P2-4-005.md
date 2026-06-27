# API Gap / Revision Proposal

Gap ID:
API-GAP-P2-4-005

Title:
Exact enum values for notification_type and notification_status

Discovered In:
P2-4 Database and Alembic Migration Foundation

Related Frozen Document:
ARI V1 — P0 Domain Model Specification v1.0
ARI V1 — P0 API Specification v1.0

Current Frozen Behavior:
P0 Domain Model section 6 defines Notification with attributes:
  - notification_id, user_id, type, message, status, created_at

Notification examples include: Upload Reminder, AI Follow-Up Reminder, System Notification.

Missing / Ambiguous Detail:
The frozen P0 Database Schema and P0 API Specification do not provide an explicit
complete list of allowed values for:
  - notification_type (type column)
  - notification_status (status column)

Candidate notification_type values (inferred from domain, not confirmed):
  - upload_reminder
  - follow_up_reminder
  - system_notification
  - ari_reply (mentioned in P1-1)

Candidate notification_status values (inferred, not confirmed):
  - unread
  - read
  - dismissed

Impact:
- Cannot create a PostgreSQL native enum type without confirmed complete value set.
- Using VARCHAR fallback loses type safety and validation.
- Mobile and web apps must handle unknown notification types gracefully.

Proposed Handling:
Store notification.type and notification.status as VARCHAR(100) and VARCHAR(50)
in P2-4 initial migration. Convert to PostgreSQL native enums in a later additive
migration once the complete frozen value set is confirmed from P0 API spec.

Scope Risk:
Does this introduce new architecture? No
Does this introduce a new entity? No
Does this introduce a new database table? No
Does this introduce a new RBAC role? No

Recommendation:
Owner to confirm complete notification_type and notification_status enum values
before P2-7 (Notification/Upload/Sync Backend) implementation begins.

Status:
Draft — Stored as VARCHAR pending confirmation of complete enum values

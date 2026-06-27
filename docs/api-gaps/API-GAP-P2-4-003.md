# API Gap / Revision Proposal

Gap ID:
API-GAP-P2-4-003

Title:
upload_queue vs upload_jobs naming; upload_entity_type and upload_action enum values

Discovered In:
P2-4 Database and Alembic Migration Foundation

Related Frozen Document:
ARI V1 — P0 Domain Model Specification v1.0
ARI V1 — P1-1 Backend Implementation Specification v1.0

Current Frozen Behavior:
P0 Domain Model names the upload lifecycle entity as `upload_queue`.
P1-1 Backend Spec uses `upload_job.py` as the implementation filename and references
`upload_jobs` in some service/repository naming.

P2-4 spec section 12.3 states: "Use upload_queue as the database table name."

Missing / Ambiguous Detail:
1. Naming inconsistency between frozen table name (upload_queue) and P1-1 implementation
   filenames (upload_job.py, upload_jobs repository).

2. upload_entity_type and upload_action column values not fully specified:
   - upload_entity_type: "notebook_entry" confirmed; other values not confirmed in frozen spec.
   - upload_action: "create" mentioned; full set not confirmed in frozen spec.

Impact:
- Table name inconsistency could cause migration errors if implementation uses wrong name.
- Incomplete enum values for upload_entity_type and upload_action prevent creating
  PostgreSQL native enums; falling back to VARCHAR loses type safety.

Proposed Handling:
Part 1 (Resolved): Table name = upload_queue. Python class = UploadJob. File = upload_job.py.
  This matches the P2-4 spec decision.

Part 2: upload_entity_type and upload_action stored as VARCHAR (String) in P2-4.
  Full enum values to be confirmed and converted to PostgreSQL enums in a later migration
  once the complete set is confirmed from frozen P0 API spec.

Scope Risk:
Does this introduce new architecture? No
Does this introduce a new entity? No
Does this introduce a new database table? No
Does this introduce a new RBAC role? No

Recommendation:
Table naming is resolved. Enum values for upload_entity_type and upload_action require
Owner/API spec confirmation before converting from VARCHAR to PostgreSQL enum type.

Status:
Draft — Table naming resolved. Enum values pending confirmation.

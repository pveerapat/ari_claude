# API Gap / Revision Proposal

Gap ID:
API-GAP-P2-4-002

Title:
users.deleted_at dependency in phone partial unique index

Discovered In:
P2-4 Database and Alembic Migration Foundation

Related Frozen Document:
ARI V1 — P0 Database Schema Additive Revision v1.1

Current Frozen Behavior:
P0 Database Schema Additive Revision v1.1 defines the following partial unique index:

    CREATE UNIQUE INDEX uq_users_phone_active
    ON users(phone)
    WHERE phone IS NOT NULL
    AND deleted_at IS NULL;

Missing / Ambiguous Detail:
The column `deleted_at` is referenced in the partial unique index but is not listed as an
explicit column in the P0 Domain Model v1.0 User entity attributes:

    user_id, organization_id, name, email, phone, role, status, created_at

The P0 base schema does not define soft delete behavior. `deleted_at` is implied by the
v1.1 additive revision index but not formally documented as a required column.

Impact:
- The partial unique phone index cannot be created as specified without `deleted_at`.
- If soft delete is not intended, the index should use `WHERE phone IS NOT NULL` only.
- If soft delete IS intended, `deleted_at` must be formally added to the frozen user schema.

Proposed Handling:
Option A (Selected for P2-4): Add `deleted_at TIMESTAMPTZ NULL` to users table and
  use the full partial index as specified in v1.1. This follows the frozen v1.1 SQL exactly.
Option B: Create partial index as `WHERE phone IS NOT NULL` only (no deleted_at dependency).
  Requires formal revision to the v1.1 index definition.

Scope Risk:
Does this introduce new architecture? No
Does this introduce a new entity? No
Does this introduce a new database table? No
Does this introduce a new RBAC role? No

Recommendation:
Proceed with Option A. The v1.1 additive revision SQL explicitly uses `deleted_at IS NULL`,
implying soft delete is intended for users. Owner should formally confirm soft delete policy
for users table before P2-5 auth implementation.

Status:
Draft — Implemented as Option A (deleted_at added) pending Owner confirmation of soft delete policy

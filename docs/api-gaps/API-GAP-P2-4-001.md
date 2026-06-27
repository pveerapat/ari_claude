# API Gap / Revision Proposal

Gap ID:
API-GAP-P2-4-001

Title:
Physical primary key column naming — id vs *_id

Discovered In:
P2-4 Database and Alembic Migration Foundation

Related Frozen Document:
ARI V1 — P0 Database Schema Specification v1.0
ARI V1 — P0 Domain Model Specification v1.0

Current Frozen Behavior:
P0 Domain Model uses domain-specific ID names (organization_id, user_id, farm_id, etc.)
as entity identifiers in the domain description. The frozen database schema specification
does not explicitly state whether the physical database column should be named `id` or the
domain-specific `*_id` name.

Missing / Ambiguous Detail:
The frozen database schema specification does not clearly decide between:
- `id` as physical primary key column (SQLAlchemy/FastAPI convention)
- `*_id` as physical primary key column (matching domain model naming)

Impact:
Naming choice affects SQLAlchemy model definitions, Alembic migration, API response serialization,
and foreign key reference syntax. Inconsistency between Python model and API schema causes
unnecessary mapping layers.

Proposed Handling:
Option A (Selected for P2-4): Use `id` as physical primary key column for all tables.
  - Expose domain-specific names (organization_id, farm_id, etc.) through API response schemas in later P2 phases.
  - Standard SQLAlchemy/FastAPI convention.
Option B: Use `*_id` as physical column name matching domain model.
  - More explicit but unconventional for ORM mapping.

Scope Risk:
Does this introduce new architecture? No
Does this introduce a new entity? No
Does this introduce a new database table? No
Does this introduce a new RBAC role? No

Recommendation:
Proceed with Option A (`id` as physical PK). This is the P2-4 implementation choice.
If Owner prefers `*_id` as physical column name, a migration rename will be required before P2-5.

Status:
Draft — Implemented as Option A pending Owner confirmation

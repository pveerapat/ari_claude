# API Gap / Revision Proposal

Gap ID:
API-GAP-P2-4-004

Title:
roles/user_roles database table inclusion confirmation

Discovered In:
P2-4 Database and Alembic Migration Foundation

Related Frozen Document:
ARI V1 — P0 Database Schema Specification v1.0
ARI V1 — P1-1 Backend Implementation Specification v1.0

Current Frozen Behavior:
P0 Domain Model lists `role` as a user attribute (a scalar value per user).
P1-1 Backend Spec section 9.2 states: "Role-related tables may be mapped only if already
included in the frozen database schema."
P1-1 section 12.1 defines frozen RBAC roles: farmer, ari_staff, farm_coordinator,
agronomist, reviewer, admin, root.

Missing / Ambiguous Detail:
The frozen P0 Database Schema Specification v1.0 does not explicitly define separate
`roles` and `user_roles` tables. The domain model implies `role` is a column on users,
not a join table. However, P1-1 conditionally references role-related tables.

Impact:
- Without confirmation, creating roles/user_roles tables would violate P2-4 forbidden scope.
- The current implementation stores `role` as a PostgreSQL enum column on the users table,
  which supports the domain model but does not support multiple roles per user.
- If the design requires multiple roles per user, a separate user_roles join table is needed.

Proposed Handling:
Option A (Selected for P2-4): Store role as a single enum column on users table.
  Matches domain model (role = user attribute). Simple RBAC for P0.
Option B: Create roles table with 7 frozen role rows + user_roles join table.
  Required if multiple roles per user is needed.

Scope Risk:
Does this introduce new architecture? Option B would add 2 new tables.
Does this introduce a new entity? Option B would add Role entity.
Does this introduce a new database table? Option B: roles + user_roles
Does this introduce a new RBAC role? No — frozen roles only.

Recommendation:
Proceed with Option A for P2-4. If multi-role assignment is required for P2-5 auth,
create a Revision Proposal to add roles/user_roles tables through a new Alembic migration.

Status:
Draft — Implemented as Option A (role as column on users) pending Owner confirmation

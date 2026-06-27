# API Gap / Revision Proposal

Gap ID:
API-GAP-P2-4-006

Title:
Exact enum values for analysis_status beyond 'not_started'

Discovered In:
P2-4 Database and Alembic Migration Foundation

Related Frozen Document:
ARI V1 — P0 Domain Model Specification v1.0
ARI V1 — P0 API Specification v1.0

Current Frozen Behavior:
P0 Domain Model lists `analysis_status` as a notebook_entry attribute.
P2-4 spec section 13 confirms `not_started` as a frozen value.
P2-4 spec states: "other values require frozen confirmation."

Missing / Ambiguous Detail:
The complete set of analysis_status values is not explicitly defined in the frozen
P0 Database Schema or P0 API Specification. Expected workflow:

  not_started → (analysis triggered) → in_progress → completed / failed

But these intermediate and terminal states are not confirmed frozen values.

Candidate values (inferred from P0 domain workflow, not confirmed):
  - not_started (confirmed)
  - pending_analysis
  - in_progress
  - completed
  - failed
  - cancelled

Impact:
- Cannot create a PostgreSQL native enum without the complete frozen value set.
- Using VARCHAR fallback loses type safety but allows forward-compatible values.
- Mobile and web apps must handle unknown analysis_status values gracefully.

Proposed Handling:
Store analysis_status as VARCHAR(50) with server_default='not_started' in P2-4.
Convert to PostgreSQL native enum in a later additive migration once the complete
frozen value set is confirmed from P0 API spec and P2-7 notebook implementation.

Scope Risk:
Does this introduce new architecture? No
Does this introduce a new entity? No
Does this introduce a new database table? No
Does this introduce a new RBAC role? No

Recommendation:
Owner to confirm complete analysis_status enum values before P2-7
(Notebook/Upload/Sync Backend) implementation begins.

Status:
Draft — Stored as VARCHAR pending confirmation of complete enum values

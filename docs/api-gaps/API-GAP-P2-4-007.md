# API Gap / Revision Proposal

Gap ID:
API-GAP-P2-4-007

Title:
consultation_status — column vs entry_type value clarification

Discovered In:
P2-4 Database and Alembic Migration Foundation

Related Frozen Document:
ARI V1 — P0 Domain Model Specification v1.0
ARI V1 — P1-1 Backend Implementation Specification v1.0

Current Frozen Behavior:
P1-1 Backend Spec section 14.7 explicitly states:
  "Consultation is implemented as Notebook Entry Type = consultation"
  "Consultation is not a separate domain entity."

Consultation-specific attributes are handled inside notebook_entry:
  - entry_type = consultation
  - external_ai (ai_provider)
  - ai_usefulness_status
  - learned_summary

Missing / Ambiguous Detail:
P2-4 spec section 13 lists 'consultation_status' as a potential enum group with
known values: pending, completed (others require frozen confirmation).

It is unclear whether:
  1. consultation_status is a separate column on notebook_entries (in addition to analysis_status)
  2. consultation_status refers to analysis_status values specific to consultation flow
  3. consultation_status does not exist as a column — the workflow state is inferred from
     analysis_status and entry_type = consultation

Impact:
- Adding a consultation_status column without confirmation violates P2-4 forbidden scope
  ("do not implement consultation entity").
- Not adding it may require a later additive migration.

Proposed Handling:
Option A (Selected for P2-4): Do NOT add a separate consultation_status column.
  The consultation lifecycle is tracked through analysis_status on notebook_entries.
  entry_type = consultation identifies the entry as a consultation.
  This is consistent with P1-1: "Consultation = Notebook Entry Type."
Option B: Add consultation_status column to notebook_entries if Owner confirms it is
  distinct from analysis_status.

Scope Risk:
Does this introduce new architecture? No
Does this introduce a new entity? No (consultation remains entry_type value)
Does this introduce a new database table? No
Does this introduce a new RBAC role? No

Recommendation:
Proceed with Option A. No consultation_status column in P2-4. If the consultation lifecycle
requires a separate status field, this should be handled as an additive migration in P2-7
with Owner confirmation.

Status:
Draft — No consultation_status column added. Consultation tracked via entry_type + analysis_status.

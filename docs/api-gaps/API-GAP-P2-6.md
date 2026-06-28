# API Gap / Revision Proposals — P2-6 Farm Structure Backend

Document: ARI V1 — P2-6 Farm Structure Backend v1.0
Date Recorded: 2026-06-28
Status: Open — Awaiting Owner Decision

---

## API-GAP-P2-6-001 — Farm Archive Status Unclear or Unsupported

**Trigger:**
`PATCH /api/v1/farms/{farm_id}/archive` was requested but the frozen schema does not define a frozen list of valid `status` values or a transition model for `archived`.

**Finding:**
The `farms.status` column is `VARCHAR(50)` (plain string). No frozen enum defines allowed values or transitions. The frozen P0 API Spec mentions `status = "archived"` but without a confirmed enum, the transition is unclear.

**Action Taken:**
- Archive endpoint NOT implemented.
- Hard delete is NOT implemented (Evidence First principle preserved).
- `status` field is NOT exposed as an updateable field in `PATCH /farms/{farm_id}`.
- `status = "active"` is set automatically on farm creation.

**Owner Decision Required:**
- Should `status` be an enum with values `active`, `inactive`, `archived`?
- Should `PATCH /api/v1/farms/{farm_id}/archive` be implemented?
- Should `status` be updateable through normal `PATCH /api/v1/farms/{farm_id}`?

---

## API-GAP-P2-6-002 — Membership Approval Endpoint Shape

**Trigger:**
Approval of `pending_farm_approval` users requires an endpoint. No dedicated approval endpoint exists in P2-6 scope.

**Finding:**
P1-2 / P0 API Additive Revision v1.1 describes using `PATCH /api/v1/users/{user_id}` with `{"membership_status": "active"}` as the approval mechanism. However, the Users API is not part of P2-6 scope and has not been explicitly implemented in P2-5.

**Action Taken:**
- No approval endpoint created in P2-6.
- `membership_status` blocking is enforced (`require_active_membership` guard).
- Pending users cannot access protected farm structure.

**Owner Decision Required:**
- Should `PATCH /api/v1/users/{user_id}` implement `membership_status` update in P2-7 or a separate sprint?
- Who is the allowed approver? (admin / root / ari_staff only per frozen spec)

---

## API-GAP-P2-6-003 — farms.location Field Status

**Finding:**
`farms.location JSONB` **EXISTS** in the implemented P2-4 schema.

**Action Taken:**
- `location` field is implemented in `FarmCreate`, `FarmUpdate`, `FarmRead`.
- Location validation is enforced: `gps_latitude` must be between -90 and 90; `gps_longitude` must be between -180 and 180.
- This gap is **RESOLVED** for P2-6.

**Status: RESOLVED**

---

## API-GAP-P2-6-004 — Simulator Farm Filter Missing

**Trigger:**
`?is_simulator=true` filter was requested by frozen spec as optional.

**Finding:**
No `is_simulator` column exists in the `farms` table in the implemented P2-4 schema.

**Action Taken:**
- Simulator filter NOT implemented.
- Normal farm list returns all farms in organization scope without simulator filtering.

**Owner Decision Required:**
- Should `is_simulator BOOLEAN` be added to the `farms` table in a new migration?
- Is simulator farm filtering required for P2-7 or a later phase?

---

## API-GAP-P2-6-005 — Delete vs Archive Behavior

**Trigger:**
Evidence First principle prohibits hard delete. Archive behavior is unclear (see API-GAP-P2-6-001).

**Action Taken:**
- No DELETE endpoints implemented for Farm, Zone, or Tree.
- No `deleted_at` column added to farms/zones/trees.
- Archive is not implemented until status enum and transitions are confirmed.

**Owner Decision Required:**
- Same as API-GAP-P2-6-001.

---

## API-GAP-P2-6-006 — Farm/Zone/Tree Uniqueness Constraints

**Trigger:**
Duplicate prevention behavior is required but no uniqueness constraints exist in frozen schema for:
- `farm_name` within an organization
- `zone_name` within a farm
- `tree_code` within a zone

**Finding:**
No unique constraints exist in the P2-4 migration for these fields.

**Action Taken:**
- No silent database constraints added.
- Duplicate names/codes are currently allowed at the database level.
- Service layer does not enforce duplicate prevention (would require read-before-write with no DB guarantee).

**Owner Decision Required:**
- Should unique constraints be added via a new migration?
  - `UNIQUE(organization_id, name)` on farms?
  - `UNIQUE(farm_id, name)` on zones?
  - `UNIQUE(zone_id, tree_code)` on trees?

---

## API-GAP-P2-6-007 — farm_code Generation / Storage Unclear

**Trigger:**
Farm display codes (e.g., `ARI-FARM-A123`) are referenced in P0 API Additive Revision v1.1 for member join flow but `farm_code` is not present in the implemented P2-4 `farms` table schema.

**Finding:**
The `Farm` SQLAlchemy model has no `farm_code` column. The P0 API spec references `farm_code` as system-generated and display-only.

**Action Taken:**
- `farm_code` NOT added to schema silently.
- No migration created.
- `farm_id` (UUID) remains the canonical Farm identifier.
- `farm_code` is NOT accepted in `FarmCreate` or `FarmUpdate`.
- `farm_code` is NOT returned in `FarmRead`.

**Owner Decision Required:**
- Should `farm_code VARCHAR` be added to the `farms` table via a new Revision Proposal migration?
- What is the generation logic? (e.g., `ARI-FARM-{random alphanumeric}`)
- Should farm_code be used as the join reference for `owner_family`/`farm_staff` registration?

---

## Summary Table

| Gap ID           | Title                                    | Status    | Blocker? |
|------------------|------------------------------------------|-----------|----------|
| API-GAP-P2-6-001 | Farm archive status unclear              | Open      | No       |
| API-GAP-P2-6-002 | Membership approval endpoint shape       | Open      | No       |
| API-GAP-P2-6-003 | farms.location field                     | Resolved  | —        |
| API-GAP-P2-6-004 | Simulator farm filter missing            | Open      | No       |
| API-GAP-P2-6-005 | Delete vs archive behavior               | Open      | No       |
| API-GAP-P2-6-006 | Farm/Zone/Tree uniqueness constraints    | Open      | No       |
| API-GAP-P2-6-007 | farm_code generation / storage unclear   | Open      | No       |

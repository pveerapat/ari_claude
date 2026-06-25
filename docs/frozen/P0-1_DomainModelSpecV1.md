# ARI Target Document Reconstruction Export

---------------------------------------------------------
Target Document Title:
ARI V1 — P0 Domain Model Specification v1.0
---------------------------------------------------------

Context:

This document is derived from the approved discussion after ARI documents:

#44 Farm AIOS
#45 Software Architecture & Monorepo Specification Rev2.0
#46 MVP Software Build Plan
#46A Mobile App UX Flow & Screen Specification
#46B Web App UX Flow & Screen Specification
#47 AI Agent Development Workflow Framework

Goal:

Reconstruct only the final agreed P0 Domain Model.

Rules:

1. Export only the final agreed Domain Model.
2. Do not redesign ARI.
3. Do not introduce new architecture.
4. Preserve all confirmed decisions:
   - Farm/Zone/Tree Nullable
   - entry_context exists in Domain Model
   - Consultation = Notebook Entry Type
   - Notebook Entry = Note Session
   - Note Item supports photo/video/voice/text/file/link
   - sequence_order support
   - Save ≠ Upload ≠ Analyze
5. Separate:
   - P0 Required
   - Optional Extension
   - Future Enhancement
   - Assumptions Requiring Owner Confirmation
6. Output Markdown only.



   ----------------------------------------
    After Owner Reviewed : Freeze 
    Reviewed by          : owner 
    Reviewed date        : 2026-06-15
    ----------------------------------------


รับทราบครับ

ARI V1 — P0 Domain Model Specification v1.0

Status: FROZEN

Freeze Confirmation

เอกสารต่อไปนี้ถือเป็น Source of Truth สำหรับการพัฒนา ARI P0 ในส่วน Domain Model:

ARI V1 — P0 Domain Model Specification v1.0
Status: FROZEN
Frozen Decisions
D1 — Identity Assignment
created_by_user_id = required
organization_id = required

farm_id = nullable
zone_id = nullable
tree_id = nullable
D2 — Entry Context
entry_context exists in Domain Model

แต่

ไม่บังคับให้ผู้ใช้เลือกใน Mobile P0
D3 — Consultation Model
Consultation = Notebook Entry Type

ไม่สร้าง Consultation Entity แยกใน P0

entry_type:
- note
- consultation
D4 — Notebook Structure
Notebook Entry = Note Session

รองรับ

Note Item
- photo
- video
- voice
- text
- file
- link
D5 — Timeline Support
sequence_order required

รองรับการบันทึกแบบ Timeline

photo
→ voice
→ photo
→ video
→ text
D6 — Link Support

รองรับ

YouTube
Facebook
TikTok
Website
Article
PDF URL

ผ่าน

item_type = link

ไม่เพิ่มเมนูใหม่ใน Mobile P0

D7 — Offline First
Save Local
≠ Upload
≠ Analyze

เป็นหลักการบังคับของ P0

D8 — Ownership Model
Organization owns data

Users create data
Freeze Scope

เอกสารนี้ใช้เป็นฐานสำหรับ:

Phase 2
P0 Database Schema Specification

และเป็น Domain Source of Truth สำหรับ:

Mobile App (#46A)
Web App (#46B)
FastAPI Backend
PostgreSQL Schema
RBAC Design
Offline Sync Design
Change Control

หลังจาก Freeze แล้ว

แนวคิดใหม่หรือการเปลี่ยนแปลงใด ๆ ต้องถูกระบุเป็น:

Revision Proposal

หรือ

Future Enhancement

ห้ามแก้ไขเนื้อหา Frozen โดยตรง

ARI V1 — P0 Domain Model Specification v1.0
FROZEN ✅

พร้อมเข้าสู่:

Phase 2 — P0 Database Schema Specification


*********************
ีupdate 2026-06-19
*********************

# ARI V1 — P0 Domain Model Additive Revision v1.1

## Project

ARI — Agricultural Intelligence Platform

## Document Type

P0 Domain Model Additive Revision

## Version

v1.1

## Status

Ready for Owner Review

## Base Document

ARI V1 — P0 Domain Model Specification v1.0
Status: FROZEN

## Related Source Documents

* #44 Farm AI Operating System (Farm AIOS)
* #45 Software Architecture & Monorepo Specification Rev2.0
* #46 MVP Software Build Plan
* #46A Mobile App UX Flow & Screen Specification
* #46B Web App UX Flow & Screen Specification
* #47 AI Agent Development Workflow Framework
* P1-2 Mobile Onboarding Specification

---

# 1. Revision Purpose

This revision note records additive domain model changes required by the Owner-approved P1-2 Mobile Onboarding Specification.

This revision does not replace P0 Domain Model Specification v1.0.

This revision extends the existing User identity model to support:

* Mobile self-registration
* Phone-based login identity
* Owner onboarding
* Farm family onboarding
* Farm staff onboarding
* Farm membership approval flow

This revision is additive only.

No existing P0 domain entity is removed or replaced.

---

# 2. Revision Scope

## 2.1 Affected Domain Entity

```text
User
```

## 2.2 Affected Relationships

```text
User ↔ Organization

User ↔ Farm
```

## 2.3 Unaffected Domain Entities

The following P0 domain entities are not changed by this revision:

```text
Organization

Farm

Zone

Tree

Notebook Entry

Note Item

Follow Up

Notification

Upload Queue
```

## 2.4 Explicit Scope Boundary

This revision only updates the User identity model.

This revision does not introduce new farm operation, notebook, evidence, AI, knowledge, commerce, or robot domain concepts.

---

# 3. User Domain Additions

Add the following attributes to the existing User domain model.

---

## 3.1 Phone

```text
phone
```

### Purpose

```text
Primary Login Identity
```

### Domain Meaning

Phone represents the mobile phone number used by a user for mobile registration and login.

### Domain Rules

For existing users migrated from P0 v1.0:

```text
phone may be null
```

For new users registered through P1-2 mobile self-registration:

```text
phone is required
```

### Notes

Phone is a User identity attribute.

Phone does not replace RBAC.

Phone does not create a new user type.

---

## 3.2 Farmer Status

```text
farmer_status
```

### Purpose

```text
Onboarding Classification
```

### Allowed Values

```text
owner

owner_family

farm_staff
```

### Domain Meaning

farmer_status classifies the user's onboarding path.

It describes how the user enters the ARI mobile onboarding flow.

### Important Rule

```text
farmer_status ≠ RBAC role
```

farmer_status is not a permission role.

farmer_status does not replace RBAC.

farmer_status does not create new application roles.

---

## 3.3 Membership Status

```text
membership_status
```

### Purpose

```text
Farm Membership Lifecycle
```

### Allowed Values

```text
pending_farm_approval

active

rejected

suspended

revoked
```

### Domain Meaning

membership_status represents whether a user is allowed to participate in a farm context.

This is especially important for:

```text
owner_family

farm_staff
```

because they join an existing Farm by Farm ID and must wait for approval.

---

## 3.4 Account Status

```text
account_status
```

### Purpose

```text
Account Lifecycle
```

### Allowed Values

```text
active

active_pending_verification

pending_review

suspended

rejected

revoked
```

### Domain Meaning

account_status represents the user account lifecycle independent of farm membership.

A user account may exist even when farm membership is still pending.

### Distinction

```text
account_status = account-level state

membership_status = farm-membership state
```

These two statuses must not be collapsed into one concept.

---

## 3.5 Primary Farm

```text
primary_farm_id
```

### Purpose

```text
Default Farm Context
```

### Applicable To

```text
owner_family

farm_staff
```

### Domain Meaning

primary_farm_id represents the default farm context for a user after approval.

It supports the mobile Farm Selector and active farm context.

### Nullable Rule

```text
primary_farm_id may be null
```

Reasons it may be null:

* User has not yet been approved
* User has not selected a default farm
* User is an owner with multiple farms and no default farm selected
* User account exists before farm membership approval is complete

---

# 4. Updated User Model

The User model is extended additively as follows.

```text
User

user_id

organization_id

role

email

phone

name

password_hash

farmer_status

membership_status

account_status

primary_farm_id
```

## Notes

The existing `email` field remains part of the User model.

This revision does not remove email-based identity.

This revision adds phone-based identity support for mobile onboarding.

---

# 5. Updated User Relationships

## 5.1 User ↔ Organization

Existing relationship remains:

```text
User belongs to Organization
```

This revision clarifies how organization assignment works during onboarding.

---

## 5.2 User ↔ Farm

Existing relationship remains:

```text
User may have access to Farm through organization scope, RBAC, and farm assignment
```

This revision adds:

```text
primary_farm_id
```

as a default farm context reference.

This does not create a Farm Membership Entity.

---

# 6. Domain Rules

---

## 6.1 Owner Onboarding Rule

When:

```text
farmer_status = owner
```

Then:

```text
membership_status = active
```

Owner may create:

```text
Farm
```

within own Organization.

### Organization Assignment

For an owner registration flow:

```text
System creates or assigns an Organization for the owner.
```

The owner becomes associated with that Organization.

Farm creation occurs under that Organization.

### Account Status

Initial account_status may be:

```text
active_pending_verification
```

or

```text
active
```

depending on verification policy defined in the implementation layer.

---

## 6.2 Owner Family Onboarding Rule

When:

```text
farmer_status = owner_family
```

Then:

```text
Farm ID required
```

and initial:

```text
membership_status = pending_farm_approval
```

until approved.

### Organization Assignment

For owner_family onboarding:

```text
organization_id is resolved from the Farm ID.
```

owner_family does not create a new Organization.

owner_family does not create a new Farm.

### Access Rule

Before approval:

```text
Farm access is limited or blocked according to RBAC and membership_status.
```

After approval:

```text
membership_status = active
```

and:

```text
primary_farm_id may be set to the approved Farm.
```

---

## 6.3 Farm Staff Onboarding Rule

When:

```text
farmer_status = farm_staff
```

Then:

```text
Farm ID required
```

and initial:

```text
membership_status = pending_farm_approval
```

until approved.

### Organization Assignment

For farm_staff onboarding:

```text
organization_id is resolved from the Farm ID.
```

farm_staff does not create a new Organization.

farm_staff does not create a new Farm.

### Access Rule

Before approval:

```text
Farm access is limited or blocked according to RBAC and membership_status.
```

After approval:

```text
membership_status = active
```

and:

```text
primary_farm_id may be set to the approved Farm.
```

---

# 7. RBAC Non-Change

RBAC remains unchanged.

Existing RBAC roles remain:

```text
farmer

ari_staff

farm_coordinator

agronomist

reviewer

admin

root
```

No new RBAC roles are introduced by this revision.

The following are not RBAC roles:

```text
owner

owner_family

farm_staff
```

They are onboarding classifications only.

---

# 8. Explicit Non-Changes

This revision does not introduce:

```text
Owner Registry

Member Registry

Farmer Registry

Farm Membership Entity

Permission Entity

New RBAC Role

New Mobile App

New Web App

New Backend Service

New Database Architecture
```

---

# 9. Impact on Existing P0 Domain Model

## 9.1 Organization

No change.

Organization remains the ownership boundary of data.

## 9.2 Farm

No change.

Farm remains the primary physical farm identity.

## 9.3 Zone

No change.

## 9.4 Tree

No change.

## 9.5 Notebook Entry

No change.

## 9.6 Note Item

No change.

## 9.7 Follow Up

No change.

## 9.8 Notification

No change.

## 9.9 Upload Queue

No change.

---

# 10. Implementation Interpretation

This revision supports mobile onboarding while preserving the frozen P0 architecture.

The system may implement registration flows such as:

```text
Owner registers by phone
↓
Owner account created
↓
Organization created or assigned
↓
Owner creates Farm
```

and:

```text
Owner Family / Farm Staff registers by phone
↓
User enters Farm ID
↓
System resolves Organization from Farm
↓
membership_status = pending_farm_approval
↓
Owner / Admin / authorized role approves
↓
membership_status = active
↓
primary_farm_id may be assigned
```

---

# 11. Database Impact Note

This Domain Model revision requires a companion additive database schema revision.

Expected affected table:

```text
users
```

Expected additive fields:

```text
phone

farmer_status

membership_status

account_status

primary_farm_id
```

Expected relationship:

```text
users.primary_farm_id → farms.farm_id
```

No destructive migration is allowed.

No existing table should be removed or replaced.

---

# 12. P0 Required

This additive revision is P0 Required only for supporting P1-2 mobile onboarding.

Required additions:

```text
phone

farmer_status

membership_status

account_status

primary_farm_id
```

Required domain rules:

```text
owner may create Farm under own Organization

owner_family joins by Farm ID

farm_staff joins by Farm ID

organization_id for owner_family/farm_staff is resolved from Farm

farmer_status is not RBAC

membership_status controls farm membership lifecycle

account_status controls account lifecycle
```

---

# 13. Optional Extension

None for this revision.

---

# 14. Future Enhancement

The following are not part of this revision:

```text
Dedicated Farm Membership Entity

Advanced Invitation System

QR-based Join Approval

Multi-Farm Membership Management

ABAC

External Identity Provider

KYC / Identity Verification

Consent Management System

Expert Network Registration

Cooperative Member Registry
```

These may be considered in future phases only if required.

---

# 15. Assumptions Requiring Owner Confirmation

## A1. Phone Login

Phone is intended to become the primary login identity for new mobile self-registration users.

Existing users may continue to have email identity.

## A2. Organization Creation for Owner

Owner registration creates or assigns an Organization for the owner.

## A3. Farm ID Requirement

owner_family and farm_staff must provide Farm ID during onboarding.

## A4. Approval Authority

Approval authority for pending farm membership will be handled by RBAC in later RBAC/API specifications.

This revision does not define approval permissions.

## A5. No Farm Membership Entity

Farm membership lifecycle is represented directly on User for this revision.

No Farm Membership Entity is introduced.

---

# 16. Revision Status

```text
Additive Domain Revision

No Breaking Change

Ready For Owner Review
```

---

# 17. Change Control

After approval, this document becomes:

```text
ARI V1 — P0 Domain Model Additive Revision v1.1
```

and should be treated as an additive extension to:

```text
ARI V1 — P0 Domain Model Specification v1.0
```

This document must not be used to replace the frozen P0 Domain Model v1.0.

Any future changes must be recorded as a new additive revision or formal revision proposal.


***********************
update 2026-06-19
***********************

ARI V1 — P0 Domain Model Additive Revision v1.1
Status
FROZEN
Base Document
ARI V1 — P0 Domain Model Specification v1.0
Status: FROZEN
Freeze Scope

เอกสารนี้เป็น Additive Revision ของ P0 Domain Model v1.0 โดยแก้เฉพาะส่วน:

User Domain Model

เพื่อรองรับ P1-2 Mobile Onboarding

Frozen Additions

เพิ่ม field ต่อไปนี้ใน User Domain:

phone

farmer_status

membership_status

account_status

primary_farm_id
Frozen Domain Rules
1. Phone
phone = Primary Login Identity

ใช้รองรับ mobile self-registration และ phone-based login

2. Farmer Status
farmer_status:
- owner
- owner_family
- farm_staff

กฎสำคัญ:

farmer_status ≠ RBAC role
3. Membership Status
membership_status:
- pending_farm_approval
- active
- rejected
- suspended
- revoked

ใช้ควบคุม lifecycle ของ farm membership

4. Account Status
account_status:
- active
- active_pending_verification
- pending_review
- suspended
- rejected
- revoked

ใช้ควบคุม lifecycle ของ account

5. Primary Farm
primary_farm_id

ใช้เป็น default farm context สำหรับ:

owner_family
farm_staff

และอาจเป็น null ได้

Frozen Onboarding Rules
Owner
farmer_status = owner

แล้ว:

membership_status = active

Owner สามารถสร้าง:

Farm

ภายใต้ Organization ของตนเอง

Owner Family
farmer_status = owner_family

ต้องมี:

Farm ID

และเริ่มต้นด้วย:

membership_status = pending_farm_approval

ระบบต้อง resolve:

organization_id

จาก Farm ID

Farm Staff
farmer_status = farm_staff

ต้องมี:

Farm ID

และเริ่มต้นด้วย:

membership_status = pending_farm_approval

ระบบต้อง resolve:

organization_id

จาก Farm ID

Frozen Non-Changes

เอกสารนี้ ไม่เพิ่ม:

Owner Registry

Member Registry

Farmer Registry

Farm Membership Entity

Permission Entity

New RBAC Role

New Mobile App

New Web App

New Backend Service

New Database Architecture
Correct Current Status
ARI V1 — P0 Domain Model Additive Revision v1.1
Status: FROZEN
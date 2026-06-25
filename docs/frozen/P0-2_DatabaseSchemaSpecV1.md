# ARI V1 — P0 Domain Model Specification v1.0

## Project

ARI — Agricultural Intelligence Platform

## Document Type

P0 Domain Model Specification

## Status

Ready for Freeze

## Source Documents

* #44 Farm AI Operating System (Farm AIOS)
* #45 Software Architecture & Monorepo Specification Rev2.0
* #46 MVP Software Build Plan
* #46A Mobile App UX Flow & Screen Specification
* #46B Web App UX Flow & Screen Specification
* #47 AI Agent Development Workflow Framework

---

# 1. Purpose

This document defines the final agreed domain model for ARI P0.

ARI P0 is a Digital Farm Notebook.

The purpose of P0 is to capture:

* Observations
* Events
* Experiences
* Stories
* Questions
* Lessons Learned
* Evidence
* AI Consultation Outcomes

before transforming them into knowledge and intelligence in later phases.

---

# 2. Domain Principles

## Evidence First

All important records should be traceable to evidence.

Evidence may include:

* Photo
* Video
* Voice Recording
* Text
* File
* External Link

---

## Human-in-the-Loop

Humans create records.

Humans validate records.

Humans remain accountable.

AI assists but does not replace human responsibility.

---

## Offline First

Save and Upload are separate operations.

```text
Save Local
≠
Upload
≠
Analyze
```

Records must be creatable without internet connectivity.

---

## Progressive Identity

Identity architecture must support future expansion without redesign.

Supported identity hierarchy:

```text
Organization
    └── Farm
            └── Zone
                    └── Tree
```

---

# 3. Core Entities

---

## 3.1 Organization

Represents the ownership boundary of data.

Examples:

* Individual Farmer
* Family Farm
* Cooperative
* Company
* ARI Internal Organization

### Responsibilities

* Own farms
* Own users
* Own operational data

### Core Attributes

```text
organization_id
name
type
status
created_at
```

---

## 3.2 User

Represents a human using ARI.

### Responsibilities

* Create records
* Upload evidence
* Review information
* Manage assigned farms

### Core Attributes

```text
user_id
organization_id
name
email
phone
role
status
created_at
```

---

## 3.3 Farm

Represents a physical farm.

### Core Attributes

```text
farm_id
organization_id
farm_name
location
description
status
created_at
```

---

## 3.4 Zone

Represents a logical subdivision within a farm.

Examples:

* Block A
* North Section
* Trial Area

### Core Attributes

```text
zone_id
farm_id
zone_name
description
created_at
```

---

## 3.5 Tree

Represents an optional tree-level identity.

### Core Attributes

```text
tree_id
zone_id
tree_code
status
created_at
```

Tree registration is optional in P0.

---

# 4. Notebook Domain

Notebook is the core domain of ARI P0.

---

## 4.1 Notebook Entry

Notebook Entry represents a Note Session.

A Notebook Entry may contain multiple Note Items arranged in timeline order.

### Entry Types

```text
note
consultation
```

### Entry Context

```text
general_note
registered_farm
external_observation
interview
```

### Core Attributes

```text
entry_id

organization_id

created_by_user_id

farm_id (nullable)

zone_id (nullable)

tree_id (nullable)

entry_type

entry_context

title (nullable)

summary (nullable)

suggested_category (nullable)

analysis_status

created_at

updated_at
```

### Notes

Farm, Zone and Tree references are optional.

This supports:

* External observations
* Interviews
* Expert consultations
* Events outside registered farms

---

## 4.2 Note Item

Represents an individual content item within a Notebook Entry.

A Notebook Entry may contain many Note Items.

### Supported Types

```text
photo
video
voice
text
file
link
```

### Core Attributes

```text
item_id

entry_id

item_type

sequence_order

content_text (nullable)

file_path (nullable)

url (nullable)

platform (nullable)

created_at

upload_status
```

### Timeline Support

Sequence order preserves capture order.

Example:

```text
Photo
→ Voice
→ Photo
→ Video
→ Text
```

---

## 4.3 Link Support

External URLs are supported through Note Items.

Examples:

* YouTube
* Facebook
* TikTok
* Website
* Article
* PDF URL

Links are stored as:

```text
item_type = link
```

No dedicated mobile menu is required.

Users may paste URLs into text entries.

The system may classify them as link items.

---

# 5. Ask AI Domain

Ask AI follows the workflow defined in #46A.

External AI providers include:

* ChatGPT
* Gemini
* Claude
* Other

ARI does not provide an internal AI assistant in P0.

---

## 5.1 Consultation Entry

Consultation is implemented as a Notebook Entry type.

```text
entry_type = consultation
```

### Additional Consultation Attributes

```text
ai_provider

ai_usefulness_status

learned_summary
```

### AI Usefulness Status

```text
useful
not_useful
later
```

---

## 5.2 Follow-Up

Follow-Up records track outcomes after AI consultation.

### Supported Follow-Up Periods

```text
3 Days
7 Days
14 Days
```

### Outcome Types

```text
improved
same
worse
unknown
```

### Core Attributes

```text
follow_up_id

entry_id

follow_up_day

outcome

notes

recorded_at
```

---

# 6. Notification Domain

Represents reminders and system notifications.

### Examples

* Upload Reminder
* AI Follow-Up Reminder
* System Notification

### Core Attributes

```text
notification_id

user_id

type

message

status

created_at
```

---

# 7. Upload Queue Domain

Supports Offline First operation.

### Purpose

Manage synchronization between device and backend.

### Core Attributes

```text
queue_id

entry_id

status

retry_count

created_at

uploaded_at
```

### Queue Status

```text
pending

uploading

failed

completed
```

---

# 8. Ownership Model

ARI ownership principle:

```text
Organization owns data.

Users create data.
```

### Ownership Hierarchy

```text
Organization
    ├── Users
    └── Farms
            └── Zones
                    └── Trees
```

### Operational Hierarchy

```text
Notebook Entry
    └── Note Items
```

### Consultation Hierarchy

```text
Notebook Entry
    └── Follow-Ups
```

---

# 9. Domain Relationship Summary

```text
Organization
 ├── Users
 └── Farms
        └── Zones
                └── Trees

Notebook Entry
 ├── Note Items
 └── Follow-Ups

User
 ├── Creates Notebook Entries
 └── Receives Notifications

Upload Queue
 └── References Notebook Entries
```

---

# P0 Required

## Identity

* Organization
* User
* Farm
* Zone
* Tree (Optional Registration)

## Notebook

* Notebook Entry
* Note Item
* Timeline Sequence Support

## Ask AI

* Consultation Entry
* Learned Summary
* Follow-Up

## Offline Operation

* Save Local
* Upload Queue
* Upload Retry

## Metadata

* Title
* Summary
* Suggested Category
* Analysis Status

## Notifications

* Upload Reminder
* Follow-Up Reminder
* System Notification

---

# Optional Extension

## External Link Capture

Support storing:

* YouTube Links
* Facebook Links
* TikTok Links
* Website Links
* Article Links
* PDF URLs

## Mobile Share Integration

Future optional support:

```text
Share → ARI
```

from external applications.

---

# Future Enhancement

Not part of P0.

## Intelligence Layer

* Knowledge Graph
* Evidence Graph
* Vector Database
* RAG
* Knowledge Extraction

## AI Layer

* Internal AI Assistant
* Agent Orchestration
* Autonomous Workflows

## Advanced Features

* Digital Twin
* Robot Integration
* Advanced GIS
* Forecasting
* Advanced Analytics

## Commerce Layer

* Marketplace
* Commerce
* Carbon Credits
* ESG Intelligence

---

# Assumptions Requiring Owner Confirmation

## A1

Tree registration remains optional during P0 deployment.

## A2

entry_context exists in the domain model but is not required as a mobile user input.

The system may assign default values and allow later review.

## A3

AI-generated metadata in P0 is limited to:

```text
title
summary
suggested_category
```

and does not constitute an internal AI assistant.


----------------------------------------
    After Owner Reviewed : Freeze 
    Reviewed by          : owner 
    Reviewed date        : 2026-06-14
    ----------------------------------------


    รับทราบครับ

สถานะเอกสาร:

ARI V1 — P0 Database Schema Specification v1.0

Status: FROZEN
Phase: P0 Digital Farm Notebook
Freeze State: Approved

เอกสารนี้ถือเป็น Source of Truth สำหรับ Phase 2 Database Layer โดยยึดตาม:

#44 Farm AIOS
#45 Software Architecture & Monorepo Specification Rev2.0
#46 MVP Software Build Plan
#46A Mobile App UX Flow & Screen Specification
#46B Web App UX Flow & Screen Specification
#47 AI Agent Development Workflow Framework
ARI V1 — P0 Domain Model Specification v1.0

Frozen Scope:

organizations
users
farms
zones
trees
notebook_entries
note_items
follow_ups
notifications
upload_queue

Frozen Principles:

One Platform
One Backend
One Database
One Domain Model
One RBAC System

Notebook Entry = Note Session

Save Local ≠ Upload ≠ Analyze

farm_id / zone_id / tree_id nullable

Simulator Farm supported

Offline First

หลังจากนี้ หากมีการเปลี่ยนแปลงให้จัดเป็น:

Revision Proposal
Optional Extension
Future Enhancement

ไม่แก้ไขเนื้อหาในเอกสาร Frozen โดยตรง

ขั้นตอนถัดไปที่แนะนำ:

ARI V1 — P0 API Specification v1.0

เพื่อกำหนด REST API Contracts ระหว่าง:

Flutter Mobile
Next.js Web
FastAPI Backend
PostgreSQL
MinIO

และเชื่อมต่อกับ P0 Domain Model + P0 Database Schema ที่ Frozen แล้ว.


*****************************
ีupdate 2026-06-19
*****************************

# ARI V1 — P0 Database Schema Additive Revision v1.1

## Revision Purpose

This revision records additive schema changes required by the approved P1-2 Mobile Onboarding Specification.

This revision does not replace P0 Database Schema v1.0.

All changes are additive.

No destructive migration is allowed.

---

# Affected Tables

```text
users
farms (optional location enhancement)
```

---

# Users Table Additions

## phone

```sql
phone VARCHAR(30) NULL
```

Rules:

```text
Required for newly registered users.

Legacy users may remain NULL.
```

Unique Index:

```sql
CREATE UNIQUE INDEX uq_users_phone_active
ON users(phone)
WHERE phone IS NOT NULL
AND deleted_at IS NULL;
```

---

## farmer_status

```sql
farmer_status_enum
```

Values:

```text
owner
owner_family
farm_staff
```

Column:

```sql
farmer_status farmer_status_enum NULL
```

---

## membership_status

```sql
membership_status_enum
```

Values:

```text
pending_farm_approval
active
rejected
suspended
revoked
```

Column:

```sql
membership_status membership_status_enum NULL
```

Index:

```sql
CREATE INDEX idx_users_membership_status
ON users(membership_status);
```

---

## account_status

```sql
account_status_enum
```

Values:

```text
active
active_pending_verification
pending_review
suspended
rejected
revoked
```

Column:

```sql
account_status account_status_enum NULL
```

Index:

```sql
CREATE INDEX idx_users_account_status
ON users(account_status);
```

---

## primary_farm_id

```sql
primary_farm_id UUID NULL
```

Foreign Key:

```sql
REFERENCES farms(id)
```

---

## registered_at

```sql
registered_at TIMESTAMPTZ NULL
```

Purpose:

```text
Stores onboarding registration timestamp.
```

---

# Farm Location Enhancement

## location

```sql
location JSONB NULL
```

Recommended structure:

```json
{
  "province": "",
  "district": "",
  "subdistrict": "",
  "address": "",
  "gps_latitude": 0,
  "gps_longitude": 0,
  "source": "device_gps"
}
```

Notes:

```text
location_text remains unchanged.

No existing column is removed.
```

---

# Migration Rules

```text
Additive Only

No Table Removal

No Column Removal

No Entity Renaming

No Foreign Key Removal

No Breaking Change
```

---

# Explicit Non-Changes

Do not create:

```text
owner_registry
member_registry
farmer_registry
farm_memberships
permission_tables
consultations
qr_registry
```

---

# Revision Status

```text
Additive Database Revision

No Breaking Change

Ready For Review
```


*****************************
ีupdate 2026-06-19/2
*****************************
# ARI V1 — P0 Database Schema Additive Revision v1.1

## 1. Revision Purpose

This revision records additive database schema changes required by:

```text
ARI V1 — P0 Domain Model Additive Revision v1.1
P1-2 Mobile Onboarding Specification
```

This revision does not replace:

```text
ARI V1 — P0 Database Schema Specification v1.0
```

All changes are additive.

No destructive migration is allowed.

---

# 2. Revision Scope

## 2.1 Affected Table

```text
users
```

## 2.2 Optional Implementation Enhancement

```text
farms.location
```

This is optional and does not change the Farm domain model.

---

# 3. Users Table Additive Changes

## 3.1 phone

If `phone` already exists in P0 Database Schema v1.0, do not recreate the column.

If missing, add:

```sql
ALTER TABLE users
ADD COLUMN phone VARCHAR(30) NULL;
```

### Rules

```text
Existing users may have phone = NULL.

New users registered through P1-2 mobile onboarding must provide phone.

This requirement is enforced by API / application validation, not by NOT NULL database constraint.
```

### Unique Index

```sql
CREATE UNIQUE INDEX IF NOT EXISTS uq_users_phone_active
ON users(phone)
WHERE phone IS NOT NULL
AND deleted_at IS NULL;
```

---

## 3.2 farmer_status

### Purpose

Onboarding classification.

### Allowed Values

```text
owner
owner_family
farm_staff
```

### PostgreSQL Enum

```sql
CREATE TYPE farmer_status_enum AS ENUM (
  'owner',
  'owner_family',
  'farm_staff'
);
```

### Column

```sql
ALTER TABLE users
ADD COLUMN farmer_status farmer_status_enum NULL;
```

### Rule

```text
farmer_status is not RBAC role.
```

---

## 3.3 membership_status

### Purpose

Farm membership lifecycle.

### Allowed Values

```text
pending_farm_approval
active
rejected
suspended
revoked
```

### PostgreSQL Enum

```sql
CREATE TYPE membership_status_enum AS ENUM (
  'pending_farm_approval',
  'active',
  'rejected',
  'suspended',
  'revoked'
);
```

### Column

```sql
ALTER TABLE users
ADD COLUMN membership_status membership_status_enum NULL;
```

### Index

```sql
CREATE INDEX IF NOT EXISTS idx_users_membership_status
ON users(membership_status);
```

---

## 3.4 account_status

### Purpose

Account lifecycle.

### Allowed Values

```text
active
active_pending_verification
pending_review
suspended
rejected
revoked
```

### PostgreSQL Enum

```sql
CREATE TYPE account_status_enum AS ENUM (
  'active',
  'active_pending_verification',
  'pending_review',
  'suspended',
  'rejected',
  'revoked'
);
```

### Column

```sql
ALTER TABLE users
ADD COLUMN account_status account_status_enum NULL;
```

### Index

```sql
CREATE INDEX IF NOT EXISTS idx_users_account_status
ON users(account_status);
```

---

## 3.5 primary_farm_id

### Purpose

Default farm context for mobile onboarding and Farm Selector.

### Column

```sql
ALTER TABLE users
ADD COLUMN primary_farm_id UUID NULL;
```

### Foreign Key

```sql
ALTER TABLE users
ADD CONSTRAINT fk_users_primary_farm_id
FOREIGN KEY (primary_farm_id)
REFERENCES farms(id);
```

### Index

```sql
CREATE INDEX IF NOT EXISTS idx_users_primary_farm_id
ON users(primary_farm_id);
```

### Rule

```text
primary_farm_id may be NULL.
```

Reasons:

```text
User has not yet been approved.
User has not selected a default farm.
Owner may own multiple farms.
User account exists before farm membership approval is complete.
```

---

# 4. Optional Farm Location Enhancement

## 4.1 location

This is optional.

It supports P1-2 mobile onboarding and farm registration UX.

It does not change the Farm domain model.

```sql
ALTER TABLE farms
ADD COLUMN location JSONB NULL;
```

### Recommended Structure

```json
{
  "province": "",
  "district": "",
  "subdistrict": "",
  "address": "",
  "gps_latitude": 0,
  "gps_longitude": 0,
  "source": "device_gps"
}
```

### Notes

```text
location_text remains unchanged.

No existing column is removed.

location JSONB is an implementation enhancement only.
```

---

# 5. Domain-to-Database Mapping

| Domain v1.1 Concept         | Database v1.1 Field              |
| --------------------------- | -------------------------------- |
| phone                       | users.phone                      |
| farmer_status               | users.farmer_status              |
| membership_status           | users.membership_status          |
| account_status              | users.account_status             |
| primary_farm_id             | users.primary_farm_id            |
| User ↔ Farm default context | users.primary_farm_id → farms.id |

---

# 6. Required Application Validation

## 6.1 Owner Registration

When:

```text
farmer_status = owner
```

Then application should set:

```text
membership_status = active
account_status = active_pending_verification or active
```

Owner may create Farm under own Organization.

---

## 6.2 Owner Family Registration

When:

```text
farmer_status = owner_family
```

Then:

```text
Farm ID is required.
organization_id is resolved from Farm.
membership_status = pending_farm_approval.
primary_farm_id may be set after approval.
```

---

## 6.3 Farm Staff Registration

When:

```text
farmer_status = farm_staff
```

Then:

```text
Farm ID is required.
organization_id is resolved from Farm.
membership_status = pending_farm_approval.
primary_farm_id may be set after approval.
```

---

# 7. Migration Rules

```text
Additive Only

No Table Removal

No Column Removal

No Entity Renaming

No Foreign Key Removal

No Destructive Migration

No Breaking Change
```

---

# 8. Explicit Non-Changes

Do not create:

```text
owner_registry

member_registry

farmer_registry

farm_memberships

permission_tables

consultations

qr_registry
```

Do not introduce:

```text
New RBAC Role

New Mobile App

New Web App

New Backend Service

New Database Architecture
```

---

# 9. Compatibility Notes

This revision remains compatible with:

```text
One Platform

One Backend

One Database Architecture

One Mobile App

One Web App

One Domain Model

One RBAC System
```

This revision does not modify:

```text
Notebook Entry

Note Item

Follow Up

Notification

Upload Queue

Farm

Zone

Tree
```

---

# 10. Revision Status

```text
Additive Database Revision

No Breaking Change

Ready For Review
```


***************
Freeze
***************

ARI V1 — P0 Database Schema Additive Revision v1.1

Status: FROZEN
Freeze Decision: Approved by Owner
Revision Type: Additive Database Revision
Breaking Change: No

Frozen scope:

users.phone
users.farmer_status
users.membership_status
users.account_status
users.primary_farm_id

optional:
farms.location JSONB

Frozen rules:

Additive only
No destructive migration
No new entity
No farm_memberships
No owner_registry
No member_registry
No farmer_registry
No permission_tables
No consultations table
No qr_registry

เอกสารนี้ถือเป็น additive extension ต่อจาก:

ARI V1 — P0 Database Schema Specification v1.0

และสอดคล้องกับ:

ARI V1 — P0 Domain Model Additive Revision v1.1
P1-2 Mobile Onboarding Specification
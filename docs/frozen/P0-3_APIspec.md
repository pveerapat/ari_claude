ARI V1 — P0 API Specification v1.0
(Target Document Reconstruction Export Style)

Markdown Complete Version
Ready For Freeze Review

1. Document Metadata
2. Purpose
3. Scope
4. Source of Truth
5. Architecture Constraints
6. API Principles
7. Versioning Strategy
8. Authentication Strategy
9. Authorization Strategy
10. Standard Conventions
11. Identity APIs
    - Organizations
    - Users
12. Farm Structure APIs
    - Farms
    - Zones
    - Trees
13. Notebook APIs
    - Notebook Entries
    - Note Items
14. Consultation APIs
15. Follow-up APIs
16. Notification APIs
17. File Upload APIs
18. Upload Queue APIs
19. Offline Sync APIs
20. Search APIs
21. Simulator Rules
22. QR/ID Rules
23. Validation Rules
24. Authorization Matrix
25. Error Handling
26. P0 Required Scope
27. Optional Extension
28. Future Enhancement
29. Assumptions Requiring Owner Confirmation
30. Owner Confirmed Resolution (A1-A6)
31. Final Consistency Assessment
32. Ready For Freeze Review

ซึ่งผมสามารถสร้าง Markdown เต็มทั้งฉบับ ได้ แต่ต้องส่งเป็นหลายตอน (Part 1, Part 2, Part 3, Part 4) เพื่อไม่ให้ถูกตัด

แนะนำให้ทำแบบนี้:

Part 1

Metadata → Standard Conventions

Part 2

Identity + Farm Structure APIs

Part 3

Notebook + Consultation + Follow-up + Notification APIs

Part 4

Upload + Sync + Search + A1-A6 Resolution + Freeze Section

แล้วคุณนำไปรวมเป็น

ARI-V1-P0-API-Specification-v1.0.md

******************************************
Part I. ARI V1 — P0 API Specification v1.0
******************************************
Project

ARI — Agricultural Intelligence Platform

Document Type

P0 API Specification

Status

READY FOR OWNER REVIEW

Phase

Phase 3 — API Specification

Document Metadata
Field	Value
Project	ARI — Agricultural Intelligence Platform
Document Title	ARI V1 — P0 API Specification v1.0
Phase	P0 Digital Farm Notebook
Status	Ready For Review
Architecture Baseline	#44, #45
MVP Baseline	#46, #46A, #46B
Development Baseline	#47
Domain Baseline	P0 Domain Model v1.0
Database Baseline	P0 Database Schema v1.0
1. Purpose

This document defines the complete API contract for ARI P0.

The purpose of ARI P0 is:

Observation
↓
Evidence
↓
Accumulation

before advanced intelligence capabilities are introduced.

The API must support:

Mobile App
Web Platform
Offline First Workflow
Digital Farm Notebook
Evidence Collection
Consultation Tracking
Follow-Up Tracking
Synchronization

without introducing architecture outside approved scope.

2. Source of Truth

This specification follows:

Architecture
#44 Farm AI Operating System
#45 Software Architecture & Monorepo Specification Rev2.0
MVP
#46 MVP Software Build Plan
#46A Mobile UX Flow & Screen Specification
#46B Web UX Flow & Screen Specification
Development
#47 AI Agent Development Workflow Framework
P0 Core
P0 Domain Model Specification
P0 Database Schema Specification
3. Architecture Constraints

The API must preserve:

One Platform
One Backend
One Database Architecture
One Mobile App
One Web App
One Domain Model
One RBAC System

The API must not introduce:

Separate Applications
Separate Backends
Separate Databases
Separate Domain Models
4. P0 Scope

ARI P0 is:

Digital Farm Notebook

Purpose:

Capture:

Observations
Events
Experiences
Stories
Questions
Lessons Learned
Evidence
AI Consultation Outcomes
5. Out Of Scope

Not part of P0:

ERP
Marketplace
Commerce Platform
Knowledge Graph
Vector Database
RAG
Multi-Agent System
Robot Platform
Autonomous AI Platform
6. Frozen Entities

Only the following entities exist.

Identity
organizations
users
Farm Structure
farms
zones
trees
Notebook
notebook_entries
note_items
Consultation
follow_ups
Notifications
notifications
Sync
upload_queue

No additional entities may be introduced.

7. API Versioning Strategy

Base path:

/api/v1

Examples:

/api/v1/auth/login

/api/v1/farms

/api/v1/notebook-entries

Rules:

Non-Breaking Change

Allowed under:

/api/v1

Examples:

Additional optional field
Additional endpoint
Additional filter
Breaking Change

Requires:

/api/v2

Examples:

Schema change
Enum change
Required field change
Authentication change
8. Authentication Strategy
Method

JWT Authentication

Compatible with:

Flutter
Next.js
FastAPI
Tokens
Access Token

Used for API requests.

Refresh Token

Used to obtain new access token.

Authorization Header
Authorization: Bearer <access_token>
JWT Claims
{
  "sub": "user_id",
  "organization_id": "uuid",
  "role": "farmer"
}
9. Authentication Endpoints
Login
Purpose

Authenticate user.

Method
POST
Path
/api/v1/auth/login
Request
{
  "email": "user@example.com",
  "password": "password"
}
Response
{
  "access_token": "jwt",
  "refresh_token": "jwt",
  "token_type": "bearer",
  "expires_in": 3600
}
Validation
email required
password required
Errors
400
401
422
500
Refresh Token
Method
POST
Path
/api/v1/auth/refresh
Request
{
  "refresh_token": "jwt"
}
Response
{
  "access_token": "jwt",
  "expires_in": 3600
}
Logout
Method
POST
Path
/api/v1/auth/logout
Response
{
  "success": true
}
Current User
Method
GET
Path
/api/v1/auth/me
Response
{
  "user_id": "uuid",
  "organization_id": "uuid",
  "role": "farmer"
}
10. Authorization Strategy
Roles
farmer
ari_staff
farm_coordinator
agronomist
reviewer
admin
root
Ownership Principle
Organization owns data

Users create data
Access Scope

Access must be controlled by:

Role
Organization
Farm
Root

May access:

All Organizations
All Farms
All Records
Admin

May access:

Assigned Organization
Assigned Farms
Farmer

May access:

Own Organization

Accessible Farms

Own Records
11. Standard API Conventions
Pagination
Request
?page=1&page_size=20
Default
page=1
page_size=20
Maximum
page_size=100
Response
{
  "data": [],
  "pagination": {
    "page": 1,
    "page_size": 20,
    "total_records": 100,
    "total_pages": 5
  }
}
Filtering

Pattern:

?field=value

Examples:

?farm_id=uuid

?entry_type=consultation

?status=active
Sorting

Pattern:

?sort_by=created_at
&sort_order=desc

Allowed:

asc
desc
Date Range

Pattern:

?date_from=2026-01-01
&date_to=2026-01-31
Search

Pattern:

?q=root_rot

P0 Search is:

Keyword Search

Only.

No:

Vector Search
Knowledge Graph
RAG
12. Standard Response Envelope
Success
{
  "data": {}
}
List
{
  "data": [],
  "pagination": {}
}
Error
{
  "error": {
    "code": "validation_error",
    "message": "Invalid request"
  }
}
13. Standard Error Codes
HTTP	Meaning
400	Bad Request
401	Unauthorized
403	Forbidden
404	Not Found
409	Conflict
422	Validation Error
500	Internal Server Error
14. Offline First Strategy

Core Rule:

Save Local
≠ Upload
≠ Analyze
Requirements

Must support:

Offline Capture
Retry Upload
Resume Upload
Background Sync
Conflict Handling
WiFi Only Upload
Manual Upload
Client ID

All offline-created records should support:

client_id

Purpose:

Idempotency
Duplicate Prevention
Sync Reliability
15. File Upload Strategy

Storage:

MinIO
Upload Flow
Create Upload URL
↓
Upload To MinIO
↓
Confirm Upload
↓
Create Note Item
Supported Types
photo
video
voice
file
Upload Method

Use:

Presigned URL
16. Validation Rules
UUID

All IDs must be valid UUID.

Hierarchy Validation
Organization
    ↓
Farm
    ↓
Zone
    ↓
Tree

Rules:

Farm belongs to Organization

Zone belongs to Farm

Tree belongs to Zone
Nullable Context

Allowed:

farm_id = null
zone_id = null
tree_id = null

Because:

External Observation
Interview
Consultation
General Note

must be supported.

Enum Validation

Must validate against frozen enums:

user_role

entry_type

entry_context

note_item_type

upload_status

upload_entity_type

upload_action

notification_type

notification_status

follow_up_outcome

analysis_status

consultation_status

**************************************************
Part 1 Complete
**************************************************


******************************************
ARI V1 — P0 API Specification v1.0
Part 2 — Identity & Farm Structure APIs

Part 2
- Organizations APIs
- Users APIs
- Farms APIs
- Zones APIs
- Trees APIs
******************************************


17. Identity APIs

Identity APIs manage:

organizations
users

These APIs establish:

Ownership Boundary
User Access Boundary
RBAC Boundary
17.1 Organization APIs
List Organizations
Purpose

Return organizations visible to current user.

Method
GET
Path
/api/v1/organizations
Query Parameters
page
page_size

status

sort_by
sort_order
Response
{
  "data": [
    {
      "organization_id": "uuid",
      "name": "Durian Cooperative",
      "type": "cooperative",
      "status": "active",
      "created_at": "datetime"
    }
  ],
  "pagination": {}
}
Validation Rules
status must be valid
Authorization Rules
Role	Access
root	all
admin	assigned organization
ari_staff	assigned organization
others	limited
Errors
401
403
422
500
Get Organization
Purpose

Return organization details.

Method
GET
Path
/api/v1/organizations/{organization_id}
Response
{
  "organization_id": "uuid",
  "name": "Durian Cooperative",
  "type": "cooperative",
  "status": "active",
  "created_at": "datetime"
}
Authorization

User must have access to organization.

Errors
401
403
404
500
Create Organization
Purpose

Create organization.

Method
POST
Path
/api/v1/organizations
Request Body
{
  "name": "Durian Cooperative",
  "type": "cooperative",
  "status": "active"
}
Response
{
  "organization_id": "uuid"
}
Validation Rules
name required
type required
status valid
Authorization
root
admin
Errors
400
403
409
422
500
Update Organization
Method
PATCH
Path
/api/v1/organizations/{organization_id}
Request Body
{
  "name": "Updated Name",
  "status": "active"
}
Validation
status valid
Authorization
root
admin
Errors
400
403
404
409
422
500
17.2 User APIs
List Users
Purpose

Return users visible to current user.

Method
GET
Path
/api/v1/users
Query Parameters
organization_id

role

status

page
page_size

sort_by
sort_order
Response
{
  "data": [
    {
      "user_id": "uuid",
      "organization_id": "uuid",
      "name": "John",
      "email": "john@example.com",
      "phone": null,
      "role": "farmer",
      "status": "active",
      "created_at": "datetime"
    }
  ],
  "pagination": {}
}
Validation
role valid
status valid
Authorization
admin
root
ari_staff

within scope.

Errors
401
403
422
500
Get User
Method
GET
Path
/api/v1/users/{user_id}
Authorization

User may access:

Own Profile

Admin may access:

Organization Users
Errors
401
403
404
500
Create User
Method
POST
Path
/api/v1/users
Request Body
{
  "organization_id": "uuid",
  "name": "John",
  "email": "john@example.com",
  "phone": "0812345678",
  "role": "farmer",
  "status": "active"
}
Response
{
  "user_id": "uuid"
}
Validation Rules
organization_id required

name required

email required

email unique

role valid

status valid
Authorization
admin
root
Errors
400
403
409
422
500
Update User
Method
PATCH
Path
/api/v1/users/{user_id}
Request Body
{
  "name": "Updated Name",
  "phone": "0811111111",
  "role": "agronomist",
  "status": "active"
}
Validation
role valid
status valid
Authorization
admin
root

or limited self-update.

Errors
400
403
404
409
422
500
18. Farm Structure APIs

Farm Structure supports:

Organization
    ↓
Farm
    ↓
Zone
    ↓
Tree
18.1 Farm APIs
List Farms
Purpose

Return farms visible to current user.

Method
GET
Path
/api/v1/farms
Query Parameters
organization_id

status

page
page_size

sort_by
sort_order
Response
{
  "data": [
    {
      "farm_id": "uuid",
      "organization_id": "uuid",
      "farm_name": "Durian Farm A",
      "location": null,
      "description": null,
      "status": "active",
      "created_at": "datetime"
    }
  ],
  "pagination": {}
}
Validation
organization_id valid
status valid
Authorization

Farm must belong to accessible organization.

Errors
401
403
422
500
Get Farm
Method
GET
Path
/api/v1/farms/{farm_id}
Authorization

User must have access to farm.

Errors
401
403
404
500
Create Farm
Method
POST
Path
/api/v1/farms
Request Body
{
  "organization_id": "uuid",
  "farm_name": "Durian Farm A",
  "location": null,
  "description": null,
  "status": "active"
}
Validation
organization_id required

farm_name required
Authorization
admin
root
ari_staff
farm_coordinator

if permitted.

Errors
400
403
404
409
422
500
Update Farm
Method
PATCH
Path
/api/v1/farms/{farm_id}
Request Body
{
  "farm_name": "Updated Farm",
  "description": "Description"
}
Authorization

Must have farm write permission.

Errors
400
403
404
422
500
Archive Farm
Method
PATCH
Path
/api/v1/farms/{farm_id}/archive
Request Body
{
  "status": "archived"
}
Notes
Hard Delete Not Recommended

Evidence First principle applies.

18.2 Zone APIs
List Zones
Method
GET
Path
/api/v1/zones
Query Parameters
farm_id

page
page_size

sort_by
sort_order
Response
{
  "data": [
    {
      "zone_id": "uuid",
      "farm_id": "uuid",
      "zone_name": "North Zone",
      "description": null,
      "created_at": "datetime"
    }
  ]
}
Validation
farm_id valid
Authorization

User must access parent farm.

Get Zone
Method
GET
Path
/api/v1/zones/{zone_id}
Authorization

Must access parent farm.

Create Zone
Method
POST
Path
/api/v1/zones
Request Body
{
  "farm_id": "uuid",
  "zone_name": "North Zone",
  "description": null
}
Validation
farm_id required

zone_name required
Authorization
admin
root
farm_coordinator

or permitted staff.

Update Zone
Method
PATCH
Path
/api/v1/zones/{zone_id}
Request Body
{
  "zone_name": "Updated Zone"
}
18.3 Tree APIs

Tree registration remains:

Optional

for P0.

List Trees
Method
GET
Path
/api/v1/trees
Query Parameters
zone_id

status

page
page_size
Response
{
  "data": [
    {
      "tree_id": "uuid",
      "zone_id": "uuid",
      "tree_code": "T-001",
      "status": "active",
      "created_at": "datetime"
    }
  ]
}
Validation
zone_id valid
Authorization

Must access parent zone/farm.

Get Tree
Method
GET
Path
/api/v1/trees/{tree_id}
Authorization

Must access parent farm.

Create Tree
Method
POST
Path
/api/v1/trees
Request Body
{
  "zone_id": "uuid",
  "tree_code": "T-001",
  "status": "active"
}
Validation
zone_id required

tree_code required
Authorization
admin
root
farm_coordinator

or permitted staff.

Update Tree
Method
PATCH
Path
/api/v1/trees/{tree_id}
Request Body
{
  "tree_code": "T-002",
  "status": "active"
}
Validation
status valid
Authorization

Must have write permission.

19. Farm Hierarchy Validation Rules
Rule 1
Farm
must belong to
Organization
Rule 2
Zone
must belong to
Farm
Rule 3
Tree
must belong to
Zone
Rule 4

When notebook entry contains:

tree_id

system must validate:

Tree
↓
Zone
↓
Farm

consistency.

Rule 5

When notebook entry contains:

zone_id

system must validate:

Zone
↓
Farm

consistency.

Part 2 Complete
*********************************

******************************************
ARI V1 — P0 API Specification v1.0
Part 3 — Notebook, Consultation, Follow-Up, Notification APIs
*******************************************
Notebook APIs
Note Item APIs
Consultation APIs
Follow-Up APIs
Notification APIs
****

20. Notebook APIs

Notebook is the core of ARI P0.

P0 revolves around:

Capture
Store
Search
Review
Follow-Up
Frozen Domain Decision
Notebook Entry
=
Note Session

A notebook entry contains:

1..N Note Items
Entity
notebook_entries
20.1 Create Notebook Entry
Purpose

Create a new notebook session.

Supports:

Observation
Story
Event
Experience
Lesson Learned
Consultation
Method
POST
Path
/api/v1/notebook-entries
Request Body
{
  "client_id": "uuid",
  "organization_id": "uuid",

  "farm_id": null,
  "zone_id": null,
  "tree_id": null,

  "entry_type": "note",

  "entry_context": "general_note",

  "title": null,
  "summary": null,

  "analysis_status": "not_started",

  "consultation_status": null,

  "ai_provider": null,

  "learned_summary": null
}
Response
{
  "entry_id": "uuid",

  "organization_id": "uuid",

  "created_by_user_id": "uuid",

  "farm_id": null,
  "zone_id": null,
  "tree_id": null,

  "entry_type": "note",

  "entry_context": "general_note",

  "created_at": "datetime",

  "updated_at": "datetime"
}
Validation Rules
organization_id required

created_by_user_id from JWT

entry_type required

entry_context required

client_id recommended

farm_id nullable

zone_id nullable

tree_id nullable
Authorization
farmer
ari_staff
farm_coordinator
agronomist
reviewer
admin
root

within scope.

Errors
400
401
403
404
409
422
500
20.2 List Notebook Entries
Purpose

Return notebook entries visible to user.

Method
GET
Path
/api/v1/notebook-entries
Query Parameters
organization_id

farm_id
zone_id
tree_id

entry_type

entry_context

analysis_status

consultation_status

created_by_user_id

date_from
date_to

q

page
page_size

sort_by
sort_order
Response
{
  "data": [
    {
      "entry_id": "uuid",

      "entry_type": "note",

      "title": "Observation",

      "summary": "Leaf yellowing",

      "created_at": "datetime"
    }
  ],

  "pagination": {}
}
Authorization

User sees only:

Accessible Organization

Accessible Farms

Own Records

according to role.

20.3 Get Notebook Entry
Method
GET
Path
/api/v1/notebook-entries/{entry_id}
Response
{
  "entry_id": "uuid",

  "organization_id": "uuid",

  "created_by_user_id": "uuid",

  "farm_id": null,
  "zone_id": null,
  "tree_id": null,

  "entry_type": "note",

  "entry_context": "general_note",

  "title": "Observation",

  "summary": "Summary",

  "analysis_status": "not_started",

  "consultation_status": null,

  "items": [],

  "follow_ups": [],

  "created_at": "datetime"
}
Authorization

Must have access to parent organization/farm.

20.4 Update Notebook Entry
Method
PATCH
Path
/api/v1/notebook-entries/{entry_id}
Request Body
{
  "title": "Updated Title",

  "summary": "Updated Summary",

  "farm_id": "uuid",

  "zone_id": null,

  "tree_id": null
}
Validation Rules
Hierarchy Validation Required

Farm
Zone
Tree
must remain consistent
Authorization

Creator or permitted staff.

20.5 Archive Notebook Entry
Method
PATCH
Path
/api/v1/notebook-entries/{entry_id}/archive
Notes
Evidence First Principle

Hard Delete Not Recommended
20.6 Search Notebook Entries
Method
GET
Path
/api/v1/notebook-entries/search
Query Parameters
q

farm_id
zone_id
tree_id

entry_type

date_from
date_to

page
page_size
Search Scope
title

summary

text note items

Only.

Explicitly Excluded
Vector Search

Semantic Search

Knowledge Graph Search

RAG Search
21. Note Item APIs

Entity:

note_items
Frozen Decision

Supported item types:

photo
video
voice
text
file
link
21.1 Create Note Item
Purpose

Add item into notebook timeline.

Method
POST
Path
/api/v1/notebook-entries/{entry_id}/items
Request Body
{
  "item_type": "photo",

  "sequence_order": 1,

  "content_text": null,

  "file_path": "object-key",

  "url": null
}
Response
{
  "item_id": "uuid",

  "entry_id": "uuid",

  "item_type": "photo",

  "sequence_order": 1
}
Validation Rules
Text
content_text required
Link
url required
Media
photo
video
voice
file

require file_path
Timeline
sequence_order required
21.2 List Note Items
Method
GET
Path
/api/v1/notebook-entries/{entry_id}/items
Response
{
  "data": [
    {
      "item_id": "uuid",

      "item_type": "photo",

      "sequence_order": 1
    }
  ]
}
21.3 Get Note Item
Method
GET
Path
/api/v1/note-items/{item_id}
21.4 Update Note Item
Method
PATCH
Path
/api/v1/note-items/{item_id}
Request Body
{
  "sequence_order": 2,

  "content_text": "Updated"
}
21.5 Delete Note Item
Method
DELETE
Path
/api/v1/note-items/{item_id}
Notes

Physical media deletion should be handled carefully.

Evidence-first policy applies.

22. Consultation APIs
Frozen Domain Decision

Consultation is not a separate entity.

Consultation is:

notebook_entries

entry_type
=
consultation
22.1 Create Consultation
Method
POST
Path
/api/v1/notebook-entries
Request Body
{
  "entry_type": "consultation",

  "ai_provider": "chatgpt",

  "consultation_status": "pending",

  "learned_summary": null
}
Supported Providers
chatgpt

gemini

claude

other
Notes

P0 uses:

External AI Apps

Only.

No internal AI agent.

22.2 List Consultations
Method
GET
Path
/api/v1/notebook-entries
Filter
entry_type=consultation
22.3 Update Consultation Outcome
Method
PATCH
Path
/api/v1/notebook-entries/{entry_id}/consultation-outcome
Request Body
{
  "consultation_status": "completed",

  "learned_summary": "User learned..."
}
Validation
entry_type must be consultation
23. Follow-Up APIs

Entity:

follow_ups
Frozen Decision

Follow-Up schedule:

3 Days

7 Days

14 Days
Outcomes
improved

same

worse

unknown
23.1 Create Follow-Up
Method
POST
Path
/api/v1/follow-ups
Request Body
{
  "entry_id": "uuid",

  "follow_up_day": 7
}
Validation

Allowed values:

3
7
14

Only.

23.2 List Follow-Ups
Method
GET
Path
/api/v1/follow-ups
Filters
entry_id

outcome

farm_id

created_by_user_id
23.3 Get Follow-Up
Method
GET
Path
/api/v1/follow-ups/{follow_up_id}
23.4 Record Follow-Up Outcome
Method
PATCH
Path
/api/v1/follow-ups/{follow_up_id}
Request Body
{
  "outcome": "improved",

  "notes": "Symptoms improved"
}
Validation

Outcome must be:

improved

same

worse

unknown
24. Notification APIs

Entity:

notifications
Notification Types

Examples:

upload_reminder

follow_up_reminder

upload_success

upload_failure

system

Actual values must follow frozen enum.

24.1 List Notifications
Method
GET
Path
/api/v1/notifications
Query Parameters
type

status

page
page_size
Response
{
  "data": [
    {
      "notification_id": "uuid",

      "type": "follow_up_reminder",

      "status": "unread"
    }
  ]
}
24.2 Get Notification
Method
GET
Path
/api/v1/notifications/{notification_id}
24.3 Mark Notification Read
Method
PATCH
Path
/api/v1/notifications/{notification_id}/read
Request Body
{
  "status": "read"
}
24.4 Mark All Notifications Read
Method
POST
Path
/api/v1/notifications/mark-all-read
Response
{
  "success": true,

  "updated_count": 15
}
25. Consultation + Follow-Up Workflow

Workflow required by #46A.

User Creates Consultation
            ↓
External AI App
            ↓
User Records Learning
            ↓
Create Follow-Up
            ↓
3 Days
            ↓
7 Days
            ↓
14 Days
            ↓
Outcome Captured
26. Notebook Timeline Rules

Notebook Entry:

1 Entry

contains:

1..N Note Items
Ordering

Must use:

sequence_order

Example:

1 Photo

2 Voice

3 Text

4 Video
27. Media Rules

Supported:

Photo

Video

Voice

File

Storage:

MinIO

Reference:

file_path

Only.

Media is not stored inside database rows.

Part 3 Complete
**************************************


Next Part 4:

File Upload APIs
Upload Queue APIs
Offline Sync APIs
Simulator Rules
QR Rules
A1-A6 Resolution
Authorization Matrix
P0 Required Scope
Future Enhancement
Final Consistency Assessment
Ready For Freeze Review

Part 4 จะเป็นส่วนสุดท้ายของเอกสาร API Specification v1.0 ครับ.

*****************************************
ARI V1 — P0 API Specification v1.0
Part 4 — Upload, Sync, Governance, Freeze Review
28. File Upload APIs

Storage Backend:

MinIO
Design Principles

Media files shall:

Save Local
↓
Upload To MinIO
↓
Link To Note Item

Media content shall NOT be stored inside PostgreSQL.

Only metadata and references are stored in database records.

Supported Upload Types
photo
video
voice
file
28.1 Create Upload URL
Purpose

Generate presigned upload URL.

Method
POST
Path
/api/v1/files/upload-url
Request Body
{
  "entry_id": "uuid",

  "item_type": "photo",

  "file_name": "leaf.jpg",

  "content_type": "image/jpeg",

  "file_size": 1048576
}
Response
{
  "file_key": "organizations/org1/entries/e1/leaf.jpg",

  "upload_url": "https://minio-presigned-url",

  "expires_in": 900
}
Validation
entry_id required

item_type valid

content_type valid

file_size > 0
Authorization

User must access parent notebook entry.

28.2 Complete Upload
Purpose

Confirm upload completed successfully.

Method
POST
Path
/api/v1/files/complete
Request Body
{
  "entry_id": "uuid",

  "file_key": "object-key",

  "upload_status": "completed"
}
Response
{
  "success": true
}
Validation
File must exist in MinIO
28.3 Report Upload Failure
Method
POST
Path
/api/v1/files/upload-failed
Request Body
{
  "entry_id": "uuid",

  "file_key": "object-key",

  "reason": "network_error"
}
Response
{
  "success": true
}
29. Upload Queue APIs

Entity:

upload_queue

Purpose:

Offline First Synchronization
Upload Lifecycle
Pending
↓
Uploading
↓
Completed

or

Pending
↓
Uploading
↓
Failed
↓
Retry
29.1 Create Upload Queue Record
Method
POST
Path
/api/v1/upload-queue
Request Body
{
  "client_id": "uuid",

  "entry_id": "uuid",

  "upload_entity_type": "notebook_entry",

  "upload_action": "create",

  "status": "pending"
}
Response
{
  "queue_id": "uuid",

  "status": "pending"
}
Validation
client_id required

upload_entity_type required

upload_action required
29.2 List Upload Queue
Method
GET
Path
/api/v1/upload-queue
Filters
status

upload_entity_type

upload_action
29.3 Get Upload Queue Record
Method
GET
Path
/api/v1/upload-queue/{queue_id}
29.4 Update Queue Status
Method
PATCH
Path
/api/v1/upload-queue/{queue_id}
Request Body
{
  "status": "uploading",

  "retry_count": 1
}
29.5 Retry Upload
Method
POST
Path
/api/v1/upload-queue/{queue_id}/retry
Response
{
  "queue_id": "uuid",

  "status": "pending"
}
30. Offline Sync APIs
Design Principle

Frozen Requirement:

Save Local
≠ Upload
≠ Analyze
Sync Requirements

Must support:

Offline Capture

Background Sync

Resume Upload

Conflict Handling

Manual Retry

WiFi Only Upload
30.1 Batch Sync
Purpose

Upload multiple offline records.

Method
POST
Path
/api/v1/sync/batch
Request Body
{
  "device_id": "uuid",

  "client_batch_id": "uuid",

  "items": [
    {
      "client_id": "uuid",

      "entity_type": "notebook_entry",

      "action": "create",

      "payload": {}
    }
  ]
}
Response
{
  "client_batch_id": "uuid",

  "results": [
    {
      "client_id": "uuid",

      "server_id": "uuid",

      "status": "completed"
    }
  ]
}
Conflict Handling

When duplicate upload occurs:

client_id

must be used for idempotency.

Duplicate Rule

Same:

client_id

should not create duplicate records.

31. Search APIs
Purpose

Support notebook retrieval.

31.1 Notebook Search
Method
GET
Path
/api/v1/notebook-entries/search
Query Parameters
q

farm_id

zone_id

tree_id

entry_type

date_from

date_to
Search Scope
title

summary

text note items
Explicitly Not Supported
Vector Search

Semantic Search

Knowledge Graph Search

RAG Search

LLM Search
32. Simulator Farm Rules

Simulator farms are supported.

Purpose:

Testing

Training

Demo

Pilot Preparation
Simulator Examples
SIM-001

SIM-DURIAN

SIM-MANGO

SIM-TEST
Simulator Separation Rule

Simulator data:

Must Not

be mixed into production reports by default.

API Requirement

Simulator records should be filterable.

Example:

?is_simulator=true

if supported by implementation.

33. QR / ID Rules

P0 supports:

Farm QR

Zone QR

Tree QR
Domain Rule

QR is:

Representation

not

Separate Entity
QR Endpoints (Optional)
Farm QR
GET
/api/v1/farms/{farm_id}/qr
Zone QR
GET
/ api/v1/zones/{zone_id}/qr
Tree QR
GET
/ api/v1/trees/{tree_id}/qr
Response Example
{
  "entity_type": "tree",

  "entity_id": "uuid",

  "qr_payload": "ari://tree/{tree_id}"
}
34. Standard Authorization Matrix
Resource	Farmer	Coordinator	Agronomist	Reviewer	ARI Staff	Admin	Root
Organizations	Limited	Limited	Limited	Limited	Assigned	Manage	Full
Users	Own	Limited	Limited	Limited	Assigned	Manage	Full
Farms	Assigned	Assigned	Assigned	Assigned	Assigned	Manage	Full
Zones	Assigned	Assigned	Assigned	Assigned	Assigned	Manage	Full
Trees	Assigned	Assigned	Assigned	Assigned	Assigned	Manage	Full
Notebook Entries	Own	Assigned	Assigned	Review Scope	Assigned	Manage	Full
Note Items	Own	Assigned	Assigned	Review Scope	Assigned	Manage	Full
Follow-Ups	Own	Assigned	Assigned	Review Scope	Assigned	Manage	Full
Notifications	Own	Own	Own	Own	Own	Manage	Full
Upload Queue	Own	Own	Own	Own	Assigned	Manage	Full
35. Assumptions Requiring Owner Confirmation
A1 — Owner ID
Finding

Referenced in #46B:

Owner ID
Owner Registry

Not present in:

P0 Domain Model

P0 Database Schema
Resolution
Organization
=
Ownership Boundary

No Owner API introduced.

A2 — Block ID
Finding

Referenced in #46B:

Block ID
Block Registry

Not present in frozen model.

Resolution
Zone
=
Operational Block

No Block API introduced.

A3 — Review Workspace
Finding

Review UX exists.

No reviews table exists.

Resolution

Use:

notebook_entries

analysis_status

consultation_status

No Review API introduced.

A4 — Knowledge Workspace
Finding

Knowledge Workspace exists in UX.

No knowledge tables exist.

Resolution

Knowledge remains:

Future Phase

No Knowledge API introduced.

A5 — Audit Logs
Finding

Auditability required.

No audit_logs table exists.

Resolution

Use:

Backend Logs

Infrastructure Logs

No Audit API introduced.

A6 — Permissions / Assignments
Finding

Permission concepts exist.

Dedicated permission tables do not exist.

Resolution

Use:

RBAC

Organization Scope

Farm Scope

No Permission API introduced.

36. P0 Required Scope

Must be implemented.

Identity
organizations

users
Farm Structure
farms

zones

trees
Notebook
notebook_entries

note_items
Consultation
consultation entry type
Follow-Up
follow_ups
Notifications
notifications
Offline Sync
upload_queue

sync
File Upload
MinIO
37. Optional Extension

May be implemented without schema redesign.

QR APIs
Farm QR

Zone QR

Tree QR
Export APIs
PDF

CSV
Share Integration
Share → ARI
38. Future Enhancement

Not P0.

Knowledge APIs

Review APIs

Case Library APIs

Knowledge Asset APIs

Audit APIs

Permission APIs

AI Agent APIs

Knowledge Graph APIs

Vector Search APIs

RAG APIs

Commerce APIs

Robot APIs

Carbon APIs

ESG APIs
39. Final Consistency Assessment

This specification preserves:

One Platform

One Backend

One Database Architecture

One Mobile App

One Web App

One Domain Model

One RBAC System

and remains consistent with:

#44 Farm AIOS

#45 Software Architecture Rev2.0

#46 MVP Build Plan

#46A Mobile UX

#46B Web UX

#47 AI Agent Workflow

P0 Domain Model v1.0

P0 Database Schema v1.0
40. Freeze Readiness Review
Architecture Review
PASS
MVP Scope Review
PASS
Domain Model Review
PASS
Database Schema Review
PASS
Cross-Document Gap Review
A1 Resolved

A2 Resolved

A3 Resolved

A4 Resolved

A5 Resolved

A6 Resolved
Status
READY FOR FREEZE REVIEW
End of Document

ARI V1 — P0 API Specification v1.0
Phase 3 API Layer
Ready For Owner Review / Freeze Decision

**********************************************

*************
Freeze now
**************

บทราบ

ARI V1 — P0 API Specification v1.0
Status
FROZEN
Freeze Date
2026-06-16
Freeze Scope
Phase 3
P0 API Layer
Frozen Dependencies
Architecture
#44 Farm AI Operating System

#45 Software Architecture & Monorepo Specification Rev2.0
MVP
#46 MVP Software Build Plan

#46A Mobile App UX Flow & Screen Specification

#46B Web App UX Flow & Screen Specification
Development
#47 AI Agent Development Workflow Framework
Core
ARI V1 — P0 Domain Model Specification v1.0

ARI V1 — P0 Database Schema Specification v1.0
Freeze Decision

The following are now frozen:

Authentication
JWT Authentication

Access Token

Refresh Token
Authorization
RBAC

farmer
ari_staff
farm_coordinator
agronomist
reviewer
admin
root
Identity APIs
organizations
users
Farm Structure APIs
farms
zones
trees
Notebook APIs
notebook_entries
note_items
Consultation APIs
entry_type = consultation
Follow-Up APIs
follow_ups
Notification APIs
notifications
File Upload APIs
MinIO Presigned Upload
Offline Sync APIs
upload_queue

sync/batch

client_id idempotency
Search APIs
Keyword Search Only
Frozen Architectural Constraints
One Platform

One Backend

One Database Architecture

One Mobile App

One Web App

One Domain Model

One RBAC System
Frozen P0 Boundary

P0 includes:

Capture

Store

Search

Review Preparation

Consultation Tracking

Follow-Up Tracking

Offline Sync

P0 excludes:

ERP

Marketplace

Commerce

Knowledge Graph

Vector Database

RAG

Multi-Agent System

Robot Platform

Autonomous AI

Knowledge Assets

Case Library

Audit System

Fine-Grained Permission System
Frozen Cross-Document Gap Resolutions
A1
Owner
=
Organization
A2
Block
=
Zone
A3
Review
=
Notebook Filters + Status
A4
Knowledge
=
Future Phase
A5
Audit
=
Backend / Infrastructure Logs
A6
Permissions
=
RBAC + Organization Scope + Farm Scope
Change Control

After this freeze:

No Domain Redesign

No Database Redesign

No New Core Entity

No API Breaking Change

unless processed through:

Revision Proposal
→ Review
→ Approval
→ New Version
Official Status
ARI V1 — P0 Domain Model Specification v1.0
FROZEN

ARI V1 — P0 Database Schema Specification v1.0
FROZEN

ARI V1 — P0 API Specification v1.0
FROZEN
P0 Core Layer Completion
P0-1 Domain Model
✓ Frozen

P0-2 Database Schema
✓ Frozen

P0-3 API Specification
✓ Frozen


******************************
2026-06-19 
******************************

# Revision Note — ARI V1 P0 API Specification Additive Revision v1.1

## 1. Revision Purpose

This revision note records additive API changes required by Owner-approved P1-2 Mobile App onboarding decisions.

This revision does not replace:

```text
ARI V1 — P0 API Specification v1.0
```

This revision extends the existing API specification only where required for mobile onboarding.

---

# 2. Revision Scope

## Affected API Areas

```text
Authentication API
User API
Organization Assignment
Farm API
Farm Join / Membership Status
Farm Location Payload
```

## Unaffected API Areas

This revision must not change:

```text
Notebook Entry API structure
Note Item API structure
Consultation as Notebook Entry Type
QR as representation
MinIO upload endpoints
Sync batch endpoint
Notification API
Follow-up API
Keyword/filter search only
```

---

# 3. Authentication API Additions

## 3.1 Add Register Endpoint

### Method

```http
POST
```

### Path

```text
/api/v1/auth/register
```

### Purpose

Allow new Android/iOS mobile users to self-register.

Registration requires internet connection.

---

## 3.2 Register Request — Owner

```json
{
  "phone": "0812345678",
  "name": "Somchai",
  "password": "1234",
  "farmer_status": "owner",
  "farm_id": null
}
```

---

## 3.3 Register Request — Owner Family / Farm Staff

```json
{
  "phone": "0812345678",
  "name": "Worker Name",
  "password": "1234",
  "farmer_status": "farm_staff",
  "farm_id": "ARI-FARM-A123"
}
```

---

## 3.4 Allowed farmer_status Values

```text
owner
owner_family
farm_staff
```

---

## 3.5 Register Validation Rules

```text
phone required
phone must be normalized before lookup/storage
phone must be unique
name required
password required
farmer_status required
farmer_status must be valid
farm_id required when farmer_status = owner_family
farm_id required when farmer_status = farm_staff
farm_id must exist when provided
password must be stored only as password_hash
role must be assigned as farmer
```

Default password:

```text
1234
```

is allowed only for P0 pilot.

---

## 3.6 Register Response — Owner

```json
{
  "user_id": "uuid",
  "phone": "0812345678",
  "role": "farmer",
  "farmer_status": "owner",
  "organization_id": "uuid",
  "account_status": "active_pending_verification",
  "access_token": "jwt",
  "refresh_token": "jwt"
}
```

---

## 3.7 Register Response — Owner Family / Farm Staff

```json
{
  "user_id": "uuid",
  "phone": "0812345678",
  "role": "farmer",
  "farmer_status": "farm_staff",
  "organization_id": "uuid",
  "primary_farm_id": "ARI-FARM-A123",
  "membership_status": "pending_farm_approval",
  "access_token": "jwt",
  "refresh_token": "jwt"
}
```

---

## 3.8 Alternative Register Response

If backend does not issue tokens immediately after registration:

```json
{
  "user_id": "uuid",
  "phone": "0812345678",
  "role": "farmer",
  "farmer_status": "owner",
  "organization_id": "uuid",
  "requires_login": true,
  "message": "Registration completed. Please login."
}
```

---

## 3.9 Register Error Responses

```text
400 invalid request
401 not applicable
403 registration not allowed
404 farm_id not found
409 phone already exists
422 validation error
500 server error
```

---

# 4. Login API Revision

## Existing Endpoint

```http
POST /api/v1/auth/login
```

## Revised Request

```json
{
  "phone": "0812345678",
  "password": "1234"
}
```

## Response

```json
{
  "access_token": "jwt",
  "refresh_token": "jwt",
  "token_type": "bearer"
}
```

## Login Rules

```text
Phone-number login is required for P1-2 mobile.
Email login may remain supported if already implemented.
Backend must normalize phone before lookup.
Backend must find user by normalized phone.
Backend must verify password_hash.
Backend must check account_status.
Backend must check membership_status when farm access is required.
```

## Security Rules

Do not store or log:

```text
plain password
plain token
password in logs
token in logs
```

---

# 5. Current User API Revision

## Existing Endpoint

```http
GET /api/v1/auth/me
```

## Revised Response

```json
{
  "user_id": "uuid",
  "phone": "0812345678",
  "name": "Somchai",
  "role": "farmer",
  "farmer_status": "owner",
  "organization_id": "uuid",
  "primary_farm_id": null,
  "membership_status": "active",
  "account_status": "active"
}
```

## Rules

The response must expose mobile onboarding state so the app can decide:

```text
Can access farm
Must wait for approval
Can create farm
Must complete setup
Account blocked
```

Mobile visibility is not authorization.

Backend remains authorization source of truth.

---

# 6. User API Additive Fields

User API responses may expose:

```text
phone
farmer_status
membership_status
primary_farm_id
account_status
```

## Non-Change

Do not create APIs for:

```text
/member-registry
/owner-registry
/farmer-registry
/mobile-users
/permissions
```

---

# 7. Owner Registration API Behavior

When:

```text
farmer_status = owner
```

Backend must:

```text
Create user_id
Assign role = farmer
Create or assign organization_id immediately
Return organization_id
Set membership_status = active
Set account_status = active_pending_verification or pending_review
Allow owner to create farm under own organization
```

Owner may create multiple farms:

```text
organization_id
 ├── farm_id_1
 ├── farm_id_2
 └── farm_id_3
```

## Authorization Rules

Owner must not:

```text
Access other organizations
Create farms under another organization
Create admin/root/ari_staff users
```

---

# 8. Owner Family / Farm Staff Registration API Behavior

When:

```text
farmer_status = owner_family
```

or:

```text
farmer_status = farm_staff
```

Backend must:

```text
Require farm_id
Validate farm_id exists
Resolve farm_id → organization_id
Create user_id
Assign role = farmer
Set primary_farm_id = provided farm_id
Set membership_status = pending_farm_approval
Restrict farm access until approved
```

## Pending Approval Message

Mobile may display:

```text
ส่งคำขอเข้าร่วมสวนแล้ว
กรุณารอเจ้าของสวนหรือผู้ดูแลระบบอนุมัติ
```

## Pending Access Restrictions

Until approved, backend must block:

```text
Farm notebook access
Farm-scoped upload/sync
Farm/Zone/Tree creation
Farm data read access
```

Backend may allow:

```text
profile read
logout
status refresh
```

---

# 9. Membership Status API Interpretation

Allowed values:

```text
pending_farm_approval
active
rejected
suspended
revoked
```

## Behavior

### pending_farm_approval

User registered but not yet approved for farm access.

### active

User can access approved farm scope.

### rejected

Join request rejected.

### suspended

Access temporarily blocked.

### revoked

Access removed.

---

# 10. Farm API Revision

## Existing Endpoint

```http
POST /api/v1/farms
```

## Revised Purpose

Allow self-registered owner to create farms under own organization.

---

## Revised Request

```json
{
  "farm_name": "สวนทุเรียนคลองสิบ",
  "location": {
    "province": "จันทบุรี",
    "district": "ท่าใหม่",
    "subdistrict": "เขาบายศรี",
    "address": "ใกล้วัด เข้าซอย 2 กม.",
    "gps_latitude": 12.345678,
    "gps_longitude": 102.345678,
    "source": "device_gps"
  },
  "description": "สวนหลักของครอบครัว"
}
```

## Required From User

```text
farm_name
```

## Optional From User

```text
location
description
```

## System Generated

```text
farm_id
farm_code
organization_id
created_by_user_id
status
created_at
```

## Owner Must Not Manually Provide

```text
farm_id
organization_id
created_by_user_id
status
```

---

# 11. Farm Create Authorization Rules

## Owner

May create multiple farms under own organization.

## Owner Family

Must not create:

```text
Farm
Zone
Tree
```

## Farm Staff

Must not create:

```text
Farm
Zone
Tree
```

## Backend Rule

Mobile UI visibility is not authorization.

Backend must enforce all restrictions.

---

# 12. Farm Location Payload

API must support structured location object.

## Supported Structure

```json
{
  "province": "จันทบุรี",
  "district": "ท่าใหม่",
  "subdistrict": "เขาบายศรี",
  "address": "ใกล้วัด เข้าซอย 2 กม.",
  "gps_latitude": 12.345678,
  "gps_longitude": 102.345678,
  "source": "device_gps"
}
```

## Rules

```text
province optional
district optional
subdistrict optional
address optional
gps_latitude optional
gps_longitude optional
source optional
```

If gps_latitude is provided:

```text
must be valid latitude
```

If gps_longitude is provided:

```text
must be valid longitude
```

---

# 13. Farm Join Approval API Policy

P1-2 minimal policy:

```text
Admin / ARI Staff handles approval through backend/admin workflow.
Owner self-approval screen is Future Enhancement.
```

## No P1-2 Requirement For

```text
Owner-managed member approval screen
Invite code
farm_memberships table
multi-farm membership management
```

## Minimal Approval Endpoint

If API support is required, use existing User API pattern:

```http
PATCH /api/v1/users/{user_id}
```

with:

```json
{
  "membership_status": "active"
}
```

or:

```json
{
  "membership_status": "rejected"
}
```

## Approval Authorization

Allowed:

```text
admin
root
ari_staff
```

if explicitly permitted.

Do not create:

```text
/farm-memberships
/join-requests
/permissions
```

---

# 14. Status Transition Rules

Allowed membership_status transitions:

```text
pending_farm_approval → active
pending_farm_approval → rejected
active → suspended
active → revoked
suspended → active
```

Invalid transitions should return:

```text
409 Conflict
```

---

# 15. P0 API Non-Changes

This revision must not change:

```text
Consultation = Notebook Entry Type
QR = Representation only
No qr_registry
No consultation entity
No permission service
Upload endpoints unchanged
Sync batch endpoint unchanged
Follow-up API unchanged
Notification API unchanged
Keyword/filter search only
```

## Upload Endpoints Unchanged

```http
POST /api/v1/files/upload-url
POST /api/v1/files/complete
POST /api/v1/files/upload-failed
```

## Sync Endpoint Unchanged

```http
POST /api/v1/sync/batch
```

## Follow-Up Rules Unchanged

Periods:

```text
3
7
14
```

Outcomes:

```text
improved
same
worse
unknown
```

---

# 16. Implementation Dependency Notice

This API revision depends on additive support from:

```text
P0 Domain Model Additive Revision
P0 Database Schema Additive Revision
P1-1 Backend Implementation
P1-2 Mobile App Implementation
```

This document does not define those revisions.

This document only defines the API-level additive changes.

---

# 17. Revision Status

```text
ARI V1 — P0 API Specification v1.0
Status: Frozen

ARI V1 — P0 API Specification Additive Revision v1.1
Status: Ready for Owner Review
```

If approved and merged:

```text
ARI V1 — P0 API Specification v1.1
Status: Ready for Freeze Review
```

---

# 18. Final Consistency Statement

This additive API revision remains within the approved ARI constraints:

```text
One Platform
One Backend
One Database Architecture
One Mobile App
One Web App
One Domain Model
One RBAC System
```

It does not introduce:

```text
Owner Registry
Member Registry
Farmer Registry
Separate Mobile User Table
Permission Table
QR Registry
Consultation Entity
Farm Membership Table
Knowledge API
Robot API
Commerce API
```

This revision only extends authentication, user state exposure, farm creation behavior, and mobile onboarding API support.


*********************
Freeze
*********************

# ARI V1 — P0 API Specification Additive Revision v1.1

## Freeze Record

### Freeze Status

```text
FROZEN
```

### Freeze Date

```text
2026-06-19
```

---

# Parent Documents

This additive revision is attached to:

```text
ARI V1 — P0 API Specification v1.0
```

Status:

```text
FROZEN
```

---

# Dependency Documents

This revision assumes compatibility with:

```text
ARI V1 — P0 Domain Model Additive Revision v1.1

ARI V1 — P0 Database Schema Additive Revision v1.1
```

and does not replace them.

---

# Approved Corrections Before Freeze

## Primary Farm Identifier

Replace all examples using:

```text
primary_farm_id = "ARI-FARM-A123"
```

with:

```text
primary_farm_id = "uuid"
```

Example:

```json
{
  "user_id": "uuid",
  "phone": "0812345678",
  "role": "farmer",
  "farmer_status": "farm_staff",
  "organization_id": "uuid",
  "primary_farm_id": "uuid",
  "membership_status": "pending_farm_approval",
  "access_token": "jwt",
  "refresh_token": "jwt"
}
```

Farm display code may remain:

```text
ARI-FARM-A123
```

as:

```text
farm_code
```

only.

---

# Frozen Additive Scope

## Authentication

Added:

```http
POST /api/v1/auth/register
```

Revised:

```http
POST /api/v1/auth/login
```

Supports:

```text
phone login
```

Required for:

```text
P1-2 Mobile Onboarding
```

---

## Auth Me

Expanded payload:

```text
phone

farmer_status

membership_status

primary_farm_id

account_status
```

---

## User API Exposure

Allowed user state exposure:

```text
phone

farmer_status

membership_status

primary_farm_id

account_status
```

---

## Owner Registration Flow

Supported:

```text
owner
```

Behavior:

```text
Create User

Assign Role = farmer

Create / Assign Organization

Allow Farm Creation
```

---

## Owner Family Registration Flow

Supported:

```text
owner_family
```

Behavior:

```text
Require Farm ID

Resolve Organization

Pending Approval
```

---

## Farm Staff Registration Flow

Supported:

```text
farm_staff
```

Behavior:

```text
Require Farm ID

Resolve Organization

Pending Approval
```

---

## Membership Lifecycle

Supported values:

```text
pending_farm_approval

active

rejected

suspended

revoked
```

---

## Farm Creation Payload

Farm API supports:

```json
{
  "farm_name": "...",
  "location": {},
  "description": "..."
}
```

with structured location payload.

---

## Farm Location Payload

Supported fields:

```text
province

district

subdistrict

address

gps_latitude

gps_longitude

source
```

---

# Explicit Non-Changes

This revision does NOT introduce:

```text
Owner Registry

Member Registry

Farmer Registry

Farm Membership Table

Permission Service

Permission Table

QR Registry

Consultation Entity

Knowledge API

Robot API

Commerce API
```

---

# Existing Frozen Decisions Preserved

```text
Consultation
=
Notebook Entry Type
```

```text
QR
=
Representation Only
```

```text
Upload
=
MinIO Presigned Upload
```

```text
Sync
=
sync/batch
```

```text
Follow-Up
=
3 / 7 / 14 Day Model
```

```text
Search
=
Keyword / Filter Search Only
```

---

# Architectural Compliance

This additive revision remains compliant with:

```text
One Platform

One Backend

One Database Architecture

One Mobile App

One Web App

One Domain Model

One RBAC System
```

---

# Final Status

```text
ARI V1 — P0 API Specification v1.0
FROZEN

ARI V1 — P0 API Specification Additive Revision v1.1
FROZEN
```

---

# Governance Note

Future onboarding changes that require:

```text
new entities
new tables
new RBAC roles
new services
```

must be processed through:

```text
Domain Revision
→ Database Revision
→ API Revision
→ Implementation Revision
```

and must not modify this frozen revision directly.

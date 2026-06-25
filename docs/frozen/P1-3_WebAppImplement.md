# ARI V1 — P1-3 Web App Implementation Specification v1.0

## 1. Document Control

Project: ARI — Agricultural Intelligence Platform

Document Title: ARI V1 — P1-3 Web App Implementation Specification v1.0

Version: v1.0

Status: Draft Final / Ready for Owner Review

Scope: Web App Implementation Specification

Target Interface:

```text
Browser-based Web App
```

Target Usage Devices:

```text
Notebook browser
PC browser
Mac browser
Ubuntu/Linux browser
Desktop browser
```

This document defines how to implement the ARI Web App using the existing ARI backend, existing `/api/v1` API contracts, existing domain model, existing database architecture, and existing RBAC system.

This document does not redesign:

```text
ARI Architecture
Backend Architecture
Database Architecture
Core Domain Model
RBAC Role List
Mobile App Scope
Desktop App Scope
```

### 1.1 Document Status

```text
Document Status: Draft Final / Ready for Owner Review
Freeze Readiness: Ready after API Gap review
Implementation Phase: P1-3
```

### 1.2 P1-3 Position

```text
P1-1 = Backend Implementation
P1-2 = Mobile App Implementation
P1-3 = Web App Implementation
```

P1-3 implements the browser-based Web App only.

P1-3 does not implement:

```text
Mobile App
Native Desktop App
Electron App
Flutter Desktop App
macOS App
Ubuntu App
Windows App
```

---

## 2. Source of Truth

P1-3 follows the frozen and approved ARI documents:

```text
#44 Farm AI Operating System
#45 Software Architecture & Monorepo Specification Rev2.0
#46 MVP Software Build Plan
#46A Mobile App UX Flow & Screen Specification
#46B Web App UX Flow & Screen Specification
#47 AI Agent Development Workflow Framework

ARI V1 — P0 Domain Model Specification v1.0
ARI V1 — P0 Domain Model Additive Revision v1.1

ARI V1 — P0 Database Schema Specification v1.0
ARI V1 — P0 Database Schema Additive Revision v1.1

ARI V1 — P0 API Specification v1.0
ARI V1 — P0 API Specification Additive Revision v1.1

ARI V1 — P1-1 Backend Implementation Specification v1.0
ARI V1 — P1-2 Mobile App Implementation Specification v1.0 — FROZEN
```

### 2.1 Frozen Principles Preserved

P1-3 must preserve:

```text
One Platform
One Backend
One Database Architecture
One Mobile App
One Web App
One Domain Model
One RBAC System
```

### 2.2 Frozen Domain Rules Preserved

```text
Organization owns data
Users create data

Notebook Entry = Note Session
Note Item = Timeline Item
Consultation = Notebook Entry Type

Save Local ≠ Upload ≠ Analyze

QR = Representation only

farm_id nullable
zone_id nullable
tree_id nullable

RBAC = backend authorization dependency guards
Web visibility ≠ authorization authority
```

### 2.3 Frozen P1-2 Rules Respected

P1-3 must remain aligned with the frozen P1-2 decisions:

```text
Mobile App = Flutter
Target platforms = Android and iOS only
Web App = P1-3
Desktop App = out of scope
Phone self-registration supported by approved backend/API revision
Phone-number login supported
farmer_status:
  - owner
  - owner_family
  - farm_staff
membership_status:
  - pending_farm_approval
  - active
  - rejected
  - suspended
  - revoked
Owner may have multiple farms
Owner's Family / Farm Staff join by Farm ID, not Owner ID
First-time permission setup belongs to mobile implementation
Offline-first capture belongs primarily to mobile implementation
Ask AI = external consultation flow
Consultation = Notebook Entry Type
No permission service
No new RBAC role
No qr_registry
No consultation entity
```

---

## 3. Implementation Boundary

### 3.1 P1-3 Required

P1-3 covers:

```text
Web project structure
Frontend technology stack
Routing structure
Authentication flow
Phone-number login
Token handling
Current user restore
RBAC-based navigation visibility
Dashboard layout
Farm List page
Farm Detail page
Farm Notebook page
Notebook Entry Detail page
Media viewer
Consultation review display
Follow-up review display
Notification view
Approval Queue
Knowledge Candidate page
Knowledge Library page
User / Organization management view
Farm / Zone / Tree management view
Pending member approval view if supported by existing backend scope
Search and filters
Error handling
Security handling
Environment configuration
Testing strategy
Build and deployment
```

### 3.2 P1-3 Optional Extension

The following may be implemented only if they use existing entities and existing APIs:

```text
QR print view from existing Farm / Zone / Tree IDs
CSV export from displayed table data
Media thumbnail display if returned by backend
Saved table filter presets stored locally in browser
TH / EN language selector
Read-only simulator farm filter
```

Optional extensions must not introduce:

```text
New backend service
New database table
New domain entity
New RBAC role
New permission engine
```

### 3.3 P1-3 Future Enhancement

The following are not part of P1-3 implementation:

```text
Dedicated Knowledge Asset service
Knowledge Graph
Vector Database
RAG
Semantic Search
LLM Search
AI Agent Orchestration
Internal AI Assistant
Commerce
Robot Control
Irrigation Control
Fertilizer Control
Advanced Disease Diagnosis
Automatic Treatment Recommendation
Advanced GIS
Farm Boundary Mapping
Zone Boundary Mapping
Tree GPS Mapping
Case Library entity
Audit Log API
Permission Matrix Engine
ABAC
Farm Membership table
Invite Code system
Native desktop app
Electron desktop app
```

### 3.4 Explicit Non-Goals

P1-3 must not create:

```text
Separate farmer web app
Separate staff web app
Separate admin backend
Separate web backend
Separate database architecture
New RBAC role
Permission service
Permission matrix engine
QR registry
Consultation entity
Owner registry
Farmer registry
Member registry
Block registry
Knowledge graph
Vector database
RAG system
Internal AI assistant
Robot control module
Commerce module
Desktop app
```

---

## 4. Web App Principle

### 4.1 Web App Positioning

```text
Mobile App = Work Anywhere / Capture First
Web App = Work Deep / Review, Manage, Approve, Analyze, Organize
```

### 4.2 Web App Purpose

The Web App is the deep-work interface for:

```text
Review
Analysis
Knowledge curation
Farm organization
Member approval support
Notebook review
Media review
Follow-up management
Administration
Governance
```

### 4.3 User Mental Model

The Web App should help users answer:

```text
What needs review?
Which farms need attention?
Which notes are important?
Which consultations need follow-up?
Which records can become knowledge candidates?
Which users or members need approval?
```

### 4.4 Implementation Principle

Web App may:

```text
Display data
Filter data
Review data
Update allowed records
Organize records
Show role-based navigation
Use approved backend APIs
```

Web App must not:

```text
Act as permission authority
Bypass backend authorization
Access MinIO directly without backend contract
Create new core entities
Create new authorization logic
Create desktop packaging
```

---

## 5. Technology Stack

### 5.1 Frontend Framework

Recommended Web App stack:

```text
Next.js
React
TypeScript
```

Rationale:

```text
Aligned with ARI web platform direction
Compatible with FastAPI REST API
Suitable for browser-based desktop use
Supports routed workspaces
Supports server-side or client-side rendering where needed
```

### 5.2 Styling / UI

Recommended:

```text
Component-based UI
Responsive desktop-first layout
CSS modules / utility CSS / design system approach
TH / EN text support
```

Implementation must remain simple.

Do not introduce complex UI platform architecture.

### 5.3 Data Fetching

Recommended:

```text
API client wrapper
Query/cache layer
Typed DTOs
Pagination support
Filter state support
Token refresh interceptor
```

### 5.4 API Base

```text
/api/v1
```

The Web App must not call a separate web backend.

### 5.5 Authentication

```text
JWT Access Token
Refresh Token
Phone-number login
Current user restore through GET /api/v1/auth/me
```

### 5.6 Media

Media must be accessed only through:

```text
Backend-approved file references
Backend-approved media URLs
Backend-generated presigned read URLs if available
```

Do not directly access MinIO using public bucket assumptions.

### 5.7 Out of Scope Technologies

Do not implement:

```text
Electron
Flutter Web if it implies duplication of the mobile implementation
Flutter Desktop
Native desktop packaging
Separate admin frontend
Separate staff frontend
Separate farmer frontend
```

---

## 6. Web Project Structure

The Web App must live under:

```text
web/
```

Required structure:

```text
web/
├── package.json
├── tsconfig.json
├── next.config.js
├── README.md
├── .env.example
├── public/
├── src/
│   ├── app/
│   │   ├── layout.tsx
│   │   ├── page.tsx
│   │   ├── login/
│   │   │   └── page.tsx
│   │   ├── register/
│   │   │   └── page.tsx
│   │   ├── dashboard/
│   │   │   └── page.tsx
│   │   ├── farms/
│   │   │   ├── page.tsx
│   │   │   └── [farmId]/
│   │   │       └── page.tsx
│   │   ├── notebook/
│   │   │   ├── page.tsx
│   │   │   └── [entryId]/
│   │   │       └── page.tsx
│   │   ├── review/
│   │   │   └── page.tsx
│   │   ├── knowledge-candidates/
│   │   │   └── page.tsx
│   │   ├── knowledge-library/
│   │   │   └── page.tsx
│   │   ├── follow-ups/
│   │   │   └── page.tsx
│   │   ├── notifications/
│   │   │   └── page.tsx
│   │   ├── administration/
│   │   │   ├── page.tsx
│   │   │   ├── users/
│   │   │   │   └── page.tsx
│   │   │   ├── organizations/
│   │   │   │   └── page.tsx
│   │   │   └── pending-members/
│   │   │       └── page.tsx
│   │   └── settings/
│   │       └── page.tsx
│   ├── core/
│   │   ├── api/
│   │   │   ├── apiClient.ts
│   │   │   ├── endpoints.ts
│   │   │   ├── apiError.ts
│   │   │   └── pagination.ts
│   │   ├── auth/
│   │   │   ├── authStore.ts
│   │   │   ├── tokenStore.ts
│   │   │   ├── sessionManager.ts
│   │   │   └── authGuard.ts
│   │   ├── config/
│   │   │   ├── env.ts
│   │   │   └── constants.ts
│   │   ├── rbac/
│   │   │   ├── roles.ts
│   │   │   ├── navigationVisibility.ts
│   │   │   └── roleLabels.ts
│   │   ├── i18n/
│   │   │   ├── th.ts
│   │   │   └── en.ts
│   │   └── utils/
│   │       ├── datetime.ts
│   │       ├── phone.ts
│   │       ├── format.ts
│   │       └── qrPayload.ts
│   ├── features/
│   │   ├── auth/
│   │   │   ├── api.ts
│   │   │   ├── models.ts
│   │   │   └── components/
│   │   ├── dashboard/
│   │   ├── farms/
│   │   ├── farm-context/
│   │   ├── notebook/
│   │   ├── note-items/
│   │   ├── media/
│   │   ├── review/
│   │   ├── knowledge-candidates/
│   │   ├── knowledge-library/
│   │   ├── follow-ups/
│   │   ├── notifications/
│   │   ├── users/
│   │   ├── organizations/
│   │   └── administration/
│   ├── shared/
│   │   ├── components/
│   │   ├── layouts/
│   │   ├── tables/
│   │   ├── forms/
│   │   ├── filters/
│   │   ├── media/
│   │   └── empty-states/
│   └── tests/
│       ├── unit/
│       ├── integration/
│       └── e2e/
└── Dockerfile
```

### 6.1 Forbidden Structures

Do not create:

```text
farmer_web/
staff_web/
admin_web/
desktop_app/
electron_app/
permission_engine/
qr_registry_module/
consultation_entity_module/
knowledge_service/
robot_module/
commerce_module/
```

---

## 7. App Architecture

Use simple layered frontend architecture:

```text
Page / Route Layer
↓
Feature Component Layer
↓
Application Hook / State Layer
↓
Repository / API Layer
↓
Backend /api/v1
```

### 7.1 Page / Route Layer

Responsible for:

```text
Route rendering
Page-level data loading
Page-level layout composition
Route access checks
Loading state
Empty state
Error state
```

Must not:

```text
Implement backend business rules
Perform permission decisions beyond UI visibility
Directly call fetch without API client wrapper
Bypass session manager
```

### 7.2 Feature Component Layer

Responsible for:

```text
Tables
Cards
Forms
Filter panels
Detail panels
Media preview
Timeline display
Status badges
Action buttons
```

### 7.3 Application Hook / State Layer

Responsible for:

```text
Session state
Current user state
Active organization context
Active farm context
Filter state
Pagination state
Notification count
Language selection
Role-based navigation visibility
```

### 7.4 Repository / API Layer

Responsible for:

```text
Calling /api/v1 endpoints
Attaching Authorization header
Refreshing access token when supported
Mapping API response envelopes
Mapping error envelopes
Handling pagination
Handling query filters
```

### 7.5 Backend Authority Rule

The Web App may hide or disable UI based on:

```text
role
organization_id
farm scope
membership_status
account_status
feature flags
```

But final authorization always belongs to backend.

---

## 8. Authentication Implementation

### 8.1 Login Flow

Primary login method:

```text
Phone number + password
```

API:

```text
POST /api/v1/auth/login
```

Flow:

```text
User opens /login
↓
User enters phone number
↓
User enters password
↓
Web normalizes phone display if needed
↓
Web calls POST /api/v1/auth/login
↓
Backend validates phone/password
↓
Backend returns access_token + refresh_token + user if supported
↓
Web stores session according to token policy
↓
Web calls GET /api/v1/auth/me
↓
Web restores user profile, role, organization_id, farmer_status, membership_status, account_status, primary_farm_id
↓
Web routes user to dashboard or pending-status screen
```

### 8.2 Email Login Compatibility

Legacy P0 API examples may include email login.

P1-3 must prioritize phone-number login because P1-2 approved phone as platform-wide login identity.

If legacy email login remains available, it may be retained as:

```text
Optional / Compatibility
```

But it must not replace phone login.

### 8.3 Web Registration Policy

Default P1-3 policy:

```text
Web registration is disabled unless Owner explicitly allows it.
```

If Web registration is allowed, it must reuse:

```text
POST /api/v1/auth/register
```

and must follow the same P1-2 onboarding contract:

```text
phone
name
password
farmer_status
farm_id when farmer_status = owner_family or farm_staff
```

Web registration must not create:

```text
New web registration service
New user type
New RBAC role
Member registry
Owner registry
Farmer registry
Farm membership table
```

### 8.4 Current User Restore

API:

```text
GET /api/v1/auth/me
```

Restore data:

```text
user_id
organization_id
role
phone
name
farmer_status
membership_status
account_status
primary_farm_id
```

If some additive fields are missing in `/auth/me`, place under:

```text
API Gap / Revision Proposal
```

### 8.5 Refresh Token Flow

API:

```text
POST /api/v1/auth/refresh
```

Flow:

```text
Access token expires
↓
API client receives 401 or token-expired response
↓
API client calls POST /api/v1/auth/refresh
↓
Backend returns new access_token
↓
API client retries original request once
↓
If refresh fails, clear session and redirect to /login
```

### 8.6 Logout Flow

API:

```text
POST /api/v1/auth/logout
```

Flow:

```text
User clicks logout
↓
Web calls logout endpoint if online
↓
Web clears local session state
↓
Web clears token storage
↓
Web redirects to /login
```

### 8.7 Pending / Blocked Status Routing

After login or restore, Web must handle:

```text
membership_status = pending_farm_approval
membership_status = rejected
membership_status = suspended
membership_status = revoked

account_status = suspended
account_status = rejected
account_status = revoked
```

Required behavior:

```text
pending_farm_approval:
  show pending approval view
  block farm-scoped workspaces

rejected:
  show rejected message

suspended:
  show suspended message

revoked:
  show revoked message
```

Backend remains final authority.

---

## 9. Token Handling

### 9.1 Token Storage Baseline

Baseline P1-3 implementation:

```text
access_token used for Authorization: Bearer <token>
refresh_token used only for refresh endpoint
tokens never logged
tokens never included in URL
tokens cleared on logout
```

### 9.2 Browser Storage Rule

Minimum implementation:

```text
Access token may be held in memory where practical.
Refresh token persistence must be minimized.
If browser storage is used, it must be treated as sensitive.
```

### 9.3 Production Security Recommendation

Preferred production implementation:

```text
HttpOnly secure refresh cookie
Short-lived access token
CSRF protection if cookie-based auth is used
```

### 9.4 API Gap / Revision Proposal — HttpOnly Refresh Cookie

If the backend does not support HttpOnly refresh cookies, P1-3 may proceed with the existing token response contract for pilot use.

For production hardening, propose:

```text
API Gap / Revision Proposal:
Backend supports secure HttpOnly refresh cookie for Web App sessions.
```

This proposal must not create a separate auth service.

---

## 10. RBAC in Web

### 10.1 Frozen Roles

Use only:

```text
farmer
ari_staff
farm_coordinator
agronomist
reviewer
admin
root
```

Do not create:

```text
owner role
owner_family role
farm_staff role
web_admin role
supervisor role
expert role
```

### 10.2 farmer_status vs RBAC Role

```text
farmer_status = onboarding classification
role = RBAC authorization role
```

Allowed `farmer_status` values:

```text
owner
owner_family
farm_staff
```

These are not RBAC roles.

### 10.3 Web Navigation Visibility

Navigation may be hidden or shown based on:

```text
role
farmer_status
membership_status
account_status
organization scope
farm scope
feature availability
```

But Web App must show this implementation note:

```text
UI visibility is not authorization.
Backend remains authorization source of truth.
```

### 10.4 Recommended Navigation Visibility

| Menu                    |                   farmer |         farm_coordinator | agronomist |     reviewer |        ari_staff |  admin | root |
| ----------------------- | -----------------------: | -----------------------: | ---------: | -----------: | ---------------: | -----: | ---: |
| Dashboard               |                      Yes |                      Yes |        Yes |          Yes |              Yes |    Yes |  Yes |
| Farms                   |                   Scoped |                   Scoped |     Scoped |       Scoped |           Scoped | Manage | Full |
| Farm Detail             |                   Scoped |                   Scoped |     Scoped |       Scoped |           Scoped | Manage | Full |
| Notebook                |             Own / Scoped |                   Scoped |     Scoped | Review Scope |           Scoped | Manage | Full |
| Review / Approval Queue |                  Limited |                      Yes |        Yes |          Yes |              Yes |    Yes | Full |
| Knowledge Candidate     |           Read / Limited |                      Yes |        Yes |          Yes |              Yes |    Yes | Full |
| Knowledge Library       |                     Read |                     Read |       Read |         Read |             Read | Manage | Full |
| Follow-ups              |             Own / Scoped |                   Scoped |     Scoped | Review Scope |           Scoped | Manage | Full |
| Notifications           |                      Own |                      Own |        Own |          Own |              Own | Manage | Full |
| Administration          |                       No |                       No |         No |      Limited |          Limited |    Yes | Full |
| Pending Members         | No unless approved later | No unless approved later |         No |           No | Yes if permitted |    Yes | Full |

### 10.5 Pending Member Approval Scope

P1-3 may include pending member approval view only if the backend supports it through existing user APIs and RBAC guards.

Allowed pattern:

```text
GET /api/v1/users?membership_status=pending_farm_approval
PATCH /api/v1/users/{user_id}
```

Do not create:

```text
/member-approvals
/farm-memberships
/member-registry
approval service
permission service
```

---

## 11. Routing Structure

### 11.1 Public Routes

```text
/login
/register        optional; disabled unless Web registration is allowed
/status          optional account status message route
```

### 11.2 Authenticated Routes

```text
/dashboard

/farms
/farms/[farmId]

/notebook
/notebook/[entryId]

/review

/knowledge-candidates
/knowledge-library

/follow-ups

/notifications

/administration
/administration/users
/administration/organizations
/administration/pending-members

/settings
```

### 11.3 Redirect Rules

```text
Unauthenticated user → /login

Authenticated active user → /dashboard

membership_status = pending_farm_approval → /status/pending-approval

account_status suspended/rejected/revoked → /status/account-blocked

403 from backend → show Forbidden page

404 from backend → show Not Found page
```

### 11.4 Route Guard Rule

Route guards only protect frontend UX.

Backend must still reject unauthorized API calls.

---

## 12. Layout / Navigation

### 12.1 Layout Model

Use hybrid desktop layout:

```text
Left Sidebar
Top Bar
Main Content Area
Optional Right Detail Panel
```

### 12.2 Left Sidebar

Required P1-3 navigation:

```text
Dashboard
Farms
Notebook
Review
Knowledge Candidates
Knowledge Library
Follow-ups
Notifications
Administration
Settings
```

### 12.3 Top Bar

Required items:

```text
Global keyword search
Farm context selector if useful
Notifications icon
Language selector TH / EN
User profile menu
Logout
```

### 12.4 Main Content

Main content must support:

```text
Data table views
Detail views
Timeline views
Media review
Filter panels
Status badges
Action buttons
Pagination
```

### 12.5 Responsive Behavior

P1-3 is desktop-browser first.

Minimum behavior:

```text
Works on notebook browser
Works on desktop browser
Works on Mac browser
Works on Ubuntu/Linux browser
```

Mobile browser optimization is not required because mobile work is handled by Flutter mobile app.

---

## 13. Page Implementation Specification

### 13.1 Dashboard Page

Route:

```text
/dashboard
```

Purpose:

```text
Work Queue
```

Not an executive dashboard.

Sections:

```text
My Farms
Pending Reviews
Pending Member Approvals if permitted
New Notebook Entries
Consultation Entries needing review
Follow-ups due
Knowledge Candidates
Notifications / Alerts
```

API dependencies:

```text
GET /api/v1/farms
GET /api/v1/notebook-entries
GET /api/v1/follow-ups
GET /api/v1/notifications
GET /api/v1/users if pending member approval is supported
```

Actions:

```text
Open Farm
Open Notebook Entry
Open Review Queue
Open Follow-up
Open Pending Member
Mark notification read
```

API Gap / Revision Proposal:

```text
If dashboard counts require efficient aggregate endpoints, add optional dashboard summary endpoint in future revision.

Do not add this endpoint silently in P1-3.
```

---

## 14. Farm List / Farm Detail

## 14.1 Farm List Page

Route:

```text
/farms
```

Purpose:

```text
Farm Directory
```

Data source:

```text
GET /api/v1/farms
```

Supported filters:

```text
keyword
organization_id if role allows
status
province if stored in farms.location
created_at date range if supported
simulator flag if supported
```

Displayed columns:

```text
Farm Name
Farm ID
Organization
Province / Location Summary
Status
Created At
Activity Status if available
Actions
```

Actions:

```text
Open Farm Detail
Create Farm if backend allows
Edit Farm if backend allows
Display / Print QR representation if supported
```

Create farm API:

```text
POST /api/v1/farms
```

Update farm API:

```text
PATCH /api/v1/farms/{farm_id}
```

API Gap / Revision Proposal:

```text
If GET /api/v1/farms does not support province/location filtering, keep location filter client-side for the current page only or propose additive backend filter support.

If Web needs farm activity count, propose additive summary fields or dashboard endpoint.
```

### 14.2 Farm Detail Page

Route:

```text
/farms/[farmId]
```

Purpose:

```text
Single workspace for one farm
```

Data source:

```text
GET /api/v1/farms/{farm_id}
GET /api/v1/zones?farm_id={farm_id}
GET /api/v1/notebook-entries?farm_id={farm_id}
GET /api/v1/follow-ups?farm_id={farm_id}
GET /api/v1/users?primary_farm_id={farm_id} if supported
```

Sections:

```text
Overview
Location
Identity / ID / QR representation
Zones
Trees
Farm Notebook
Media
Consultation Entries
Follow-ups
Members if supported
Activity if available
```

P0 location display:

```text
Latitude
Longitude
Province
District
Subdistrict
Address
Location source
```

Map rule:

```text
P1-3 may show a simple farm location marker if location data exists.
P1-3 must not implement advanced GIS boundary mapping.
```

QR rule:

```text
Farm QR / Zone QR / Tree QR may be generated as visual representation from existing IDs.
Do not create qr_registry.
Do not create QR entity.
```

---

## 15. Farm Notebook

### 15.1 Global Notebook Page

Route:

```text
/notebook
```

Purpose:

```text
Global Memory Repository
```

Data source:

```text
GET /api/v1/notebook-entries
```

Optional search source if frozen API supports it:

```text
GET /api/v1/notebook-entries/search
```

Filters:

```text
keyword q
farm_id
zone_id
tree_id
entry_type
entry_context
created_by_user_id
analysis_status
consultation_status
date_from
date_to
status if supported
```

Displayed columns:

```text
Title / Summary
Entry Type
Farm / Zone / Tree context
Created By
Created At
Analysis Status
Consultation Status
Item Count if available
Follow-up Status if available
Actions
```

Actions:

```text
Open Entry Detail
Filter by Farm
Filter by Entry Type
Filter consultation entries
Open Media Review
Promote to Knowledge Candidate if supported by existing status fields
Assign / open Follow-up if supported
```

### 15.2 Farm-Specific Notebook Page

Can be implemented as:

```text
/notebook?farm_id={farm_id}
```

or embedded inside:

```text
/farms/[farmId]
```

Rule:

```text
Do not create separate farm notebook entity.
Use notebook_entries filtered by farm_id.
```

### 15.3 Notebook Search Policy

Allowed:

```text
Keyword search
Filter search
Date filter
Farm filter
Zone filter
Tree filter
Entry type filter
Created by filter
Status filter
```

Not allowed:

```text
Vector search
Semantic search
RAG search
LLM search
Knowledge graph search
```

---

## 16. Notebook Entry Detail

Route:

```text
/notebook/[entryId]
```

Purpose:

```text
Detailed view of one Notebook Entry as Note Session
```

Data source:

```text
GET /api/v1/notebook-entries/{entry_id}
GET /api/v1/note-items?entry_id={entry_id}
GET /api/v1/follow-ups?entry_id={entry_id}
```

Displayed sections:

```text
Entry Summary
Farm / Zone / Tree Context
Entry Type
Entry Context
Created By
Created At / Updated At
Analysis Status
Consultation Status
Timeline of Note Items
Media Viewer
Consultation Result if entry_type = consultation
Follow-up History
Review Actions if role allows
```

### 16.1 Timeline Rule

Notebook Entry contains many Note Items.

Display Note Items ordered by:

```text
sequence_order ASC
created_at ASC as fallback
```

Supported item types:

```text
photo
video
voice
text
file
link
```

### 16.2 Consultation Display Rule

If:

```text
entry_type = consultation
```

Web may display:

```text
ai_provider
learned_summary
ai_usefulness_status
consultation_status
follow-up schedule
follow-up outcome
```

Do not create:

```text
consultation entity
consultation table
consultation service
consultation router
```

### 16.3 Review Actions

Allowed only when backend permits:

```text
Update title
Update summary
Update suggested category
Update analysis_status
Update consultation outcome
Add reviewer notes if already supported
Create follow-up
Record follow-up outcome
Promote to Knowledge Candidate if status field supports it
```

API Gap / Revision Proposal:

```text
If PATCH /api/v1/notebook-entries/{entry_id} or status update is not supported, review actions must be read-only until an additive API revision is approved.
```

---

## 17. Media Viewer

### 17.1 Purpose

Support deep media review from notebook evidence.

Media sources:

```text
Note Items
file_path / file_ref
backend-approved media URL
backend-generated presigned read URL if available
```

Supported media:

```text
Photo
Video
Voice
File
Link
```

### 17.2 Media Viewer Requirements

Photo:

```text
Preview image
Open full screen
Show metadata if available
```

Video:

```text
Play video
Show duration if available
Show file size if available
```

Voice:

```text
Audio player
Duration display if available
```

File:

```text
File name
File type
Download/open action through approved backend URL
```

Link:

```text
Display URL
Open external site in new browser tab
Show platform if available
```

### 17.3 Media Security Rule

Web App must not:

```text
Directly access MinIO buckets
Assume public object URLs
Expose file keys beyond UI need
Log presigned URLs
Cache sensitive media URLs unnecessarily
```

### 17.4 API Gap / Revision Proposal — Media Read URL

If note item responses include only object keys and not authorized read URLs, add:

```text
API Gap / Revision Proposal:
Backend provides approved media read URL or media proxy endpoint for authorized users.
```

Do not bypass backend authorization to solve media viewing.

---

## 18. Approval Queue

Route:

```text
/review
```

Purpose:

```text
Review / Approval Queue for notebook entries and consultation entries
```

Important rule:

```text
Review Workspace is a UI workflow over Notebook Entries.
No reviews table.
No review entity.
No review service.
```

Data source:

```text
GET /api/v1/notebook-entries
```

Suggested filters:

```text
analysis_status
consultation_status
entry_type
farm_id
created_by_user_id
date_from
date_to
status if supported
```

Queue views:

```text
New
In Review
Needs Follow-up
Approved
Knowledge Candidate
Rejected
```

Actions if backend supports update:

```text
Open Entry Detail
Mark In Review
Request Follow-up
Approve
Reject
Promote to Knowledge Candidate
Update summary/category/tags if supported
```

API Gap / Revision Proposal:

```text
If backend does not support status transitions for notebook review, implement Approval Queue as read-only filtered views and propose additive PATCH support for notebook entry review fields.

Do not create Review API or reviews table.
```

---

## 19. Knowledge Candidate

Route:

```text
/knowledge-candidates
```

Purpose:

```text
Workspace for records that may become reusable agricultural knowledge
```

Important boundary:

```text
Knowledge Candidate is a workflow state/view over Notebook Entries.
It is not a new entity in P1-3.
```

Data source:

```text
GET /api/v1/notebook-entries?status=knowledge_candidate
```

or, if status is not available:

```text
GET /api/v1/notebook-entries?analysis_status=approved
```

Displayed fields:

```text
Entry title
Summary
Farm context
Evidence count
Consultation status
Follow-up outcome
Created by
Reviewed by if available
Candidate reason if available
```

Actions if backend supports:

```text
Open Notebook Entry Detail
Edit summary
Add category/tag if supported
Return to Review
Mark ready for Knowledge Library if supported
```

API Gap / Revision Proposal:

```text
If there is no approved field representing knowledge_candidate, propose additive enum/status support on notebook_entries.

Do not add knowledge_candidate table.
Do not add knowledge service.
```

---

## 20. Knowledge Library

Route:

```text
/knowledge-library
```

Purpose:

```text
Basic read-oriented library of approved reusable lessons from existing Notebook Entries
```

P1-3 boundary:

```text
Knowledge Library in P1-3 is a basic UI view.
It must not create a Knowledge Asset entity.
It must not create Knowledge Graph.
It must not create Case Library entity.
It must not create RAG.
```

Allowed implementation:

```text
Display approved notebook entries
Display completed consultation outcomes
Display follow-up outcomes
Display evidence timeline
Filter by keyword/farm/topic/status
```

Data source:

```text
GET /api/v1/notebook-entries
GET /api/v1/note-items
GET /api/v1/follow-ups
```

Allowed filters:

```text
q
farm_id
entry_type
analysis_status
consultation_status
follow_up_outcome
date_from
date_to
```

API Gap / Revision Proposal:

```text
If true Knowledge Library publishing requires separate lifecycle, versioning, article body, confidence score, or case object, that belongs to Future Enhancement.

Do not implement it silently in P1-3.
```

---

## 21. User / Organization Management

### 21.1 Administration Overview

Route:

```text
/administration
```

Visible to:

```text
admin
root
ari_staff if permitted
reviewer limited if permitted
```

Purpose:

```text
Basic management view for users and organizations within existing RBAC scope
```

### 21.2 Users Page

Route:

```text
/administration/users
```

Data source:

```text
GET /api/v1/users
GET /api/v1/users/{user_id}
PATCH /api/v1/users/{user_id}
```

Filters:

```text
organization_id
role
status
phone
farmer_status
membership_status
account_status
primary_farm_id
```

Displayed fields:

```text
Name
Phone
Email if available
Role
farmer_status
membership_status
account_status
Organization
Primary Farm
Created At
Actions
```

Actions if backend permits:

```text
View user
Update user status
Update account_status
Update membership_status
Assign primary_farm_id if supported
Suspend / revoke if supported
```

Do not create:

```text
member_registry
farmer_registry
owner_registry
permission table
```

### 21.3 Pending Member Approval Page

Route:

```text
/administration/pending-members
```

Purpose:

```text
Review users with membership_status = pending_farm_approval
```

Data source:

```text
GET /api/v1/users?membership_status=pending_farm_approval
```

Approval action:

```text
PATCH /api/v1/users/{user_id}
```

Allowed transitions if backend supports:

```text
pending_farm_approval → active
pending_farm_approval → rejected
active → suspended
active → revoked
suspended → active
```

Visible to:

```text
admin
root
ari_staff if explicitly permitted
```

API Gap / Revision Proposal:

```text
If GET /api/v1/users does not support membership_status filter, propose additive filter support.

If PATCH /api/v1/users/{user_id} does not safely support membership transition, propose additive user status transition contract.

Do not create member approval service.
Do not create farm_memberships table.
```

### 21.4 Organizations Page

Route:

```text
/administration/organizations
```

Data source:

```text
GET /api/v1/organizations
GET /api/v1/organizations/{organization_id}
POST /api/v1/organizations if role allows
PATCH /api/v1/organizations/{organization_id} if role allows
```

Displayed fields:

```text
Organization Name
Organization ID
Type
Status
Created At
Farm Count if available
User Count if available
```

API Gap / Revision Proposal:

```text
Farm count and user count must not be assumed unless returned by backend.
If needed, propose additive summary fields.
```

---

## 22. Farm / Zone / Tree Management

### 22.1 Farm Management

Routes:

```text
/farms
/farms/[farmId]
```

APIs:

```text
GET /api/v1/farms
GET /api/v1/farms/{farm_id}
POST /api/v1/farms
PATCH /api/v1/farms/{farm_id}
```

Rules:

```text
Owner may create multiple farms under own organization if backend permits.
owner_family and farm_staff cannot create Farm / Zone / Tree.
Backend enforces authorization.
```

### 22.2 Zone Management

Embedded in:

```text
/farms/[farmId]
```

or route:

```text
/farms/[farmId]/zones
```

APIs:

```text
GET /api/v1/zones?farm_id={farm_id}
POST /api/v1/zones
PATCH /api/v1/zones/{zone_id}
```

Rules:

```text
Zone represents operational block context.
Do not create Block entity.
Do not create Block registry.
```

### 22.3 Tree Management

Embedded in:

```text
/farms/[farmId]
```

or route:

```text
/farms/[farmId]/trees
```

APIs:

```text
GET /api/v1/trees?zone_id={zone_id}
POST /api/v1/trees
PATCH /api/v1/trees/{tree_id}
```

Rules:

```text
Tree registration remains optional.
Tree identity supports notebook context.
```

### 22.4 QR / ID Display

Allowed:

```text
Display Farm ID
Display Zone ID
Display Tree ID
Generate QR payload visually from existing ID
Print QR label if useful
```

Example payloads:

```text
ari://farm/{farm_id}
ari://zone/{zone_id}
ari://tree/{tree_id}
```

Not allowed:

```text
qr_registry
QR entity
QR service boundary
QR database table
```

---

## 23. Notifications

Route:

```text
/notifications
```

Top bar:

```text
Notification icon with unread count if available
```

APIs:

```text
GET /api/v1/notifications
PATCH /api/v1/notifications/{notification_id}/read
POST /api/v1/notifications/mark-all-read
```

Filters:

```text
type
status
date_from
date_to
```

Notification types may include:

```text
upload_reminder
follow_up_reminder
upload_success
upload_failure
system
```

Actual values must follow frozen backend enum.

Actions:

```text
Open related notebook entry if entity reference is available
Open follow-up if linked
Mark read
Mark all read
```

API Gap / Revision Proposal:

```text
If notifications do not include target entity reference, Web can show message only.

If navigation to related entity is required, propose additive target fields.
```

---

## 24. Follow-ups

Route:

```text
/follow-ups
```

Purpose:

```text
Learning completion workflow
```

APIs:

```text
GET /api/v1/follow-ups
GET /api/v1/follow-ups/{follow_up_id}
POST /api/v1/follow-ups
PATCH /api/v1/follow-ups/{follow_up_id}
```

Views:

```text
Pending
Today
This Week
Overdue
Completed
```

Allowed follow-up periods:

```text
3 days
7 days
14 days
```

Allowed outcomes:

```text
improved
same
worse
unknown
```

Displayed fields:

```text
Follow-up ID
Notebook Entry
Farm context
Follow-up day
Due date if available
Outcome
Notes
Recorded At
Status
```

Actions:

```text
Open Notebook Entry
Record outcome
Update notes
Filter by farm
Filter by outcome
```

API Gap / Revision Proposal:

```text
If due date is not stored or returned, Web may compute approximate due date from created_at + follow_up_day for display only.

Backend remains source of truth for stored fields.
```

---

## 25. Search and Filters

### 25.1 Search Policy

Allowed P1-3 search:

```text
Keyword search
Filter search
Date filter
Farm filter
Zone filter
Tree filter
Entry type filter
Created by filter
Status filter
```

Forbidden in P1-3:

```text
Vector search
Semantic search
RAG search
LLM search
Knowledge graph search
```

### 25.2 Global Search

Top bar global search may route to:

```text
/notebook?q={keyword}
```

or:

```text
/search?q={keyword}
```

Implementation must use existing keyword search only.

### 25.3 Search Targets

Allowed if supported by existing APIs:

```text
Farms
Notebook Entries
Note Items text
Consultation entries
Follow-ups
Notifications
Users if admin scope
```

### 25.4 Search API

Preferred existing API:

```text
GET /api/v1/notebook-entries/search
```

Alternative:

```text
GET /api/v1/notebook-entries?q={keyword}
```

API Gap / Revision Proposal:

```text
If the frozen backend only supports one of the two patterns, P1-3 must use that pattern.

Do not invent a new search endpoint silently.
```

### 25.5 Filter State

Filters should be represented in URL query parameters:

```text
farm_id
zone_id
tree_id
entry_type
created_by_user_id
status
analysis_status
consultation_status
date_from
date_to
page
page_size
sort_by
sort_order
```

---

## 26. Error Handling UX

### 26.1 Standard Error Mapping

| HTTP Status | Web UX                                     |
| ----------: | ------------------------------------------ |
|         400 | Show invalid request message               |
|         401 | Attempt refresh; if failed, redirect login |
|         403 | Show forbidden / no access                 |
|         404 | Show not found                             |
|         409 | Show conflict message                      |
|         422 | Show field validation messages             |
|         500 | Show system error and retry option         |

### 26.2 Authentication Errors

Cases:

```text
Invalid phone or password
Token expired
Refresh failed
Logged out from another session if supported
```

UX:

```text
Show clear message
Do not expose backend internals
Return to login if required
```

### 26.3 Membership / Account Errors

Cases:

```text
pending_farm_approval
rejected
suspended
revoked
account blocked
```

UX:

```text
Show account status page
Explain current status
Disable unauthorized workspaces
Allow logout
Allow status refresh if backend permits
```

### 26.4 API Offline / Network Errors

Web App is not offline-first capture.

If network fails:

```text
Show connection error
Keep current page state if cached
Allow retry
Do not create offline notebook capture workflow in Web P1-3
```

### 26.5 Media Errors

Cases:

```text
Media URL expired
File missing
Unsupported media type
Forbidden media access
```

UX:

```text
Show media unavailable
Allow refresh URL if backend supports
Do not expose raw MinIO errors
```

### 26.6 Empty States

Required empty states:

```text
No farms found
No notebook entries found
No pending reviews
No knowledge candidates
No notifications
No follow-ups
No pending members
```

---

## 27. Security Implementation

### 27.1 Authorization

```text
All API calls must include Authorization header when authenticated.
Backend decides final authorization.
Web App must not trust UI role visibility as permission.
```

### 27.2 Token Security

```text
Never log access_token.
Never log refresh_token.
Never put token in URL.
Clear tokens on logout.
Refresh token only through approved endpoint.
```

### 27.3 Media Security

```text
Do not directly access MinIO.
Do not assume public bucket URLs.
Do not log presigned URLs.
Do not share media URLs outside authorized page context.
```

### 27.4 XSS / Input Safety

```text
Escape rendered text.
Sanitize external links.
Open external links in new tab with safe attributes.
Do not render raw HTML from notebook content unless sanitized.
```

### 27.5 Role and Status Safety

```text
Do not hard-code hidden admin behavior as security.
Do not expose admin routes to blocked users.
Do not allow pending_farm_approval users into farm-scoped workspaces.
```

### 27.6 Configuration Safety

```text
Do not commit production secrets.
Only expose public frontend env vars required by browser.
Backend secrets remain backend-only.
```

---

## 28. Configuration

### 28.1 Environments

```text
local
dev
staging
production
```

### 28.2 Required Environment Variables

```text
NEXT_PUBLIC_API_BASE_URL
NEXT_PUBLIC_API_VERSION
NEXT_PUBLIC_APP_ENV
NEXT_PUBLIC_DEFAULT_LANGUAGE
NEXT_PUBLIC_ENABLE_WEB_REGISTER
NEXT_PUBLIC_ENABLE_SIMULATOR_FILTER
NEXT_PUBLIC_ENABLE_QR_PRINT
NEXT_PUBLIC_PAGE_SIZE
```

Default values:

```text
NEXT_PUBLIC_API_VERSION=/api/v1
NEXT_PUBLIC_DEFAULT_LANGUAGE=th
NEXT_PUBLIC_ENABLE_WEB_REGISTER=false
NEXT_PUBLIC_ENABLE_SIMULATOR_FILTER=false
NEXT_PUBLIC_ENABLE_QR_PRINT=true
NEXT_PUBLIC_PAGE_SIZE=20
```

### 28.3 API Client Configuration

```text
API timeout
Retry once after token refresh
Do not retry unsafe mutation automatically unless idempotency is guaranteed
Handle standard response envelope
Handle pagination envelope
```

---

## 29. Testing Strategy

### 29.1 Unit Tests

Test:

```text
phone normalization display
auth session state
token refresh decision
RBAC navigation visibility
membership_status routing
account_status routing
API error mapping
pagination helper
filter query builder
date formatting
QR payload generation from Farm / Zone / Tree ID
```

### 29.2 Component Tests

Test:

```text
Login form
Dashboard cards
Farm table
Farm detail sections
Notebook filters
Notebook entry timeline
Media viewer
Consultation panel
Follow-up outcome form
Notification list
Approval queue table
Knowledge candidate table
Knowledge library view
User table
Pending member approval table
```

### 29.3 Integration Tests

Test:

```text
login → auth/me → dashboard
login pending_farm_approval → pending status page
token expired → refresh → retry request
farm list → farm detail
farm detail → notebook filter
notebook list → entry detail
entry detail → media viewer
consultation entry → learned_summary display
follow-up list → record outcome
notification read → mark read
admin → pending members → approve/reject if backend supports
```

### 29.4 E2E Tests

Test:

```text
phone login successful
invalid login
role-based navigation visibility
farmer scoped farm access
reviewer review queue access
admin user management access
forbidden route handling
notebook keyword search
farm filter + date filter
media viewer authorized display
logout clears session
```

### 29.5 Security Tests

Test:

```text
no token in URL
no token in console logs
403 renders forbidden page
pending user cannot access farm detail
blocked account cannot access dashboard
expired media URL handled safely
external link opens safely
```

---

## 30. Build and Deployment

### 30.1 Local Development

Required:

```text
npm install
npm run dev
```

or equivalent package manager commands approved by project repository.

Web local app should connect to:

```text
FastAPI backend /api/v1
```

### 30.2 Build

Required output:

```text
Production web build
```

Command example:

```text
npm run build
```

### 30.3 Deployment Target

Allowed deployment forms:

```text
Dockerized web app
Static/Node web deployment depending on Next.js mode
Reverse proxy behind HTTPS
```

### 30.4 Docker

P1-3 may include:

```text
web/Dockerfile
```

Do not create separate backend container for web.

### 30.5 Deployment Rules

```text
Use HTTPS in production.
Set correct API base URL.
Do not expose backend secrets.
Do not expose MinIO credentials.
Use backend-approved media access only.
```

### 30.6 Browser Support

Required:

```text
Modern Chrome
Modern Edge
Modern Firefox
Modern Safari
```

Target use:

```text
Desktop and notebook browsers
```

---

## 31. Required Checklist

Before P1-3 coding starts:

```text
[ ] Browser-based Web App confirmed.
[ ] No native desktop app.
[ ] No Electron app.
[ ] No Flutter desktop app.
[ ] Web project lives under web/.
[ ] One Web App only.
[ ] Uses existing /api/v1 backend.
[ ] No separate web backend.
[ ] Phone-number login defined.
[ ] POST /api/v1/auth/login used.
[ ] GET /api/v1/auth/me used.
[ ] POST /api/v1/auth/refresh used.
[ ] POST /api/v1/auth/logout used.
[ ] Web registration disabled by default unless approved.
[ ] If registration enabled, POST /api/v1/auth/register reused.
[ ] Existing RBAC roles used exactly.
[ ] farmer_status not treated as RBAC role.
[ ] membership_status handled in routing.
[ ] account_status handled in routing.
[ ] RBAC navigation visibility defined.
[ ] Backend remains authorization source of truth.
[ ] Dashboard implemented as Work Queue.
[ ] Farm List page defined.
[ ] Farm Detail page defined.
[ ] Farm Notebook page defined.
[ ] Notebook Entry Detail page defined.
[ ] Media Viewer defined.
[ ] Consultation display uses entry_type=consultation.
[ ] No consultation entity introduced.
[ ] Approval Queue uses notebook entries and statuses.
[ ] No reviews table introduced.
[ ] Knowledge Candidate is UI/status workflow only.
[ ] No knowledge_candidate table introduced.
[ ] Knowledge Library is basic view over approved notebook entries only.
[ ] No Knowledge Graph.
[ ] No Vector DB.
[ ] No RAG.
[ ] User / Organization management uses existing APIs.
[ ] Pending member approval uses users + membership_status only if backend supports.
[ ] No farm_memberships table introduced.
[ ] Farm / Zone / Tree management uses existing APIs.
[ ] QR display generated from existing IDs only.
[ ] No qr_registry.
[ ] Notifications use existing notification APIs.
[ ] Follow-ups use existing follow-up APIs.
[ ] Search is keyword/filter only.
[ ] No semantic / vector / LLM search.
[ ] Media access does not bypass backend.
[ ] Error handling UX defined.
[ ] Security handling defined.
[ ] Environment configuration defined.
[ ] Testing strategy defined.
[ ] Build and deployment defined.
```

---

## 32. API Gap / Revision Proposal

The following items may require backend/API confirmation before full implementation.

### 32.1 Web Registration

```text
Gap:
P1-3 default disables Web registration.

Revision Proposal:
If Owner wants browser-based registration, Web must reuse POST /api/v1/auth/register and the same phone/farmer_status/membership_status contract from P1-2.
```

### 32.2 Current User Additive Fields

```text
Gap:
GET /api/v1/auth/me must return farmer_status, membership_status, account_status, primary_farm_id for correct Web routing.

Revision Proposal:
Add these fields to /auth/me response if missing.
```

### 32.3 Pending Member Approval Filters

```text
Gap:
Pending member view requires filtering users by membership_status.

Revision Proposal:
Add membership_status, farmer_status, primary_farm_id filters to GET /api/v1/users if missing.
```

### 32.4 Membership Status Transition

```text
Gap:
Approval/rejection requires safe user membership transition.

Revision Proposal:
Use PATCH /api/v1/users/{user_id} if already approved.
If not, define additive transition behavior without creating approval service or farm_memberships table.
```

### 32.5 Review Status Update

```text
Gap:
Approval Queue requires notebook entry review status updates.

Revision Proposal:
Use existing notebook entry update endpoint if available.
If missing, add additive PATCH support for approved notebook entry status fields.
Do not create reviews table.
```

### 32.6 Knowledge Candidate State

```text
Gap:
Knowledge Candidate requires an approved representation using existing notebook entry fields.

Revision Proposal:
Use existing analysis_status/status if available.
If missing, add additive enum value or status field to notebook_entries.
Do not create knowledge table.
```

### 32.7 Media Read URL

```text
Gap:
Media viewer requires authorized media read access.

Revision Proposal:
Backend returns approved media URL or provides authorized read URL endpoint.
Do not access MinIO directly.
```

### 32.8 Dashboard Aggregates

```text
Gap:
Dashboard cards may require counts.

Revision Proposal:
Use existing list endpoints initially.
Add summary endpoint later only if performance requires it.
```

---

## 33. Non-Goals

P1-3 must not implement:

```text
Mobile App implementation
Native desktop app
Electron app
Flutter desktop app
Separate admin backend
Separate web backend
Separate farmer web app
Separate staff web app
Internal AI Assistant
Knowledge Graph
Vector Database
RAG
Agent Orchestration
Commerce
Robot Control
Irrigation Control
Fertilizer Control
Advanced AI Disease Diagnosis
Automatic Treatment Recommendation
Permission Service
Permission Matrix Engine
New RBAC Role
New Database Architecture
QR Registry
Consultation Entity
Owner Registry
Farmer Registry
Member Registry
Block Registry
Farm Membership Table
Case Library Entity
Knowledge Asset Entity
Audit Log API
Advanced GIS Boundary Mapping
Semantic Search
LLM Search
```

---

## 34. Freeze Boundary

After P1-3 Freeze:

```text
No web UX redesign without revision
No new web app
No separate admin app
No desktop app scope
No new backend service
No new database architecture
No new domain entity
No new RBAC role
No permission service
No qr_registry
No consultation entity
No knowledge service
No vector search
No RAG
No internal AI assistant
No commerce module
No robot module
```

Any change must go through:

```text
Revision Proposal
↓
Review
↓
Owner Approval
↓
New Version
```

### 34.1 Final Statement

ARI V1 — P1-3 Web App Implementation Specification v1.0 defines how to implement the ARI browser-based Web App for deep-work activities.

It implements:

```text
Phone-number login
Current user restore
Token handling
RBAC-based navigation visibility
Dashboard work queue
Farm list
Farm detail
Farm notebook
Notebook entry detail
Media review
Consultation display
Follow-up display
Notifications
Approval queue as notebook workflow
Knowledge Candidate as notebook workflow
Basic Knowledge Library view over approved notebook records
User / Organization management
Pending member approval view if backend supports
Farm / Zone / Tree management
QR / ID representation display
Keyword and filter search
Error handling
Security handling
Testing
Build and deployment
```

It preserves:

```text
One Platform
One Backend
One Database Architecture
One Mobile App
One Web App
One Domain Model
One RBAC System
```

It does not implement:

```text
Desktop App
Separate Admin App
Permission Service
QR Registry
Consultation Entity
Knowledge Graph
Vector DB
RAG
Internal AI
Commerce
Robot Control
Irrigation
Fertilizer
Advanced AI Diagnosis
```

Recommended final status after Owner approval:

```text
Status: FROZEN
Freeze Date: <Owner approval date>
```

End of Document.


*********************************
include Additive revision patch
*********************************

## Additive Revision Patch — P1-3 Web App Implementation Specification v1.0

### A. Small Prototype / Real Pilot First Principle

P1-3 Web App implementation must support a small real-world prototype before full-scale rollout.

The purpose of the first Web App implementation is not to complete every future ARI capability.

The purpose is to support:

```text
Small pilot operation
Real farm data review
Notebook review
Media review
Consultation review
Follow-up review
Farm / Zone / Tree context organization
User / membership approval support
Knowledge candidate identification
Learning from real usage
```

The Web App must help the ARI team collect enough real usage evidence to improve the next phase.

This follows the ARI progressive adoption principle:

```text
Build small
Use with real users
Collect evidence
Review problems
Improve workflow
Revise specification
Then expand phase-by-phase
```

#### Prototype Boundary

The P1-3 prototype must remain inside the frozen architecture.

It must use:

```text
Existing Organization
Existing User
Existing Farm
Existing Zone
Existing Tree
Existing Notebook Entry
Existing Note Item
Existing Follow-Up
Existing Notification
Existing /api/v1 backend
Existing RBAC roles
```

It must not create:

```text
Temporary Farm Entity
Survey Farm Entity
Field Collection Entity
Simulator Entity
Owner Registry
Farmer Registry
Member Registry
Block Registry
Permission Service
Separate Web Backend
Separate ARI Staff App
Separate Farmer App
```

#### Prototype Success Criteria

The first small prototype is considered successful if ARI can:

```text
Register / login users by phone
Create or select farms
Capture real farm notes from mobile
Upload photo / video / voice / text evidence
Review notebook entries from web
Review consultation entries from web
Record follow-up outcomes
Find records using keyword / filters
Identify useful knowledge candidates
Manage basic farm / zone / tree context
Approve or review pending members if backend supports
Separate simulator/test data from real pilot data
```

---

### B. Search Workspace

#### Purpose

Search Workspace is the central Web App workspace for finding existing ARI records using keyword search and filters.

Search Workspace is not an AI search system.

It is not:

```text
Vector Search
Semantic Search
RAG Search
LLM Search
Knowledge Graph Search
```

#### Route

```text
/search
```

#### Allowed Search Targets

Search Workspace may search or filter existing records that the current user is allowed to access:

```text
Farms
Zones
Trees
Notebook Entries
Note Items text
Consultation entries
Follow-ups
Notifications
Users if current role allows
Media metadata if backend returns it
```

Consultation entries are searched through:

```text
Notebook Entry where entry_type = consultation
```

Do not create a consultation entity or consultation search service.

#### Allowed Search Methods

P1-3 supports:

```text
Keyword search
Farm filter
Zone filter
Tree filter
Entry type filter
Created by filter
Status filter
Date range filter
Follow-up outcome filter
Consultation status filter if backend supports
```

#### API Dependency

Use existing API patterns only:

```text
GET /api/v1/notebook-entries?q={keyword}
GET /api/v1/notebook-entries?farm_id={farm_id}
GET /api/v1/notebook-entries?entry_type=consultation
GET /api/v1/farms?q={keyword}
GET /api/v1/users?... if role allows
GET /api/v1/follow-ups?...
GET /api/v1/notifications?...
```

If the frozen backend supports:

```text
GET /api/v1/notebook-entries/search
```

then Web may use it.

Do not invent a new search endpoint silently.

#### API Gap / Revision Proposal

If required search filters are missing, propose additive filter support only.

Example:

```text
API Gap / Revision Proposal:
Add keyword/filter parameters to existing list endpoints.

Do not add:
  Vector search endpoint
  Semantic search endpoint
  RAG endpoint
  Knowledge graph search endpoint
```

---

### C. Simulator Workspace

#### Purpose

Simulator Workspace supports:

```text
Testing
Training
Demo
Workflow validation
Pilot preparation
Dataset creation
ARI staff practice
Mobile/Web workflow testing
```

Simulator Workspace allows ARI staff to test ARI workflows before or alongside real pilot farms.

#### Route

```text
/simulator
```

#### Meaning

Simulator Workspace may include simulator organization/farm records created under the existing ARI data model.

Example:

```text
Organization:
  ARI Internal Organization
  ARI Simulator Organization

Farm:
  SIM-001
  SIM-DURIAN
  SIM-MANGO
  SIM-TEST

Zone:
  SIM-ZONE-A
  SIM-ZONE-B

Tree:
  SIM-TREE-001
```

#### ARI Staff Simulated Owner Use Case

ARI staff may use simulator organization/farm records to behave like a farm owner for testing.

This may include:

```text
Login through mobile app
Use farmer_status = owner for test user if allowed
Create simulator farm
Create simulator zone
Create simulator tree
Capture notes
Upload media
Create consultation entry
Record learned summary
Record follow-up
Review the data in Web App
Promote useful records as knowledge candidate if supported
```

This is allowed only as a simulator/test workflow.

It does not create:

```text
Owner Registry
Simulator Entity
Temporary Farm Entity
Field Collection Entity
Separate Staff App
Separate Backend
```

#### Real Field Collection During Early Prototype

If ARI staff visits real farms before full onboarding is ready, they may record field data under an ARI-managed simulator or internal pilot farm context.

Recommended rule:

```text
Use existing Organization / Farm / Zone / Tree records.
Mark or identify the farm as simulator/pilot if backend supports.
Keep simulator/test data separated from production data.
```

If data is collected from a real farm but ownership/approval is not finalized, the record should be treated as:

```text
Unverified / Needs Human Review
```

Do not create:

```text
Survey Farm Entity
Temporary Farm Entity
Field Visit Entity
Production Farm Conversion Workflow
```

Any later conversion from simulator/pilot farm data into production farm data must be handled as:

```text
Future Enhancement / Revision Proposal
```

#### Simulator Separation Rule

Simulator data must be logically separated from production/pilot data.

Simulator data must not appear in production reports by default.

Simulator data must not be mixed into real farm knowledge results unless explicitly included by an authorized user.

#### API Dependency

Preferred existing/additive support:

```text
GET /api/v1/farms?is_simulator=true
GET /api/v1/notebook-entries?is_simulator=true
```

If backend does not support `is_simulator`, P1-3 may use naming convention for prototype only:

```text
SIM-001
SIM-DURIAN
SIM-MANGO
SIM-TEST
```

Naming convention is only a prototype fallback.

It is not a replacement for backend-supported simulator flag.

#### API Gap / Revision Proposal

```text
API Gap / Revision Proposal:
Add additive is_simulator filter support to Farm and Notebook Entry list APIs if not already supported.

Do not add:
  simulator table
  simulator service
  simulator entity
  temporary farm entity
```

---

### D. Identity / QR Mapping Clarification

P1-3 must clarify identity terms from earlier UX documents so developers do not create new entities.

#### Owner ID

Owner ID must not become a new entity.

Implementation rule:

```text
Owner context = User + Organization context
```

Do not create:

```text
Owner Registry
Owner API
Owner Table
```

#### Block ID

Block ID must not become a new entity.

Implementation rule:

```text
Block = Zone
```

Do not create:

```text
Block Registry
Block API
Block Table
```

#### Farm ID / Zone ID / Tree ID

Farm ID, Zone ID, and Tree ID are existing identifiers from the existing backend/domain model.

The Web App may display:

```text
Farm ID
Zone ID
Tree ID
```

The Web App may generate QR images from these existing IDs for printing or display.

#### QR Rule

QR is representation only.

The Web App may generate QR payloads such as:

```text
ari://farm/{farm_id}
ari://zone/{zone_id}
ari://tree/{tree_id}
```

Do not create:

```text
qr_registry
QR entity
QR service
QR table
```

---

### E. Knowledge Workspace Boundary Strengthening

P1-3 Knowledge Workspace is a UI workflow over existing Notebook Entries.

It is not a new knowledge system.

Allowed:

```text
Knowledge Candidate view
Basic Knowledge Library view
Approved notebook entries
Consultation outcome review
Follow-up outcome review
Evidence timeline review
Keyword/filter search
Manual human review
```

Not allowed in P1-3:

```text
Knowledge Article entity
Knowledge Asset entity
Case Library entity
Knowledge Relationship table
Knowledge Graph
Vector Database
RAG
LLM Search
Knowledge API
Versioned knowledge publishing system
```

If the project later needs true knowledge articles, case library, confidence score, versioning, or relationship graph, those must be created as:

```text
Future Enhancement / Revision Proposal
```

---

### F. Pending Member Approval Boundary

Pending member approval in P1-3 must use the existing User model and membership_status only.

Allowed:

```text
GET /api/v1/users?membership_status=pending_farm_approval
PATCH /api/v1/users/{user_id}
```

Allowed status transitions if backend supports:

```text
pending_farm_approval → active
pending_farm_approval → rejected
active → suspended
active → revoked
suspended → active
```

Authority:

```text
admin
root
ari_staff if explicitly permitted by backend/RBAC
```

Owner self-approval is not implemented in P1-3 unless a later approved API/RBAC revision explicitly allows it.

Do not create:

```text
farm_memberships
join_requests
approval_service
member_registry
permission_service
```

If owner-managed approval is required later, it must be handled as:

```text
Future Enhancement / Revision Proposal
```

---

### G. Updated Freeze Readiness Statement

After this additive patch is applied, P1-3 Web App Implementation Specification v1.0 may be considered ready for freeze review if the Owner accepts the following implementation position:

```text
P1-3 Web App v1.0 is a small real-world prototype implementation.

It supports:
  Work Deep
  Review
  Manage
  Approve
  Search
  Simulator testing
  Notebook review
  Media review
  Consultation review
  Follow-up review
  Basic knowledge candidate workflow
  User / organization / farm context management

It does not attempt to implement the full future ARI intelligence platform.

The prototype will be used with real pilot data first.
After enough data is collected, ARI will review actual usage, problems, missing workflows, and data quality before designing the next phase.
```

Recommended status after Owner approval:

```text
Status: FROZEN
Freeze Boundary:
  Small Prototype / Real Pilot First
  Browser-based Web App only
  Existing backend/API only
  Existing domain/database only
  Existing RBAC only
```
****************************************

ARI V1 — P1-3 Web App Implementation Specification v1.0
Status: FROZEN
Freeze State: Approved by Owner
Freeze Date: 2026-06-19

ถือว่าเอกสาร #P1-3 Web App Implementation Specification v1.0 เสร็จสมบูรณ์และ Freeze แล้ว

โดย Freeze รวม patch ล่าสุดแล้ว:

1. Search Workspace
2. Simulator Workspace
3. Identity / QR Mapping
4. Knowledge Workspace Boundary
5. Pending Member Approval Boundary
6. Small Prototype / Real Pilot First Principle

Frozen Scope หลัก:

Browser-based Web App only
No native desktop app
No Electron app
No Flutter desktop app
Use existing /api/v1 backend
Use existing database/domain/RBAC
Support small prototype / real pilot first

หลังจากนี้ ถ้ามีการเปลี่ยนแปลง P1-3 ต้องแยกเป็น:

Revision Proposal
Optional Extension
Future Enhancement

ไม่แก้ Frozen document โดยตรงครับ.
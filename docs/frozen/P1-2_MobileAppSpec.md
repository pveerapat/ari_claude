# ARI V1 — P1-2 Mobile App Implementation Specification v1.0

## 1. Document Control

Project: ARI — Agricultural Intelligence Platform

Document Title: ARI V1 — P1-2 Mobile App Implementation Specification v1.0

Version: v1.0

Status: Draft Final / Ready for Freeze

Freeze Readiness: Ready for Owner Freeze Approval

Scope: Flutter Mobile App Implementation Specification

Target Platforms:

```text
Android
iOS
```

This document defines how to implement the ARI mobile app using Flutter.

This document does not redesign:

```text
ARI Architecture
Backend Architecture
Database Architecture
Core Domain Model
RBAC Role List
Mobile UX Principles
Web App Scope
Desktop App Scope
```

### 1.1 Source of Truth

This document follows the frozen and approved ARI documents:

```text
#44 Farm AI Operating System
#45 Software Architecture & Monorepo Specification Rev2.0
#46 MVP Software Build Plan
#46A Mobile App UX Flow & Screen Specification
#46B Web App UX Flow & Screen Specification
#47 AI Agent Development Workflow Framework
ARI V1 — P0 Domain Model Specification v1.0
ARI V1 — P0 Database Schema Specification v1.0
ARI V1 — P0 API Specification v1.0
ARI V1 — P1-1 Backend Implementation Specification v1.0
```

### 1.2 Dependency Status

Dependency status for this P1-2 freeze review:

```text
P0 Domain Model Additive Revision: Confirmed
P0 Database Schema Additive Revision: Confirmed
P0 API Additive Revision: Confirmed
P1-1 Backend Additive Revision: Confirmed
```

### 1.3 Frozen Baseline Dependencies

The following frozen baseline decisions remain unchanged:

```text
One Platform
One Backend
One Database Architecture
One Mobile App
One Web App
One Domain Model
One RBAC System

organization_id required
farm_id nullable
zone_id nullable
tree_id nullable

Notebook Entry = Note Session
Note Item = Timeline Item
Consultation = Notebook Entry Type
QR = Representation, not Entity
RBAC = Backend Dependency Guards
No Permission Service
Save Local ≠ Upload ≠ Analyze
Offline First
Capture First
Structure Later
```

### 1.4 Owner-Approved Mobile Onboarding Decisions

The following Owner-approved decisions are supported by the approved additive revisions to P0 Domain Model, P0 Database Schema, P0 API, and P1-1 Backend, and are included as part of P1-2 Mobile implementation scope:

```text
Mobile self-registration
Phone-number login
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
Owner registration creates or assigns organization_id
Owner may create multiple farms
Owner's Family / Farm Staff join by Farm ID, not Owner ID
First-time permission setup after registration/login
Create Farm location auto-fill from phone GPS
Android/iOS only in P1-2
Web App moved to P1-3
Desktop App out of scope
```

These decisions must not create:

```text
Separate platform
Separate mobile app
New RBAC role
Permission service
Owner registry
QR registry
Consultation entity
New database architecture
```

---

## 2. Implementation Boundary

### 2.1 P1-2 Required

P1-2 covers:

```text
Flutter project structure
Android/iOS mobile app implementation
Mobile registration and login flow
Phone-number login
Farmer status selection
Owner onboarding
Farm join policy
Farm creation
Zone and Tree creation if allowed
First-time permission setup
Authentication state
RBAC visibility
Offline local storage
Offline capture
Upload queue
Offline sync
File upload via backend presigned URL
Media capture
Ask AI external consultation workflow
Farm Notebook
Notifications
Follow-ups
QR scan as representation only
Error handling
Security handling
Configuration
Testing
Android/iOS build and release
```

### 2.2 P1-2 Optional Extension

Optional extensions may be added only if they do not require architecture redesign or new core entities:

```text
QR scan helper UI
QR display from existing Farm / Zone / Tree ID
Share-to-ARI from external apps
Media thumbnail preview
Wi-Fi-only upload option
Local-only draft export
Basic upload progress notification
```

### 2.3 Future Enhancement

The following are not part of P1-2:

```text
Internal AI Assistant
Knowledge Graph
Vector Database
RAG
Agent Orchestration
Commerce
Robot Control
Irrigation Control
Fertilizer Control
Audit System
Fine-grained Permission Service
Semantic Search
LLM Search
Advanced AI Media Processing
OTP / SMS verification
Invite link
Password reset
Forced password change
Owner-managed member approval screen
Multi-farm membership table
macOS Desktop App
Ubuntu Desktop App
Windows Desktop App
Web App Implementation
```

### 2.4 Non-Goals

P1-2 must not introduce:

```text
New mobile UX redesign
Separate Farmer App
Separate Staff App
New backend service
New database architecture
New domain model
New RBAC role
Permission service
Permission matrix engine
QR Registry
Consultation Entity
Owner Registry
Block Registry
Knowledge Module
Robot Module
Commerce Module
Desktop App
Web App
```

---

## 3. Mobile App Principle

ARI Mobile must preserve:

```text
One Mobile App
No Separate Farmer App
No Separate ARI Staff App
Role-Based Access Control
Offline First
Capture First
Simple Home Screen
Evidence First
Human-in-the-Loop
Progressive Adoption
Structure Later
```

The user should think only:

```text
Ask
Record
Review
Learn
```

### 3.1 Save Local Principle

Mobile must always preserve:

```text
Save Local
≠
Upload
≠
Analyze
```

Meaning:

```text
Capture can happen offline.
Local save must happen before upload.
Upload can happen later.
Analysis is not required for local capture.
```

---

## 4. Technology Stack

### 4.1 Mobile Framework

```text
Flutter
```

### 4.2 Target Platforms

```text
Android
iOS
```

### 4.3 Out of Scope Platforms

```text
macOS Desktop App
Ubuntu Desktop App
Windows Desktop App
Web App
```

Notebook / PC / desktop browser access will be handled later in:

```text
P1-3 Web App Implementation Specification
```

### 4.4 Backend API

```text
FastAPI REST API
/api/v1
```

### 4.5 Authentication

```text
JWT Access Token
Refresh Token
Phone-number login
```

### 4.6 Local Storage

```text
Local mobile database
Secure token storage
Local media file storage
Offline queue
Upload queue
Cached user/session/farm context
```

### 4.7 Media

Supported media:

```text
Photo
Video
Voice
Text
File
Link
Existing Media
```

### 4.8 Upload

```text
MinIO Presigned Upload via Backend API
```

Frozen upload endpoints:

```text
POST /api/v1/files/upload-url
POST /api/v1/files/complete
```

### 4.9 Sync

```text
client_id
device_id
client_batch_id
POST /api/v1/sync/batch
upload_queue
```

---

## 5. Flutter Project Structure

The mobile app must live under:

```text
mobile/
```

There must be only one Flutter app.

Required structure:

```text
mobile/
├── pubspec.yaml
├── analysis_options.yaml
├── README.md
├── lib/
│   ├── main.dart
│   ├── app.dart
│   ├── core/
│   │   ├── config/
│   │   │   ├── app_config.dart
│   │   │   ├── environment.dart
│   │   │   └── constants.dart
│   │   ├── auth/
│   │   │   ├── token_store.dart
│   │   │   ├── auth_interceptor.dart
│   │   │   └── session_manager.dart
│   │   ├── network/
│   │   │   ├── api_client.dart
│   │   │   ├── api_error.dart
│   │   │   └── connectivity_service.dart
│   │   ├── storage/
│   │   │   ├── local_database.dart
│   │   │   ├── secure_storage.dart
│   │   │   └── media_storage.dart
│   │   ├── sync/
│   │   │   ├── sync_batch_builder.dart
│   │   │   ├── sync_service.dart
│   │   │   └── upload_worker.dart
│   │   ├── utils/
│   │   │   ├── uuid_generator.dart
│   │   │   ├── checksum_util.dart
│   │   │   ├── datetime_util.dart
│   │   │   └── file_util.dart
│   │   └── errors/
│   │       └── app_error.dart
│   ├── shared/
│   │   ├── widgets/
│   │   ├── models/
│   │   ├── providers/
│   │   └── utils/
│   ├── features/
│   │   ├── auth/
│   │   │   ├── data/
│   │   │   ├── domain/
│   │   │   └── presentation/
│   │   ├── onboarding/
│   │   │   ├── data/
│   │   │   ├── domain/
│   │   │   └── presentation/
│   │   ├── home/
│   │   │   └── presentation/
│   │   ├── farm_context/
│   │   │   ├── data/
│   │   │   ├── domain/
│   │   │   └── presentation/
│   │   ├── farm_setup/
│   │   │   ├── data/
│   │   │   ├── domain/
│   │   │   └── presentation/
│   │   ├── notebook/
│   │   │   ├── data/
│   │   │   ├── domain/
│   │   │   └── presentation/
│   │   ├── ask_ai/
│   │   │   ├── data/
│   │   │   ├── domain/
│   │   │   └── presentation/
│   │   ├── media_capture/
│   │   │   ├── data/
│   │   │   ├── services/
│   │   │   └── presentation/
│   │   ├── notifications/
│   │   │   ├── data/
│   │   │   ├── domain/
│   │   │   └── presentation/
│   │   ├── follow_ups/
│   │   │   ├── data/
│   │   │   ├── domain/
│   │   │   └── presentation/
│   │   ├── qr/
│   │   │   ├── data/
│   │   │   └── presentation/
│   │   ├── upload_queue/
│   │   │   ├── data/
│   │   │   ├── services/
│   │   │   └── presentation/
│   │   └── profile/
│   │       ├── data/
│   │       └── presentation/
│   └── generated/
├── test/
│   ├── unit/
│   ├── widget/
│   ├── integration/
│   ├── auth/
│   ├── onboarding/
│   ├── offline_sync/
│   ├── upload_flow/
│   └── navigation/
├── android/
└── ios/
```

Forbidden structures:

```text
farmer_app/
staff_app/
desktop_app/
web_app/
permission_engine/
qr_registry_module/
consultation_entity_module/
knowledge_module/
robot_module/
commerce_module/
```

---

## 6. App Architecture

Use simple layered Flutter architecture:

```text
Presentation Layer
State Management Layer
Application / Service Layer
Repository Layer
Local Storage Layer
Remote API Layer
```

### 6.1 Presentation Layer

Responsible for:

```text
Screens
Widgets
Forms
Navigation
User interaction
Local validation messages
Upload/sync state display
Permission explanation
Offline status display
```

Must not:

```text
Call REST APIs directly
Write directly to local database
Act as permission authority
Implement backend business rules
```

### 6.2 State Management Layer

Recommended approach:

```text
ChangeNotifier-based providers
```

Track:

```text
Authentication state
Registration state
Farmer status state
Active farm context
Offline queue state
Upload queue state
Notebook draft state
Notification state
Follow-up state
Permission state
```

### 6.3 Application / Service Layer

Responsible for:

```text
Registration flow orchestration
Login flow orchestration
Permission setup orchestration
Farm setup flow
Draft save flow
Capture flow
Sync flow
Upload flow
Follow-up scheduling
Notification scheduling
External AI handoff flow
```

### 6.4 Repository Layer

Responsible for:

```text
Read/write local records
Call remote API client
Map local model to API DTO
Map API response to local model
Maintain server_id mapping
```

### 6.5 Local Storage Layer

Responsible for:

```text
Draft notebook entries
Draft note items
Local media paths
Upload queue
Sync queue
Device ID
Client IDs
Active farm context
Cached farm/zone/tree lists
Cached user/session data
Notification cache
Follow-up cache
```

### 6.6 Remote API Layer

Responsible for calling frozen or revised `/api/v1` APIs.

No feature may require a separate backend.

---

## 7. Account Registration and Phone Login

### 7.1 Backend/API Dependency

This section uses the approved P0 API / P1-1 Backend additive revision contracts for:

```text
Mobile self-registration
Phone-number login
farmer_status
membership_status
account_status
primary_farm_id
Farm ID join behavior
Owner organization assignment
```

P1-2 mobile must use those approved contracts consistently.

### 7.2 Login ID Rule

The mobile phone number is the platform-wide login ID.

```text
login_id = phone number
```

The same phone number should be usable for:

```text
Android App
iOS App
Future Web App in P1-3
```

### 7.3 Phone Normalization

Mobile must normalize phone number before submitting.

Acceptable format must follow the approved backend/API rule.

Recommended display examples:

```text
0812345678
+66812345678
```

Rules:

```text
Phone number must be unique.
Phone number must be validated by backend.
Mobile must use same phone format for registration and login.
```

### 7.4 Registration Screen

Purpose:

```text
Allow new users to register from mobile app.
```

Required fields:

```text
Phone number
Name
Password
Farmer status
```

Farmer status must be single choice, not checkbox:

```text
( ) Owner / เจ้าของสวน
( ) Owner's Family / คนในครอบครัวเจ้าของสวน
( ) Farm Staff / คนงานหรือพนักงานสวน
```

If status is `owner_family` or `farm_staff`, require:

```text
Farm ID
```

Optional fields:

```text
Relationship note
Known owner name
Additional note
```

### 7.5 Default Password Policy

For P0 pilot simplicity, default password may be:

```text
1234
```

Rules:

```text
Default password is allowed only for P0 pilot.
Backend must store only password_hash.
Mobile must not store password in plain local database.
Mobile must not log password.
Production should replace this with OTP, invite link, or stronger password policy.
```

Recommended but not required for P1-2:

```text
After first successful login, app should encourage user to change password.
```

### 7.6 Registration API

Approved API:

```text
POST /api/v1/auth/register
```

Required request fields:

```text
phone
name
password
farmer_status
farm_id if farmer_status = owner_family or farm_staff
```

Expected backend behavior:

```text
Create user_id
Validate phone uniqueness
Assign role = farmer
Store password_hash
Assign status / membership_status based on farmer_status
Return authentication result or require login
```

This must not create:

```text
member_registry
farmer_registry
owner_registry
separate farmer account table
separate authentication service
```

---

## 8. Farmer Status Policy

### 8.1 Role vs Status

Do not create new RBAC roles.

Use existing role:

```text
role = farmer
```

Add farmer status:

```text
farmer_status = owner
farmer_status = owner_family
farmer_status = farm_staff
```

### 8.2 Backend/API Dependency

`farmer_status` must be persisted and returned by the approved backend/API contract.

Approved minimal additive field:

```text
users.farmer_status nullable
```

or equivalent approved storage in the existing user/profile model.

This is supported by the approved additive DB/API revision and must be used consistently by mobile.

### 8.3 Owner

Owner means:

```text
Actual farm owner or primary responsible person.
```

Owner can:

```text
Register by phone number
Receive or create organization_id
Create multiple farms under own organization
Create zones under own farms
Create trees under own zones if desired
Create notebook entries
Use Ask AI
View own farm notebook
```

Owner cannot:

```text
Access other organizations
Create admin/root/ari_staff users
Bypass backend authorization
```

### 8.4 Owner's Family

Owner's Family means:

```text
Family member of farm owner.
```

Must register with:

```text
Farm ID
```

Can:

```text
Register by phone number
Request to join farm
Create notebook entries after approval
Use Ask AI after approval if allowed
View farm data within approved scope
```

Cannot:

```text
Create Farm ID
Create Zone ID
Create Tree ID
Manage users
Change owner
Access unapproved farms
```

### 8.5 Farm Staff

Farm Staff means:

```text
Worker or staff member working at a farm.
```

Must register with:

```text
Farm ID
```

Can:

```text
Register by phone number
Request to join farm
Create notebook entries after approval
Capture photo/video/voice/text/file/link after approval
Use Ask AI if allowed
```

Cannot:

```text
Create Organization
Create Farm ID
Create Zone ID
Create Tree ID
Manage users
Change owner
Access unapproved farms
```

---

## 9. Owner Registration and Organization Assignment

### 9.1 Owner Registration Flow

```text
User installs app
↓
Tap Register
↓
Enter phone number
↓
Enter name
↓
Enter password
↓
Select farmer_status = owner
↓
Submit while internet is available
↓
Backend creates user_id
↓
Backend creates or assigns organization_id
↓
Backend returns registration result
↓
Mobile stores authenticated session
↓
Mobile opens Permission Setup
↓
Mobile opens Create Farm flow
```

### 9.2 Organization Rule

Because `organization_id` is required for ARI records, backend creates or assigns `organization_id` immediately after owner registration.

Approved policy:

```text
Owner registration creates/assigns organization_id immediately.
Account may be marked active_pending_verification or pending_review.
Admin can suspend/revoke later if registration is false.
```

Avoid:

```text
Owner waits without organization_id
```

because without `organization_id`, mobile cannot create properly scoped records.

### 9.3 Owner Verification / False Registration

If a user falsely registers as owner:

```text
Admin can suspend, reject, revoke, or deactivate the account.
Backend controls account status.
Mobile only displays resulting status.
```

Allowed statuses:

```text
active
active_pending_verification
pending_review
suspended
rejected
revoked
```

P1-2 mobile must display meaningful messages for suspended/rejected/revoked accounts.

---

## 10. Farm Join Policy for Owner's Family and Farm Staff

### 10.1 Join Reference

Owner's Family and Farm Staff must join by:

```text
Farm ID
```

not:

```text
Owner ID
```

Reason:

```text
One owner may have multiple farms.
Owner ID alone does not identify which farm the member belongs to.
Farm ID identifies the exact farm.
```

### 10.2 Family / Staff Registration Flow

```text
User installs app
↓
Tap Register
↓
Enter phone number
↓
Enter name
↓
Enter password
↓
Select farmer_status = owner_family or farm_staff
↓
Enter Farm ID
↓
Submit while internet is available
↓
Backend validates Farm ID exists
↓
Backend creates user_id
↓
Backend links request to Farm ID
↓
membership_status = pending_farm_approval
↓
Mobile shows pending approval message
```

### 10.3 Pending Approval Message

English:

```text
Your request has been sent.
Waiting for farm owner or admin approval.
```

Thai:

```text
ส่งคำขอเข้าร่วมสวนแล้ว
กรุณารอเจ้าของสวนหรือผู้ดูแลระบบอนุมัติ
```

### 10.4 Membership Status

Backend/API supports:

```text
pending_farm_approval
active
rejected
suspended
revoked
```

### 10.5 Minimal P1-2 Membership Storage

Approved minimal P1-2 backend dependency:

```text
users.primary_farm_id nullable
users.membership_status nullable
```

Used for:

```text
owner_family
farm_staff
```

This avoids adding a `farm_memberships` table in P1-2.

### 10.6 Future Membership Enhancement

Future enhancement:

```text
farm_memberships table
multi-farm membership
owner-managed member approval screen
invite code
member permission settings
```

These are not part of P1-2.

### 10.7 Approval Responsibility

P1-2 minimal policy:

```text
Admin / ARI Staff handles approval through backend/admin workflow.
Owner self-approval screen is Future Enhancement unless separately approved.
```

Mobile must not implement a full member-management system in P1-2.

---

## 11. Authentication Implementation

### 11.1 Login

API:

```text
POST /api/v1/auth/login
```

P1-2 mobile login uses:

```text
phone number + password
```

Mobile flow:

```text
User enters phone number
↓
User enters password
↓
Mobile calls backend login
↓
Backend verifies phone and password_hash
↓
Backend returns access_token + refresh_token
↓
Mobile stores tokens securely
↓
Mobile calls /api/v1/auth/me
↓
Mobile restores user, role, farmer_status, organization_id, membership_status
↓
Navigate to next required screen
```

### 11.2 First Login Requirement

First registration and first login require internet.

If no internet and no prior session exists:

```text
No internet. Please connect to the internet for first login.
```

### 11.3 Offline Use After First Login

After successful first login, ARI Mobile must support offline use.

Allowed offline actions:

```text
Open Home Screen
View cached Farm Notebook
Create Add Note drafts
Capture photo
Capture video
Record voice
Write text note
Attach file
Add link
Use existing media
Create local Notebook Entry
Create local Note Items
View pending upload queue
View cached notifications
Capture follow-up outcome locally
Use cached farm/zone/tree context
```

Actions requiring internet must show:

```text
No internet
```

Examples:

```text
First registration
First login
Token refresh
Backend sync
Media upload to MinIO
Fresh farm/zone/tree loading
Fresh notifications loading
ChatGPT / Gemini / Claude usage
Backend confirmation
```

### 11.4 Token Storage

Store securely:

```text
access_token
refresh_token
```

Never store:

```text
plain password
token in logs
token in plain local database
```

### 11.5 Access Token Handling

Every authenticated API request must include:

```text
Authorization: Bearer <access_token>
```

### 11.6 Refresh Token Handling

API:

```text
POST /api/v1/auth/refresh
```

Flow:

```text
401 token_expired
↓
Call refresh endpoint
↓
If success, retry once
↓
If failed, require login
```

### 11.7 Logout

API:

```text
POST /api/v1/auth/logout
```

Logout behavior:

```text
Clear tokens
Clear session state
Stop upload worker
Keep unsynced drafts/media unless user confirms deletion
```

After logout:

```text
Offline use is not allowed until user logs in again online.
```

---

## 12. RBAC in Mobile

Frozen roles:

```text
farmer
ari_staff
farm_coordinator
agronomist
reviewer
admin
root
```

Do not add new roles.

### 12.1 Mobile Responsibility

Mobile controls only:

```text
Visible menu items
Available buttons
Editable fields
Screen entry points
```

### 12.2 Backend Responsibility

Backend remains source of authorization truth.

Mobile must not create:

```text
Permission Service
Permission Matrix Engine
Policy Engine
Authorization Microservice
Permission API
Dedicated permission table
```

### 12.3 Farmer Status Visibility

For `role = farmer`:

```text
farmer_status = owner
  can see Create Farm flow after organization_id exists

farmer_status = owner_family
  must provide Farm ID and wait for approval

farmer_status = farm_staff
  must provide Farm ID and wait for approval
```

### 12.4 Role Visibility Summary

| Role                | Mobile Visibility                                                                                            |
| ------------------- | ------------------------------------------------------------------------------------------------------------ |
| farmer owner        | Home, Ask AI, Add Note, Farm Notebook, Notifications, Profile, Create Farm/Zone/Tree within own organization |
| farmer owner_family | Home after approval, Add Note, Ask AI, Notebook within approved farm scope                                   |
| farmer farm_staff   | Home after approval, Add Note, Ask AI if allowed, Notebook within approved farm scope                        |
| ari_staff           | Same app, staff field collection and onboarding support if backend allows                                    |
| farm_coordinator    | Farm/Zone/Tree context management in assigned scope                                                          |
| agronomist          | Notebook review and consultation viewing in assigned scope                                                   |
| reviewer            | Notebook filters/status/follow-up review in assigned scope                                                   |
| admin               | Organization/user/farm access in assigned scope                                                              |
| root                | Full system scope                                                                                            |

---

## 13. Navigation Structure

Navigation must preserve frozen UX.

### 13.1 Home Screen Fixed Primary Actions

```text
🤖 Ask AI
➕ เพิ่มบันทึก
📒 สมุดชาวสวน
🔔 แจ้งเตือน
```

### 13.2 Top-Level Context

Home Screen includes:

```text
🌳 Farm Selector
👤 Profile
```

Settings must be inside Profile or simple Settings area.

### 13.3 Onboarding Navigation

New user path:

```text
Launch App
↓
Register / Login
↓
Permission Setup
↓
If farmer_status = owner:
    Create Farm
↓
If farmer_status = owner_family / farm_staff:
    Pending Farm Approval or Home if active
↓
Home
```

### 13.4 No Bottom Navigation Redesign

Do not redesign navigation.

Do not create role-specific apps.

Do not add desktop navigation.

---

## 14. Screen Implementation Specification

### 14.1 Register Screen

Purpose:

```text
Allow mobile self-registration.
```

Data Needed:

```text
phone
name
password
farmer_status
farm_id if owner_family or farm_staff
```

Local State:

```text
registration_form_state
selected_farmer_status
farm_id_input
loading
error_message
```

API Calls:

```text
POST /api/v1/auth/register
```

Offline Behavior:

```text
Registration requires internet.
If no internet, show No internet.
```

Error Behavior:

```text
Phone already registered
Invalid phone format
Missing Farm ID for family/staff
Farm ID not found
Server unavailable
```

Navigation Result:

```text
owner → Permission Setup → Create Farm
owner_family/farm_staff → Permission Setup → Pending Approval or Home if active
```

### 14.2 Login Screen

Purpose:

```text
Authenticate user by phone number.
```

Data Needed:

```text
phone
password
```

API Calls:

```text
POST /api/v1/auth/login
GET /api/v1/auth/me
```

Offline Behavior:

```text
First login requires internet.
Previously logged-in user may open offline using cached session.
```

Navigation Result:

```text
Success → Home or required onboarding step
Failure → remain on Login Screen
```

### 14.3 Permission Setup Screen

Purpose:

```text
Request key mobile permissions once during first-time onboarding.
```

Permissions:

```text
Location
Camera
Microphone
Photos / Media / Files
Notifications
```

Rules:

```text
Explain permission before OS request.
Do not request same permission repeatedly.
Check permission status before feature use.
If denied, provide fallback.
If permanently denied, guide to Settings.
```

Offline Behavior:

```text
Permission setup can run offline after successful login.
```

Navigation Result:

```text
Owner → Create Farm
Family/Staff → Pending Approval or Home
Existing user → Home
```

### 14.4 Create Farm Screen

Purpose:

```text
Allow owner to create new farm under own organization.
```

Required user input:

```text
Farm Name
```

Auto-filled if available:

```text
GPS Latitude
GPS Longitude
Province
District
Subdistrict
Address
```

Optional manual fields:

```text
Farm Area
Main Crop
Description / Note
```

System-generated fields:

```text
organization_id
created_by_user_id
farm_id
farm_code
created_at
status
```

Rules:

```text
Owner must not manually type farm_id.
Backend generates farm_id / farm_code.
Owner may create multiple farms.
Auto-filled location must be editable before saving.
Farm Name remains the only required user-entered field in P1-2.
```

API Calls:

```text
POST /api/v1/farms
```

Offline Behavior:

```text
Create Farm as server record requires internet.
If offline, allow local draft only if implementation supports it.
Otherwise show No internet.
```

### 14.5 Create Zone Screen

Purpose:

```text
Allow owner or permitted user to create zone under farm.
```

Required:

```text
farm_id
zone_name
```

Optional:

```text
description
```

API Calls:

```text
POST /api/v1/zones
```

Offline Behavior:

```text
Server creation requires internet.
Local draft optional.
```

### 14.6 Create Tree Screen

Purpose:

```text
Allow owner or permitted user to create tree identity under zone.
```

Required:

```text
zone_id
tree_code
```

Optional:

```text
status
```

API Calls:

```text
POST /api/v1/trees
```

Rules:

```text
Tree registration is optional in P0.
Do not force users to create trees before capture.
```

### 14.7 Home Screen

Purpose:

```text
Provide simple access to Ask, Record, Review, Learn.
```

Data Needed:

```text
current_user
role
farmer_status
membership_status
active_organization
active_farm_context
notification_count
upload_queue_count
```

Offline Behavior:

```text
Show cached user/context.
Allow local capture if session exists.
Show pending queue.
```

### 14.8 Ask AI Screen

Purpose:

```text
Implement external AI consultation workflow.
```

Flow:

```text
Open Ask AI
↓
Capture photo/video/voice/text/file/link
↓
Save Local
↓
Create Notebook Entry with entry_type = consultation
↓
Select external AI app:
  ChatGPT
  Gemini
  Claude
  Other
↓
If internet unavailable:
  Show No internet
↓
User returns to ARI
↓
Prompt: What did you learn?
↓
Save learned_summary
↓
Schedule follow-up 3/7/14 days
```

Rules:

```text
No internal AI assistant
No RAG
No vector database
No autonomous agent
External AI result must be verified by user
Consultation is Notebook Entry Type, not separate entity
```

### 14.9 Add Note Screen

Purpose:

```text
Create standard Notebook Entry as Note Session.
```

Supported items:

```text
Photo
Video
Voice
Text
File
Link
Existing Media
```

Rules:

```text
Notebook Entry = Note Session
Note Item = Timeline Item
sequence_order required
Save Local first
Upload later
farm_id / zone_id / tree_id nullable
organization_id required
created_by_user_id from authenticated user
```

### 14.10 Capture Media Screen

Purpose:

```text
Capture or attach media and create Local Note Items.
```

Required metadata:

```text
local_path
file_name
file_size
mime_type
checksum if available
duration_sec for video/voice
sequence_order
upload_status
```

Offline Behavior:

```text
Fully available offline if permission granted.
```

### 14.11 Farm Notebook Screen

Purpose:

```text
List and search notebook entries.
```

Search:

```text
Keyword search
Filter search
```

Allowed filters:

```text
farm_id
zone_id
tree_id
entry_type
entry_context
date_from
date_to
created_by_user_id if API allows
upload_status local only
```

Not allowed:

```text
Vector Search
Semantic Search
Knowledge Graph Search
RAG Search
LLM Search
```

### 14.12 Notebook Entry Detail Screen

Purpose:

```text
Show Notebook Entry and timeline items.
```

Displays:

```text
Entry metadata
Timeline Note Items
Media previews/playback
Text
Links
Consultation learned_summary
Follow-up status
Upload/sync status
```

Timeline order:

```text
sequence_order ascending
```

### 14.13 Notifications Screen

Purpose:

```text
Show upload reminders, follow-up reminders, system notifications.
```

API Calls:

```text
GET /api/v1/notifications
GET /api/v1/notifications/{notification_id}
PATCH /api/v1/notifications/{notification_id}/read
POST /api/v1/notifications/mark-all-read
```

Offline Behavior:

```text
Show cached notifications.
Allow local read state pending sync.
```

### 14.14 Follow-Up Screen

Purpose:

```text
Record consultation outcome after 3, 7, or 14 days.
```

Allowed outcomes:

```text
improved
same
worse
unknown
```

Offline Behavior:

```text
Allow local outcome capture.
Queue update for later sync.
```

### 14.15 Farm Selector Screen

Purpose:

```text
Set active organization/farm/zone/tree context.
```

Context fields:

```text
organization_id required
farm_id nullable
zone_id nullable
tree_id nullable
```

Sources:

```text
manual
qr
restored
field_collection
none
```

Rules:

```text
Capture works without farm/zone/tree selected.
Capture does not work without organization_id.
```

### 14.16 Pending Approval Screen

Purpose:

```text
Show owner_family / farm_staff pending approval state.
```

Displayed message:

```text
ส่งคำขอเข้าร่วมสวนแล้ว
กรุณารอเจ้าของสวนหรือผู้ดูแลระบบอนุมัติ
```

Allowed actions:

```text
Refresh status
Logout
Edit profile if allowed
```

Not allowed before approval:

```text
Access farm notebook
Create farm/zone/tree
Upload farm-scoped records
View farm data
```

### 14.17 Profile / Settings Screen

Purpose:

```text
Show user profile, role, farmer_status, membership_status, app settings, logout.
```

Displays:

```text
Phone number
Name
Role
Farmer status
Membership status
Organization ID
Active Farm ID if applicable
App version
Environment
```

### 14.18 QR Scan Screen If Supported

Supported payloads:

```text
ari://farm/{farm_id}
ari://zone/{zone_id}
ari://tree/{tree_id}
```

Rules:

```text
QR = Representation only
No qr_registry
No QR entity
No QR module
Manual fallback required
```

### 14.19 Upload Queue / Sync Status Screen

Purpose:

```text
Show pending records and upload/sync progress.
```

API Calls:

```text
POST /api/v1/sync/batch
POST /api/v1/files/upload-url
POST /api/v1/files/complete
```

Offline Behavior:

```text
Show pending queue.
Disable remote retry.
Allow user to keep capturing.
```

---

## 15. First-Time Permission Setup Policy

After successful registration or first login, ARI Mobile must present a Permission Setup screen.

Permissions:

```text
Location
Camera
Microphone
Photos / Media / Files
Notifications
```

Rules:

```text
Request during onboarding.
Explain reason before requesting.
Do not repeatedly request the same permission.
Check permission status before feature use.
If denied, provide fallback.
If permanently denied, guide to Settings.
Do not delete local drafts because permission is denied.
```

### 15.1 Location Permission for Create Farm

If permission granted:

```text
Capture GPS latitude/longitude.
If internet available, reverse geocode to province/district/subdistrict/address.
Show all fields to owner for review/edit before saving.
```

If no internet:

```text
GPS may still be captured.
Address auto-fill may fail.
Show No internet for address lookup.
Manual entry remains available.
```

If permission denied:

```text
Show manual entry fields.
```

---

## 16. Create Farm Implementation

### 16.1 Owner May Have Multiple Farms

Policy:

```text
One Owner User
↓
One Organization
↓
Multiple Farms
```

Example:

```text
Owner: Somchai
Organization: Org-Somchai
Farm A: ARI-FARM-A123
Farm B: ARI-FARM-B456
Farm C: ARI-FARM-C789
```

### 16.2 Create Farm Required Input

Only required user-entered field:

```text
Farm Name
```

### 16.3 Auto-Filled Fields

Auto-filled from phone when possible:

```text
GPS Latitude
GPS Longitude
Province
District
Subdistrict
Address
```

All auto-filled fields must be editable before saving.

### 16.4 Optional Fields

```text
Farm Area
Main Crop
Description / Note
```

### 16.5 System-Generated Fields

```text
organization_id
created_by_user_id
farm_id
farm_code
status
created_at
```

Owner must not manually enter:

```text
farm_id
organization_id
created_by_user_id
status
```

### 16.6 Farm Code Purpose

Farm ID / Farm Code may be used by:

```text
Owner's Family
Farm Staff
```

to request joining the farm.

### 16.7 Farm Location Storage

Mobile must use the approved `farms.location` storage strategy from P0 Database / P0 API.

Preferred implementation:

```text
farms.location JSONB/object
```

Supported structure:

```json
{
  "province": "...",
  "district": "...",
  "subdistrict": "...",
  "address": "...",
  "gps_latitude": 0.0,
  "gps_longitude": 0.0,
  "source": "device_gps|manual"
}
```

If backend only supports text location in a specific implementation, mobile may serialize the location summary into `location` or `description` only if explicitly approved.

---

## 17. Local Storage Implementation

Local storage must support:

```text
Draft notebook entries
Draft note items
Media local paths
Offline queue
Upload queue
Auth tokens
Active farm context
Device ID
Client IDs
Pending follow-ups
Notifications cache
Cached user/session data
Cached farm/zone/tree hierarchy
Registration/onboarding status
Permission setup status
Server ID mapping
```

Secure storage:

```text
access_token
refresh_token
```

Local database:

```text
notebook_entries_local
note_items_local
upload_queue_local
sync_queue_local
follow_ups_local
notifications_local
farm_context_cache
user_session_cache
id_mapping
```

File system storage:

```text
photo files
video files
voice files
picked files
temporary compressed files
```

No data loss after:

```text
app restart
network loss
token expiry
upload failure
partial sync failure
```

---

## 18. Client ID and Device ID Strategy

### 18.1 Device ID

Generate once per installation:

```text
device_id = uuid
```

Persist locally.

### 18.2 Client ID

Generate for every offline-created logical record:

```text
client_id = uuid
```

Applies to:

```text
Notebook Entry
Local Note Item
Follow-Up update
Notification read update
Upload queue item
```

### 18.3 Client Batch ID

Generate for each sync batch:

```text
client_batch_id = uuid
```

Used in:

```text
POST /api/v1/sync/batch
```

### 18.4 Idempotency Rule

Use:

```text
user_id + client_id
```

Rules:

```text
Do not regenerate client_id on retry.
Do not duplicate records after retry.
Map local_id to server_id after success.
```

---

## 19. Offline Sync Implementation

### 19.1 Sync Queue Operations

```text
create_notebook_entry
create_text_note_item
create_link_note_item
create_note_item_after_file_upload
update_notebook_entry
create_follow_up
update_follow_up_outcome
mark_notification_read
```

### 19.2 Sync Batch

API:

```text
POST /api/v1/sync/batch
```

Batch includes:

```text
client_batch_id
device_id
organization_id
operations[]
```

Each operation includes:

```text
client_id
operation_type
entity_type
payload
created_at
```

### 19.3 Retry Logic

```text
retry_count starts at 0
max retry from configuration
failed items remain in queue
manual retry allowed
network unavailable blocks retry
```

### 19.4 Partial Success

```text
Mark successful operations synced.
Persist server_id mapping.
Keep failed operations in queue.
Do not resend successful operations.
```

### 19.5 Conflict

```text
Do not delete local record.
Mark conflict.
Show manual review needed.
```

---

## 20. File Upload Implementation

### 20.1 Frozen Upload Endpoints

Use only:

```text
POST /api/v1/files/upload-url
POST /api/v1/files/complete
```

Do not invent:

```text
/files/presign
/files/confirm
/upload/presign
/upload/complete
/media/upload
```

### 20.2 Local Note Item vs Server Note Item

Mobile may create Local Note Item immediately after capture.

Local Note Item may contain:

```text
local_item_id
local_entry_id
client_id
item_type
sequence_order
local_path
file_name
file_size
mime_type
checksum if available
duration_sec if applicable
upload_status
sync_status
```

Server-side media Note Item must be completed only after:

```text
Notebook Entry resolved to server entry_id
Presigned upload URL requested
Media uploaded to MinIO
Backend confirms upload
file_ref / file_path exists
Local Note Item updated with server_item_id and file_ref / file_path
```

### 20.3 Correct Upload Order

```text
Capture media
↓
Create Local Note Item
↓
Save local_path and metadata
↓
Queue upload
↓
Sync or resolve Notebook Entry to server entry_id
↓
Request backend presigned upload URL
↓
Upload media to MinIO
↓
Confirm upload with backend
↓
Create or complete server Note Item with file_ref / file_path
↓
Update Local Note Item mapping
↓
Mark upload_status = completed
```

### 20.4 Failed Upload

```text
Mark upload_status = failed.
Increment retry_count.
Retain local file.
Show retry option.
Do not create duplicate note item.
Reuse same client_id, local_item_id, and sequence_order.
```

---

## 21. Media Capture Implementation

Supported capture types:

```text
Camera photo
Camera video
Voice recording
Text note
File picker
Link capture
Existing media picker
```

Metadata:

```text
local_path
file_name
file_size
mime_type
checksum if available
duration_sec for video/voice
created_at
upload_status
```

Not allowed:

```text
AI image diagnosis
AI disease detection
Object detection
Video analysis
Speech-to-text AI pipeline
Automated treatment recommendation
```

---

## 22. QR / ID Implementation

P0 supports:

```text
Farm QR
Zone QR
Tree QR
```

QR is:

```text
Representation
```

QR is not:

```text
Entity
Database Table
Domain Model
Registry
Service Boundary
```

Supported payloads:

```text
ari://farm/{farm_id}
ari://zone/{zone_id}
ari://tree/{tree_id}
```

Manual fallback:

```text
Farm Selector
Zone Selector
Tree Selector
Clear Context
General Note
```

---

## 23. ARI Field Collection Code / Simulator Farm Code

### 23.1 Purpose

This is not a fake farm.

It is a field collection context for ARI Staff to capture real-world survey evidence before production farm structure is fully registered or approved.

Used for:

```text
Disease examples
Pest examples
Fertilizer observations
Soil / water / canopy observations
Expert interviews
Farmer interviews
Field walk notes
Orchard survey notes
Photos
Videos
Voice recordings
Documents
External AI consultation records
Other field evidence
```

### 23.2 Naming

Preferred user-facing label:

```text
ARI Field Collection Code
```

### 23.3 Domain Rule

Do not create:

```text
Simulator Farm Entity
Field Collection Entity
Survey Farm Entity
Temporary Farm Entity
Owner Registry
Block Registry
QR Registry
```

Use existing Farm / Organization context if backend returns it.

### 23.4 Mobile Behavior

Mobile may:

```text
Select ARI Field Collection Code from Farm Selector if backend returns it.
Display badge: ARI Field Collection.
Capture notebook entries under that context.
Sync normally.
```

Mobile must not create new field collection entity/table/API.

---

## 24. Farm Notebook Implementation

Notebook list shows:

```text
title or fallback label
entry_type
created_at
farm/zone/tree context
ARI Field Collection badge if applicable
upload_status
consultation indicator
follow-up status
```

Entry detail shows:

```text
Notebook Entry metadata
Timeline Note Items
Media previews/playback
Text content
Link items
Consultation learned_summary
Follow-up status
Upload/sync status
```

Timeline order:

```text
sequence_order ascending
```

---

## 25. Notifications Implementation

Notification types:

```text
Upload reminders
Follow-up reminders
System notifications
ARI reply notifications if API supports
```

Backend APIs:

```text
GET /api/v1/notifications
GET /api/v1/notifications/{notification_id}
PATCH /api/v1/notifications/{notification_id}/read
POST /api/v1/notifications/mark-all-read
```

Local notification scheduling:

```text
20:00 upload reminder
3-day follow-up
7-day follow-up
14-day follow-up
```

---

## 26. Follow-Up Implementation

Required periods:

```text
3 days
7 days
14 days
```

Status:

```text
pending
completed
missed if locally overdue
sync_pending
```

Outcomes:

```text
improved
same
worse
unknown
```

---

## 27. Error Handling UX

### 27.1 No Internet

```text
Show offline banner.
Allow local capture.
Disable remote-only actions.
Queue sync/upload.
Show “No internet” for backend/external-AI actions.
```

### 27.2 Token Expired

```text
Attempt refresh once.
If success, retry.
If failed, require login.
Keep local data.
```

### 27.3 Registration Errors

```text
Phone already registered
Invalid phone
Missing Farm ID
Farm ID not found
Pending approval
Rejected
Suspended
Revoked
```

### 27.4 Upload Failed

```text
Mark failed.
Keep local media.
Show retry.
Do not duplicate note item.
```

### 27.5 Permission Denied

```text
Show explanation.
Provide fallback.
Guide to Settings if permanently denied.
```

### 27.6 Storage Full

```text
Stop capture safely.
Warn user.
Preserve saved data.
Suggest freeing storage.
```

---

## 28. Security Implementation

### 28.1 Token Security

```text
Store access token securely.
Store refresh token securely.
Never store password.
Never log tokens.
```

### 28.2 Password Security

```text
Default password 1234 is P0 pilot only.
Backend stores only password_hash.
Mobile must not log password.
Mobile must not store password in plain database.
```

### 28.3 Media Privacy

```text
Store media in app-controlled storage when possible.
Do not expose local media paths in logs.
Do not upload without user action or scheduled upload rule.
```

### 28.4 Presigned URL Security

```text
Do not log presigned URL.
Do not reuse expired upload URL.
Request new URL on retry if expired.
```

### 28.5 Logout

```text
Clear tokens.
Clear session state.
Stop active upload worker.
Keep unsynced drafts/media unless user confirms deletion.
```

---

## 29. Configuration

Environments:

```text
local
dev
staging
production
```

Configuration items:

```text
API_BASE_URL
API_VERSION
UPLOAD_TIMEOUT
SYNC_BATCH_SIZE
MAX_RETRY_COUNT
DEFAULT_UPLOAD_REMINDER_TIME
SUPPORTED_EXTERNAL_AI_APPS
PHONE_NUMBER_FORMAT
DEFAULT_P0_PASSWORD_POLICY
```

Default values:

```text
API_VERSION = /api/v1
DEFAULT_UPLOAD_REMINDER_TIME = 20:00
SUPPORTED_EXTERNAL_AI_APPS = chatgpt, gemini, claude, other
```

---

## 30. Testing Strategy

### 30.1 Unit Tests

Test:

```text
phone normalization
farmer_status selection
membership_status handling
client_id generation
device_id persistence
sync batch builder
upload queue status transitions
QR payload parser
checksum utility
follow-up date calculation
field collection badge logic
location auto-fill mapping
permission state handling
```

### 30.2 Widget Tests

Test:

```text
Register Screen
Login Screen
Permission Setup Screen
Create Farm Screen
Create Zone Screen
Create Tree Screen
Pending Approval Screen
Home Screen
Ask AI Screen
Add Note Screen
Farm Notebook Screen
Notifications Screen
Follow-up Screen
Farm Selector Screen
Upload Queue Screen
```

### 30.3 Integration Tests

Test:

```text
owner registration → organization assignment → create farm
family/staff registration → farm ID → pending approval
login → permission setup → home
offline after first login
add note → save local
ask ai → local consultation → no internet behavior
media capture → upload queue
upload queue → upload-url → MinIO upload → files/complete
notification → follow-up outcome
```

### 30.4 Offline Sync Tests

Test:

```text
capture offline
restart app
sync when online
partial success
conflict response
retry failed item
idempotent retry with same client_id
```

### 30.5 Upload Flow Tests

Test:

```text
request upload URL through /api/v1/files/upload-url
upload media to presigned URL
confirm upload through /api/v1/files/complete
retry failed upload
large video pending upload
expired presigned URL refresh
server note item completed only after file_ref / file_path exists
```

---

## 31. Build and Release

### 31.1 Android

Required outputs:

```text
Debug APK
Internal testing APK
Release AAB
```

### 31.2 iOS

Required outputs:

```text
Debug build
TestFlight build
Release build
```

### 31.3 P1-2 Platform Policy

P1-2 supports only:

```text
Android
iOS
```

P1-2 does not support:

```text
macOS Desktop App
Ubuntu Desktop App
Windows Desktop App
Web App
```

Web App will be handled in:

```text
P1-3 Web App Implementation Specification
```

---

## 32. P1-2 Required Checklist

Before coding starts:

```text
[ ] Android/iOS only confirmed.
[ ] Desktop app excluded.
[ ] Web app moved to P1-3.
[ ] One mobile app only.
[ ] /api/v1 API base configured.
[ ] Self-registration screen defined.
[ ] Phone-number login defined.
[ ] Phone normalization policy defined.
[ ] farmer_status defined: owner / owner_family / farm_staff.
[ ] farmer_status confirmed as status, not new RBAC role.
[ ] membership_status defined.
[ ] users.farmer_status backend dependency confirmed.
[ ] users.membership_status backend dependency confirmed.
[ ] users.primary_farm_id backend dependency confirmed if used.
[ ] POST /api/v1/auth/register confirmed.
[ ] Login by phone confirmed.
[ ] Default password 1234 limited to P0 pilot.
[ ] Password hash only.
[ ] First login requires internet.
[ ] Offline use after successful login defined.
[ ] Owner registration creates/assigns organization_id.
[ ] Owner may create multiple farms.
[ ] Create Farm Screen defined.
[ ] Farm Name is only required user-entered field.
[ ] Farm location auto-fill defined.
[ ] Auto-filled location editable before save.
[ ] Family/Staff join by Farm ID, not Owner ID.
[ ] Family/Staff cannot create Farm/Zone/Tree.
[ ] Pending approval screen defined.
[ ] Owner self-managed approval excluded from P1-2.
[ ] First-time permission setup defined.
[ ] Location/Camera/Microphone/Photos/Notifications permission policy defined.
[ ] Auth token secure storage defined.
[ ] Current user restore flow defined.
[ ] Frozen roles listed exactly.
[ ] No permission engine added.
[ ] Home screen four actions fixed.
[ ] Add Note local-first flow defined.
[ ] Ask AI external consultation flow defined.
[ ] Consultation implemented as entry_type = consultation.
[ ] No Consultation entity/module added.
[ ] Note Item timeline sequence_order supported.
[ ] Supported item types: photo/video/voice/text/file/link.
[ ] Existing media picker supported.
[ ] Local database schema for drafts/queues defined.
[ ] Device ID generation defined.
[ ] Client ID generation defined.
[ ] Client batch ID generation defined.
[ ] Offline sync batch builder defined.
[ ] POST /api/v1/sync/batch supported.
[ ] Upload endpoint locked to POST /api/v1/files/upload-url.
[ ] Upload complete endpoint locked to POST /api/v1/files/complete.
[ ] Local Note Item vs Server Note Item separation defined.
[ ] No direct upload without backend presign.
[ ] Follow-up 3/7/14 days defined.
[ ] Outcomes limited to improved/same/worse/unknown.
[ ] Notifications cache and read state defined.
[ ] Upload reminder default 20:00 defined.
[ ] QR scan supports ari://farm, ari://zone, ari://tree if supported.
[ ] QR remains representation only.
[ ] No qr_registry added.
[ ] Farm/zone/tree nullable capture supported.
[ ] organization_id required.
[ ] Keyword/filter notebook search only.
[ ] No vector/semantic/RAG/LLM search.
[ ] Error handling UX defined.
[ ] Security rules defined.
[ ] Environment configuration defined.
[ ] Flutter tests planned.
[ ] Android/iOS release checklist defined.
```

---

## 33. Confirmed Backend/API Dependency Checklist

The following dependencies are confirmed as part of the approved P0 API / P1-1 Backend additive revision path and must be used consistently by P1-2 mobile:

```text
[ ] Confirm POST /api/v1/auth/register exists in P0 API revision.
[ ] Confirm login by phone number exists in P0 API revision.
[ ] Confirm phone normalization and uniqueness rules exist.
[ ] Confirm farmer_status exists:
    owner
    owner_family
    farm_staff
[ ] Confirm membership_status exists:
    pending_farm_approval
    active
    rejected
    suspended
    revoked
[ ] Confirm owner registration behavior:
    create/assign organization_id immediately.
[ ] Confirm family/staff registration behavior:
    require Farm ID.
[ ] Confirm Farm ID validation.
[ ] Confirm minimal membership storage:
    users.primary_farm_id or approved equivalent.
[ ] Confirm owner can create farm through POST /api/v1/farms.
[ ] Confirm approved farms.location storage strategy.
[ ] Confirm no new RBAC roles.
[ ] Confirm no permission service.
[ ] Confirm no owner registry.
[ ] Confirm no farm_memberships table in P1-2 unless explicitly revised later.
```

---

## 34. Non-Goals

P1-2 must not implement:

```text
Internal AI Assistant
Knowledge Graph
Vector Database
RAG
Agent Orchestration
Commerce
Robot Control
Irrigation Control
Fertilizer Control
Audit System
Permission Service
Separate Farmer App
Separate Staff App
New Backend Architecture
New Database Architecture
QR Registry
Consultation Entity
Owner Registry
Block Registry
Field Collection Entity
Temporary Farm Entity
Survey Farm Entity
Review Table
Knowledge Table
Semantic Search
LLM Search
AI Diagnosis
Autonomous Recommendation
Production farm conversion workflow
macOS Desktop App
Ubuntu Desktop App
Windows Desktop App
Web App
OTP / SMS verification
Invite link
Password reset
Owner-managed member approval screen
Multi-farm membership management
```

---

## 35. Freeze Boundary

After P1-2 Freeze:

```text
No mobile UX redesign
No new app
No new API requirement
No new database requirement
No new role
No new domain entity
No Consultation entity
No QR Registry
No permission service
No internal AI assistant
No desktop app scope
No web app scope
```

Any change must go through:

```text
Revision Proposal
→ Review
→ Approval
→ New Version
```

### Final Statement

ARI V1 — P1-2 Mobile App Implementation Specification v1.0 defines how to implement the ARI mobile app using Flutter for Android and iOS.

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

It implements:

```text
Mobile self-registration
Phone-number login
Farmer status onboarding
Owner farm creation
Family/staff farm join by Farm ID
First-time permission setup
Offline local capture
Notebook entries
Note item timeline
External AI consultation as Notebook Entry Type
Follow-up tracking
Notifications
Farm context
QR/ID representation handling
Offline sync
MinIO presigned upload
Secure authentication
Android/iOS build and release
```

It does not implement:

```text
Web App
Desktop App
Internal AI
Knowledge Graph
RAG
Vector Search
Commerce
Robot Control
Permission Service
QR Registry
Consultation Entity
```

Current Status:

```text
Draft Final
Owner Decisions Integrated
Backend/API Additive Revisions Confirmed
Freeze Readiness: Ready for Owner Freeze Approval
```

---

## 36. Cross-Document Revision Impact

### 36.1 Purpose

This section records the cross-document impact of Owner-approved P1-2 decisions that affect backend/API implementation contracts.

This section does not create a new ARI document.

This section does not create a new source of truth.

This section confirms that P1-2 mobile implementation must remain aligned with the approved additive revisions in the affected documents.

### 36.2 Affected Documents

The following documents are affected:

```text
ARI V1 — P0 API Specification v1.0
ARI V1 — P1-1 Backend Implementation Specification v1.0
```

The following documents are not redesigned:

```text
P0 Domain Model
P0 Database Schema
#46A Mobile UX
#46B Web UX
#45 Architecture
#47 AI Agent Development Workflow
```

However, additive API/backend implementation support is required for the approved mobile onboarding flow.

### 36.3 Owner-Approved Decisions Causing Cross-Document Impact

The following Owner-approved decisions are now part of P1-2 mobile implementation scope:

```text
1. User can self-register from ARI Mobile App.
2. Registration requires internet.
3. Phone number is the platform-wide login ID.
4. The same login ID should later work for Web App in P1-3.
5. Initial P0 pilot password may be simple, e.g. 1234.
6. Password must never be stored as plain text.
7. First login requires internet.
8. After successful login, mobile can be used offline.
9. Backend/external-AI actions must show “No internet” when offline.
10. Farmer role remains existing role = farmer.
11. farmer_status is added:
    - owner
    - owner_family
    - farm_staff
12. Owner registration creates or assigns organization_id.
13. Owner may create multiple farms under own organization.
14. Owner's Family and Farm Staff join by Farm ID, not Owner ID.
15. Owner's Family and Farm Staff cannot create Farm/Zone/Tree.
16. Owner's Family and Farm Staff require membership approval.
17. membership_status is required:
    - pending_farm_approval
    - active
    - rejected
    - suspended
    - revoked
18. Create Farm screen requires only Farm Name from user.
19. Mobile may auto-fill location from phone GPS.
20. Auto-filled location must be editable before save.
21. First-time Permission Setup is shown after registration/login.
22. P1-2 supports Android and iOS only.
23. Desktop app is out of scope.
24. Web App is moved to P1-3.
```

### 36.4 P0 API Dependency Impact

P1-2 depends on P0 API support for:

```text
POST /api/v1/auth/register
Phone-number login
Phone normalization
Phone uniqueness
farmer_status
membership_status
Owner registration with organization assignment
Family/Staff registration with Farm ID
Farm ID validation
Create Farm permission for self-registered owner
Structured farm location or approved location storage strategy
```

### 36.5 P1-1 Backend Dependency Impact

P1-2 depends on P1-1 Backend support for:

```text
Auth registration service
Phone-based login lookup
Password hash only
User model additive fields
Organization assignment during owner registration
Farm join request handling
membership_status handling
primary_farm_id or approved equivalent
Create Farm authorization for self-registered owner
Farm location storage handling
No new RBAC roles
No permission service
No owner registry
No QR registry
No consultation entity
```

### 36.6 Freeze Rule

P1-2 may be frozen only after confirming that the required additive revisions are already accepted in the affected documents.

For the current freeze review, the required revision dependencies are considered resolved if P0 API and P1-1 Backend revision notes have been merged or approved by Owner.

Current status:

```text
Revision dependencies confirmed.
P1-2 Freeze Readiness: Ready for Owner Freeze Approval.
```

### 36.7 No Architecture Redesign

The revision impact must not introduce:

```text
New platform
New mobile app
Separate farmer app
Separate staff app
New domain model
New database architecture
New RBAC role
Permission service
Owner registry
QR registry
Consultation entity
Knowledge graph
Vector database
RAG
Agent orchestration
Desktop app
Web app implementation inside P1-2
```

### 36.8 Freeze Confirmation Checklist

Before P1-2 Freeze, the following must be confirmed:

```text
[ ] P0 API register endpoint confirmed.
[ ] Phone-number login confirmed.
[ ] farmer_status confirmed.
[ ] membership_status confirmed.
[ ] Owner organization assignment confirmed.
[ ] Family/Staff join by Farm ID confirmed.
[ ] Farm ID validation confirmed.
[ ] Minimal membership storage confirmed.
[ ] Create Farm authorization for self-registered owner confirmed.
[ ] Farm location storage strategy confirmed.
[ ] P1-1 Backend patch confirmed.
[ ] No new RBAC role introduced.
[ ] No permission service introduced.
[ ] No new registry entity introduced.
```

### 36.9 Final Freeze Readiness Statement

This P1-2 Mobile App Implementation Specification is ready for Owner Freeze Approval because it:

```text
Aligns with P0 Domain Model
Aligns with P0 Database Schema
Aligns with P0 API additive revision
Aligns with P1-1 Backend additive revision
Preserves One Platform / One Mobile App / One Backend / One Database
Does not introduce forbidden entities, services, roles, registries, or architecture changes
Keeps Web App in P1-3
Keeps Desktop App out of scope
```

Recommended final status after Owner approval:

```text
Status: FROZEN
Freeze Date: <Owner approval date>
```
**************
Freeze
**************

ARI V1 — P1-2 Mobile App Implementation Specification v1.0
Status: FROZEN
Freeze confirmed by Owner

สรุป Freeze Boundary ที่ล็อกแล้ว:

- Android / iOS only
- Flutter Mobile App
- Web App ไปทำใน P1-3
- Desktop App out of scope
- Phone self-registration
- Phone-number login
- farmer_status: owner / owner_family / farm_staff
- Owner มีหลาย Farm ได้
- Family / Staff join by Farm ID
- First-time permission setup
- Offline-first capture
- Ask AI = external consultation flow
- Consultation = Notebook Entry Type
- QR = Representation only
- No permission service
- No new RBAC role
- No qr_registry
- No consultation entity

ต่อจากนี้ถ้ามีการเปลี่ยนแปลง P1-2 ต้องทำผ่าน:

Revision Proposal
→ Review
→ Approval
→ New Version
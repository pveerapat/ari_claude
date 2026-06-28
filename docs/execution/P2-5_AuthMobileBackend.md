# ARI V1 — P2-5 Auth and Mobile Onboarding Backend v1.0

Project: ARI — Agricultural Intelligence Platform
Phase: P2 Coding Execution Phase
Document Number: P2-5
Document Type: Auth and Mobile Onboarding Backend Specification / Execution Document
Version: v1.0
Status: Draft Final / Ready for Owner Review
Prepared From: Frozen Source of Truth + P2-1 / P2-2 / P2-3 / P2-4 Coding Execution Authority
Coding Direction: Backend Foundation First → Database → Auth → Farm Structure → Notebook / Upload / Sync → Mobile MVP → Web MVP → E2E → Prototype Deployment

---

# 1. Document Control

## 1.1 Document Identity

```text
Document Title:
ARI V1 — P2-5 Auth and Mobile Onboarding Backend v1.0

Project:
ARI — Agricultural Intelligence Platform

Phase:
P2 Coding Execution Phase

Document Number:
P2-5

Document Status:
Draft Final / Ready for Owner Review
```

## 1.2 Previous Frozen / Confirmed Documents

```text
ARI V1 — P2-1 Coding Execution Plan & Sprint Backlog v1.0
Status: FROZEN

ARI V1 — P2-2 Monorepo & Local Development Setup v1.0
Status: FROZEN
Coding Foundation: IMPLEMENTED
Smoke Test: PASS

ARI V1 — P2-3 Backend Feature Foundation v1.0
Status: FROZEN
Coding Foundation: IMPLEMENTED
Smoke Test: PASS

ARI V1 — P2-4 Database and Alembic Migration Foundation v1.0
Status: FROZEN
Coding Foundation: IMPLEMENTED LOCALLY
Smoke Test: PASS
```

## 1.3 P2-4 Implementation Status Note

P2-4 local implementation status is recorded as:

```text
GET /health: PASS
GET /api/v1/health: PASS
alembic upgrade head: PASS
pytest: 82/82 passed
```

Commit / push / merge status is not assumed in this document.

```text
Owner Confirmation Required:
Confirm whether P2-4 has been committed, pushed, and merged before coding implementation starts.
```

## 1.4 Document Boundary

This document defines the backend authentication and mobile onboarding implementation scope only.

This document is still a specification / execution document.

This document does not authorize actual coding implementation unless the Owner explicitly instructs implementation later.

This document does not create P2-6.

This document does not redesign ARI.

---

# 2. Purpose

The purpose of P2-5 is to define the backend authentication and mobile onboarding foundation after the database and Alembic foundation.

P2-5 prepares the backend for:

```text
Mobile self-registration
Phone-number login
JWT access token issuing
JWT refresh token issuing
Current user retrieval
Owner onboarding
Owner family onboarding
Farm staff onboarding
Farm ID join validation
Pending farm approval state handling
Account status handling
Membership status handling
Basic auth dependency foundation
Basic guard foundation
```

P2-5 must use the User additive fields from P0 Domain Model Additive Revision v1.1:

```text
phone
farmer_status
membership_status
account_status
primary_farm_id
```

Important frozen rule:

```text
farmer_status is not an RBAC role.
```

P2-5 must not create:

```text
Owner Registry
Member Registry
Farmer Registry
Farm Membership Entity
Permission Entity
New RBAC Role
New Backend Service
New Database Architecture
```

---

# 3. Scope

## 3.1 In Scope

P2-5 covers:

```text
Authentication implementation boundary
Password hashing strategy
Password verification strategy
JWT access token strategy
JWT refresh token strategy
JWT token decode / validation foundation
Phone normalization strategy
Phone-number login
Phone uniqueness handling
POST /api/v1/auth/register
POST /api/v1/auth/login
POST /api/v1/auth/refresh
GET /api/v1/auth/me
POST /api/v1/auth/logout boundary
Current user schema
Owner onboarding backend flow
Owner family onboarding backend flow
Farm staff onboarding backend flow
Farm ID join validation boundary
Account status handling
Membership status handling
Pending farm approval handling
User repository/service implementation boundary
Organization assignment / creation boundary for owner registration
Minimal Farm ID lookup boundary for owner_family / farm_staff registration
Auth router/service/schema implementation boundary
Auth dependency foundation
RBAC guard boundary
What is allowed in P2-5
What must be deferred to P2-6 or later
Tests and smoke test requirements
P2-5 GitHub issue breakdown
API Gap / Revision Proposal handling
```

## 3.2 Deliverable

The deliverable is a safe auth and mobile onboarding backend execution specification.

Target result after P2-5 coding implementation is explicitly approved:

```text
Auth schemas exist
Auth router exists
Auth service exists
Auth dependencies exist
Password hashing works
Phone normalization works
Phone registration works
Phone login works
JWT access token issuing works
JWT refresh token issuing works within frozen boundary
GET /api/v1/auth/me returns onboarding state
Owner registration creates/assigns organization_id
Owner family / farm staff registration resolves organization_id from Farm ID
Owner family / farm staff registration uses Farm ID as join reference
Pending farm approval blocks protected farm-scoped access
Health endpoints remain unchanged
Alembic migration foundation remains unchanged
No new database tables are introduced
No new RBAC roles are introduced
No Farm CRUD is introduced
No Notebook / Upload / Sync implementation is introduced
Tests pass
```

## 3.3 Scope Principle

P2-5 implements only the auth/onboarding layer required before farm structure APIs.

P2-5 may touch:

```text
Router Layer
Service Layer
Repository Layer
Dependency Layer
Security Utilities
Schema Layer
```

P2-5 must not implement full business feature APIs beyond the authentication and onboarding boundary.

---

# 4. Source of Truth

## 4.1 Frozen Source Documents

P2-5 must follow:

```text
ARI V1 — P0 Domain Model Specification v1.0
ARI V1 — P0 Domain Model Additive Revision v1.1

ARI V1 — P0 Database Schema Specification v1.0
ARI V1 — P0 Database Schema Additive Revision v1.1

ARI V1 — P0 API Specification v1.0
ARI V1 — P0 API Specification Additive Revision v1.1

ARI V1 — P1-1 Backend Implementation Specification v1.0
ARI V1 — P1-2 Mobile App Implementation Specification v1.0
ARI V1 — P1-3 Web App Implementation Specification v1.0

ARI V1 — P2-1 Coding Execution Plan & Sprint Backlog v1.0
ARI V1 — P2-2 Monorepo & Local Development Setup v1.0
ARI V1 — P2-3 Backend Feature Foundation v1.0
ARI V1 — P2-4 Database and Alembic Migration Foundation v1.0
```

## 4.2 Frozen Architecture Rules

P2-5 must preserve:

```text
One Platform
One Backend
One Database Architecture
One Mobile App
One Web App
One Domain Model
One RBAC System
```

P2-5 must not introduce:

```text
Separate farmer app
Separate staff app
Separate admin backend
Separate web backend
New database architecture
New RBAC role
Permission service
Permission matrix engine
QR registry
Consultation entity
Owner registry
Farmer registry
Member registry
Block registry
Farm membership table
Knowledge graph
Vector database
RAG system
Internal AI assistant
Robot control module
Commerce module
Desktop app
Electron app
Flutter desktop app
```

---

# 5. Relationship to P2-1 / P2-2 / P2-3 / P2-4

## 5.1 Relationship to P2-1

P2-1 defines the coding order:

```text
1. Backend foundation
2. Database migrations
3. Auth and onboarding
4. Farm structure
5. Notebook / upload / sync
6. Mobile MVP
7. Web MVP
8. E2E test
9. Prototype deployment
10. Pilot
```

P2-5 corresponds to:

```text
Auth and onboarding
```

P2-5 remains before:

```text
Farm structure APIs
Notebook APIs
Upload / sync APIs
Mobile MVP
Web MVP
```

## 5.2 Relationship to P2-2

P2-2 created:

```text
backend/
mobile/
web/
infra/
docs/
scripts/
docker-compose.yml
.env.example
health endpoints
local Docker stack
```

P2-5 must preserve the existing local stack:

```text
api
postgres
minio
emqx
```

P2-5 must not modify the monorepo structure except for approved backend auth files.

## 5.3 Relationship to P2-3

P2-3 created generic backend foundation:

```text
Common response foundation
Common error foundation
Logging foundation
CORS foundation
Request ID middleware foundation
Configuration foundation
Database dependency placeholder
Repository base pattern
Service base pattern
Common schemas
Utilities
Foundation tests
```

P2-5 must implement auth using this foundation.

## 5.4 Relationship to P2-4

P2-4 created:

```text
SQLAlchemy models
Frozen database tables
Alembic env
Initial frozen schema migration
Frozen Python enums
Indexes and constraints
Nullable hierarchy rules
UTC timestamp rules
User additive fields from P0 v1.1
Phone uniqueness
registered_at
Database import / metadata / migration tests
API Gap documents
```

P2-5 must use the P2-4 database foundation.

P2-5 must not create new migrations unless a missing auth-required field is not present in P2-4 and the Owner approves the gap.

---

# 6. Current Backend State

## 6.1 Confirmed Health Contract

Existing endpoints must remain:

```text
GET /health
GET /api/v1/health
```

Expected response remains:

```json
{
  "status": "ok",
  "service": "ari-backend",
  "api": "/api/v1"
}
```

P2-5 must not break health endpoints.

## 6.2 Confirmed Database Foundation

P2-5 assumes these frozen tables exist after P2-4:

```text
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
```

Conditional tables:

```text
roles
user_roles
```

only if confirmed by P2-4 implementation.

P2-5 must not create new tables:

```text
auth_sessions
refresh_tokens
token_blacklist
farm_memberships
owners
members
farmers
permissions
qr_registry
consultations
knowledge
audit_logs
```

---

# 7. Auth and Onboarding Boundary

P2-5 is the first backend feature document that may implement real auth behavior.

Allowed feature boundary:

```text
Auth
User onboarding
Token issuing
Current user retrieval
Basic account guard
Basic membership guard
Minimal organization creation/assignment for owner registration
Minimal farm read lookup for family/staff join
```

Forbidden feature boundary:

```text
Farm CRUD
Zone CRUD
Tree CRUD
Notebook CRUD
Note Item CRUD
File upload
Upload queue processing
Sync batch
Notifications
Follow-ups
Approval UI
Full member management
Full RBAC matrix
Permission service
Permission matrix
ABAC
```

---

# 8. Allowed Implementation Scope

P2-5 may create or modify the following backend areas:

```text
backend/app/core/security.py
backend/app/core/enums.py only if enum constants already frozen and exist
backend/app/schemas/auth.py
backend/app/schemas/user.py only for auth response fields
backend/app/api/v1/auth.py
backend/app/services/auth_service.py
backend/app/services/user_service.py only for auth-required user operations
backend/app/services/organization_service.py only for owner org assignment/creation boundary
backend/app/repositories/users.py
backend/app/repositories/organizations.py minimal owner org create/lookup
backend/app/repositories/farms.py minimal farm lookup only
backend/app/dependencies/auth.py
backend/app/dependencies/rbac.py only for basic guard foundation
backend/app/api/v1/router.py include auth router
backend/tests/unit/
backend/tests/api/
backend/tests/services/
backend/tests/repositories/
backend/README.md if needed
docs/api-gaps/ if gap appears
```

P2-5 may not create new backend service boundaries outside this scope.

---

# 9. Out of Scope

P2-5 must not implement:

```text
Farm CRUD APIs
Zone APIs
Tree APIs
Notebook Entry APIs
Note Item APIs
Follow-Up APIs
Notification APIs
File upload APIs
Upload queue processing
Sync batch implementation
MinIO upload flow
Mobile app screens
Web app pages
Owner approval UI
Pending member approval web page
Full RBAC matrix
Permission service
Permission table
Farm membership table
Invite code system
OTP / SMS verification
Password reset
Email verification
Forced password change
Audit log system
Deployment
Production hardening
```

---

# 10. Frozen User Identity Rules

## 10.1 User Additive Fields

P2-5 must use:

```text
phone
farmer_status
membership_status
account_status
primary_farm_id
```

## 10.2 Farmer Status Values

Allowed:

```text
owner
owner_family
farm_staff
```

Important rule:

```text
farmer_status is not an RBAC role.
```

## 10.3 Membership Status Values

Allowed:

```text
pending_farm_approval
active
rejected
suspended
revoked
```

## 10.4 Account Status Values

Frozen P0 / P1 / P2 sources use:

```text
active
active_pending_verification
pending_review
suspended
rejected
revoked
```

Do not add:

```text
disabled
```

unless approved through API Gap / Revision Proposal.

## 10.5 Primary Farm Rule

```text
primary_farm_id nullable
```

Used mainly for:

```text
owner_family
farm_staff
```

For owner users:

```text
primary_farm_id may be null
```

because an owner may own multiple farms.

---

# 11. Corrected Account Status Rule

## 11.1 Disabled Status Handling

The P2-5 prompt draft mentions:

```text
disabled
```

However, `disabled` is not part of the frozen P0 / P1 account_status enum.

Current P2-5 rule:

```text
Do not implement disabled.
```

If Owner wants to add `disabled`, create:

```text
API Gap / Revision Proposal
```

Do not silently add it to database enum, Python enum, schemas, API responses, or tests.

## 11.2 Owner Default Account Status

P2-5 default rule:

```text
owner.account_status = active_pending_verification
owner.membership_status = active
```

Do not use:

```text
owner.account_status = active
owner.account_status = pending_review
```

as the default unless Owner explicitly approves a project-level policy change.

## 11.3 Family / Staff Default Account Status

For owner_family / farm_staff registration:

```text
account_status = active
membership_status = pending_farm_approval
```

This allows the user to log in and see pending approval state, but does not grant protected farm-scoped access until approval.

---

# 12. Corrected Roles / User Roles Boundary

## 12.1 Conditional Role Tables

P2-5 must not create new `roles` or `user_roles` tables.

However:

```text
If roles/user_roles already exist from confirmed P2-4 implementation,
P2-5 may use them only to assign the frozen role = farmer during registration.
```

## 12.2 Allowed Role Usage

Allowed:

```text
Assign frozen role = farmer to a newly registered mobile user
Include role claim in JWT if role exists in frozen model
Use existing role/user_roles structure if confirmed
```

## 12.3 Forbidden Role Changes

P2-5 must not:

```text
Create new RBAC roles
Create owner role
Create owner_family role
Create farm_staff role
Create permission service
Create permission matrix engine
Create ABAC
Create farm membership table
```

## 12.4 Important Rule

The following are not RBAC roles:

```text
owner
owner_family
farm_staff
```

They are onboarding classifications only under:

```text
farmer_status
```

---

# 13. Corrected Primary Farm ID Rule

## 13.1 Owner

For owner registration:

```text
primary_farm_id may be null
```

Reason:

```text
Owner may later create multiple farms.
P2-5 does not implement Farm CRUD.
```

## 13.2 Owner Family / Farm Staff

For owner_family / farm_staff registration, P2-5 may set:

```text
primary_farm_id = provided farm_id
```

during registration as onboarding/default farm context.

This does not grant farm access.

Actual protected farm access remains blocked until:

```text
membership_status = active
```

## 13.3 Access Boundary

For pending users:

```text
primary_farm_id may identify requested/default farm context
membership_status controls whether access is granted
```

So:

```text
primary_farm_id exists
```

does not mean:

```text
farm access is approved
```

---

# 14. Phone Normalization Strategy

## 14.1 Purpose

Phone number is the primary login identity for mobile self-registration users.

## 14.2 Backend Responsibility

Backend must normalize phone before:

```text
registration uniqueness check
database storage
login lookup
comparison
auth/me response if normalized format is preferred
```

## 14.3 P0 Pilot Normalization Rule

Recommended P2-5 pilot rule:

```text
Trim whitespace
Remove spaces and hyphens
Accept Thai local format: 0812345678
Accept international format: +66812345678
Normalize Thai local mobile numbers to +66 format if helper is implemented
Reject invalid length / non-phone input
```

## 14.4 Storage Rule

Store only one canonical normalized phone value in:

```text
users.phone
```

Do not store multiple phone formats in separate columns.

## 14.5 Error Cases

```text
invalid_phone_format
phone_already_exists
phone_required
```

---

# 15. Password Hashing Strategy

## 15.1 Required Rule

Never store plain text password.

Store only:

```text
password_hash
```

## 15.2 Recommended Library Boundary

Use a secure password hashing library such as:

```text
passlib[bcrypt]
```

or equivalent approved Python password hashing library.

## 15.3 P0 Pilot Default Password Rule

P1-2 allows a default password for pilot simplicity:

```text
1234
```

P2-5 must still hash this password before storage.

## 15.4 Forbidden

Do not log:

```text
plain password
password_hash
```

Do not return:

```text
password
password_hash
```

in API responses.

---

# 16. JWT Strategy

## 16.1 Token Types

P2-5 uses:

```text
Access Token
Refresh Token
```

## 16.2 Access Token Claims

Minimum access token claims:

```json
{
  "sub": "user_id",
  "role": "farmer",
  "organization_id": "uuid",
  "farmer_status": "owner",
  "membership_status": "active",
  "account_status": "active_pending_verification",
  "type": "access",
  "iat": "timestamp",
  "exp": "timestamp"
}
```

## 16.3 Refresh Token Claims

Minimum refresh token claims:

```json
{
  "sub": "user_id",
  "type": "refresh",
  "iat": "timestamp",
  "exp": "timestamp"
}
```

## 16.4 Token Secret Configuration

Required environment settings:

```text
JWT_SECRET_KEY
JWT_ALGORITHM
ACCESS_TOKEN_EXPIRE_MINUTES
REFRESH_TOKEN_EXPIRE_DAYS
```

Do not hard-code secrets.

## 16.5 Token Validation

Backend must validate:

```text
signature
expiration
token type
user exists
user account status
```

---

# 17. Refresh Token Boundary

## 17.1 Allowed in P2-5

P2-5 may implement signed stateless refresh tokens.

Flow:

```text
Client submits refresh_token
Backend validates signature and expiry
Backend loads user by sub
Backend checks account_status
Backend issues new access_token
Backend may issue new refresh_token if implemented
```

## 17.2 Not Allowed Without Revision

Do not create:

```text
refresh_tokens table
auth_sessions table
token_blacklist table
session service
```

unless frozen documents explicitly require it and Owner approves.

## 17.3 Logout Boundary

P2-5 logout may be:

```text
client-side token discard
```

If server-side logout invalidation is required, create API Gap / Revision Proposal.

---

# 18. Registration Flow

## 18.1 Endpoint

```http
POST /api/v1/auth/register
```

## 18.2 Request Body — Owner

```json
{
  "phone": "0812345678",
  "name": "Somchai",
  "password": "1234",
  "farmer_status": "owner",
  "farm_id": null
}
```

## 18.3 Request Body — Owner Family / Farm Staff

```json
{
  "phone": "0812345678",
  "name": "Somchai",
  "password": "1234",
  "farmer_status": "farm_staff",
  "farm_id": "uuid"
}
```

## 18.4 Backend Steps

```text
1. Validate request schema.
2. Normalize phone.
3. Check phone uniqueness.
4. Validate farmer_status.
5. Hash password.
6. Branch by farmer_status:
   - owner
   - owner_family
   - farm_staff
7. Create user.
8. Assign frozen role = farmer if roles/user_roles are confirmed.
9. Set organization_id.
10. Set membership_status.
11. Set account_status.
12. Set primary_farm_id if applicable.
13. Set registered_at if present in model.
14. Issue access_token.
15. Issue refresh_token.
16. Return auth response.
```

## 18.5 Response

```json
{
  "access_token": "jwt",
  "refresh_token": "jwt",
  "token_type": "bearer",
  "user": {
    "user_id": "uuid",
    "phone": "+66812345678",
    "name": "Somchai",
    "role": "farmer",
    "farmer_status": "owner",
    "organization_id": "uuid",
    "primary_farm_id": null,
    "membership_status": "active",
    "account_status": "active_pending_verification"
  }
}
```

---

# 19. Owner Registration Flow

## 19.1 Rule

When:

```text
farmer_status = owner
```

Backend must:

```text
Create user
Assign frozen role = farmer if role tables are confirmed
Create or assign organization_id immediately
Set membership_status = active
Set account_status = active_pending_verification
Return organization_id
Return access_token and refresh_token
```

## 19.2 Organization Assignment

P2-5 may create a minimal Organization record for owner onboarding if no owner organization exists.

Minimal organization creation may include:

```text
name derived from user name
type = existing frozen organization type only
status = existing frozen organization status only
created_at = UTC now
```

If P2-4 enum/model does not safely support organization type/status values, create API Gap / Revision Proposal instead of inventing values.

## 19.3 Owner Farm Creation Boundary

Owner may later create multiple farms, but P2-5 must not implement Farm CRUD.

Farm creation is deferred to:

```text
P2-6 Farm Structure Backend
```

---

# 20. Owner Family / Farm Staff Registration Flow

## 20.1 Rule

When:

```text
farmer_status = owner_family
```

or:

```text
farmer_status = farm_staff
```

Backend must require:

```text
farm_id
```

## 20.2 Backend Steps

```text
1. Validate farm_id is provided.
2. Lookup farm by existing farms table.
3. Reject if farm does not exist.
4. Resolve organization_id from farm.organization_id.
5. Create user.
6. Assign frozen role = farmer if role tables are confirmed.
7. Set primary_farm_id = provided farm_id as onboarding/default farm context.
8. Set membership_status = pending_farm_approval.
9. Set account_status = active.
10. Return access_token and refresh_token.
11. Restrict protected farm-scoped access until approval.
```

## 20.3 Pending Approval Message

Mobile may display:

```text
ส่งคำขอเข้าร่วมสวนแล้ว
กรุณารอเจ้าของสวนหรือผู้ดูแลระบบอนุมัติ
```

## 20.4 Access Rule

Before approval:

```text
membership_status = pending_farm_approval
```

Backend must block protected farm-scoped access.

After approval:

```text
membership_status = active
```

protected farm access may be allowed according to frozen RBAC and scope rules.

## 20.5 Forbidden

Do not create:

```text
farm_membership table
member registry
owner registry
farmer registry
invite code system
approval service
```

---

# 21. Phone Login Flow

## 21.1 Endpoint

```http
POST /api/v1/auth/login
```

## 21.2 Request Body

```json
{
  "phone": "0812345678",
  "password": "1234"
}
```

## 21.3 Backend Steps

```text
1. Validate request schema.
2. Normalize phone.
3. Find user by normalized phone.
4. Verify password_hash.
5. Check account_status.
6. Issue access_token.
7. Issue refresh_token.
8. Return auth response.
```

## 21.4 Email Login Compatibility

Email login may remain if already implemented, but P2-5 must prioritize phone login for mobile onboarding.

Do not remove existing email identity fields.

---

# 22. Current User Flow

## 22.1 Endpoint

```http
GET /api/v1/auth/me
```

## 22.2 Auth Requirement

Requires valid access token:

```text
Authorization: Bearer <access_token>
```

## 22.3 Response Body

```json
{
  "user_id": "uuid",
  "phone": "+66812345678",
  "name": "Somchai",
  "role": "farmer",
  "farmer_status": "owner",
  "organization_id": "uuid",
  "primary_farm_id": null,
  "membership_status": "active",
  "account_status": "active_pending_verification"
}
```

## 22.4 Rule

`/auth/me` must expose mobile onboarding state so mobile and web can decide what to display.

Mobile visibility is not authorization.

Backend remains authorization source of truth.

---

# 23. Account Status Guard

## 23.1 Purpose

Account status guard controls whether an account may use protected backend functions.

## 23.2 Allowed Account Status for Basic Access

For P2-5:

```text
active
active_pending_verification
```

may be allowed for basic authenticated access.

## 23.3 Blocked Account Status

```text
suspended
rejected
revoked
```

must be blocked from protected app functions.

## 23.4 Pending Review

```text
pending_review
```

requires project decision.

Recommended P2-5 behavior:

```text
Allow /auth/me
Allow /auth/logout
Block protected farm-scoped actions until resolved
```

If exact behavior is unclear, record API Gap.

---

# 24. Membership Status Guard

## 24.1 Purpose

Membership status controls farm participation lifecycle.

## 24.2 Active Membership

```text
membership_status = active
```

User may access approved farm scope if role and organization/farm scope allow it.

## 24.3 Pending Farm Approval

```text
membership_status = pending_farm_approval
```

Backend must block:

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

## 24.4 Rejected / Suspended / Revoked

Backend must block protected farm-scoped actions.

---

# 25. Corrected Guard Boundary

## 25.1 require_active_membership

P2-5 may implement:

```text
require_active_membership
```

only as a simple guard for blocking:

```text
pending_farm_approval
rejected
suspended
revoked
```

from protected farm-scoped access.

## 25.2 Not a Permission Service

`require_active_membership` is not:

```text
Permission service
Permission matrix
ABAC
Fine-grained authorization engine
Farm membership service
Approval workflow service
```

## 25.3 Deferred Scope Authorization

Full farm/organization scope authorization belongs to:

```text
P2-6 or later
```

Examples deferred:

```text
require_farm_access
require_organization_access
require_owner_or_scoped_role
full role matrix guards
approval authority guards
```

---

# 26. Auth Dependency Foundation

P2-5 may implement:

```text
get_current_user
require_authenticated_user
require_active_account
require_active_membership
```

## 26.1 get_current_user

Responsibilities:

```text
Read Authorization header
Decode access token
Validate token type
Load user from database
Return current user object
Raise 401 if invalid
```

## 26.2 require_active_account

Responsibilities:

```text
Check account_status
Raise 403 if blocked
```

## 26.3 require_active_membership

Responsibilities:

```text
Check membership_status
Raise 403 if pending/rejected/suspended/revoked for protected farm-scoped actions
```

## 26.4 Deferred Dependencies

Defer full dependencies to P2-6 or later:

```text
require_farm_access
require_organization_access
require_owner_or_scoped_role
full role matrix guards
approval authority guards
```

---

# 27. RBAC Boundary

## 27.1 Frozen Roles

Frozen RBAC roles remain:

```text
farmer
ari_staff
farm_coordinator
agronomist
reviewer
admin
root
```

## 27.2 Important Rule

Do not create RBAC roles:

```text
owner
owner_family
farm_staff
```

These are `farmer_status` values only.

## 27.3 Allowed in P2-5

Allowed:

```text
Basic role claim in JWT
Basic authenticated-user dependency
Basic active-account dependency
Basic active-membership dependency
Assign role = farmer if existing roles/user_roles structure is confirmed
```

## 27.4 Forbidden in P2-5

Forbidden:

```text
Permission service
Permission matrix engine
ABAC
New RBAC roles
owner role
owner_family role
farm_staff role
farm_membership table
fine-grained permission system
```

---

# 28. API Endpoint Specification

## 28.1 Register

```http
POST /api/v1/auth/register
```

Purpose:

```text
Mobile self-registration for owner / owner_family / farm_staff.
```

Errors:

```text
400 invalid_request
403 registration_not_allowed
404 farm_id_not_found
409 phone_already_exists
422 validation_error
500 server_error
```

## 28.2 Login

```http
POST /api/v1/auth/login
```

Purpose:

```text
Phone-number login.
```

Errors:

```text
400 invalid_request
401 invalid_credentials
403 account_blocked
422 validation_error
500 server_error
```

## 28.3 Refresh

```http
POST /api/v1/auth/refresh
```

Request:

```json
{
  "refresh_token": "jwt"
}
```

Response:

```json
{
  "access_token": "jwt",
  "refresh_token": "jwt",
  "token_type": "bearer"
}
```

Errors:

```text
401 invalid_or_expired_refresh_token
403 account_blocked
422 validation_error
500 server_error
```

## 28.4 Me

```http
GET /api/v1/auth/me
```

Purpose:

```text
Return current authenticated user and onboarding state.
```

Errors:

```text
401 unauthorized
403 account_blocked
404 user_not_found
500 server_error
```

## 28.5 Logout

```http
POST /api/v1/auth/logout
```

P2-5 behavior:

```text
Return success.
Client discards tokens.
No server-side token blacklist unless approved later.
```

Response:

```json
{
  "success": true
}
```

---

# 29. Schema Requirements

## 29.1 AuthRegisterRequest

```text
phone: required string
name: required string
password: required string
farmer_status: required enum
farm_id: required only for owner_family / farm_staff
```

## 29.2 AuthLoginRequest

```text
phone: required string
password: required string
```

## 29.3 AuthRefreshRequest

```text
refresh_token: required string
```

## 29.4 AuthUserResponse

```text
user_id
phone
name
role
farmer_status
organization_id
primary_farm_id
membership_status
account_status
```

## 29.5 AuthTokenResponse

```text
access_token
refresh_token
token_type
user
```

## 29.6 Validation Rules

```text
phone required
phone valid format
phone unique for registration
password required
farmer_status valid
farm_id required for owner_family / farm_staff
farm_id must exist for owner_family / farm_staff
```

---

# 30. Repository / Service / Router Pattern

## 30.1 Router Layer

Auth router handles:

```text
HTTP method/path
request schema validation
dependency injection
service call
response formatting
```

Router must not:

```text
perform SQL queries
hash passwords directly
decode token business logic directly
create organizations directly
```

## 30.2 Service Layer

Auth service handles:

```text
registration flow
login flow
refresh flow
current user lookup logic
password hash verification orchestration
token issuing orchestration
account/membership checks
```

## 30.3 Repository Layer

User repository handles:

```text
get_by_id
get_by_phone
create_user
phone_exists
```

Organization repository handles:

```text
create minimal organization for owner registration
```

Farm repository handles only:

```text
get_by_id for registration validation
```

P2-5 must not implement full Farm CRUD repository behavior.

---

# 31. Database Interaction Boundary

## 31.1 Allowed Tables

P2-5 may read/write:

```text
users
organizations
```

P2-5 may read only:

```text
farms
```

for owner_family / farm_staff registration validation.

P2-5 may use:

```text
roles
user_roles
```

only if confirmed by P2-4 and only for assigning frozen role = farmer.

## 31.2 Not Allowed Tables

Do not create or modify:

```text
farm_memberships
auth_sessions
refresh_tokens
token_blacklist
permissions
audit_logs
owners
members
farmers
qr_registry
consultations
knowledge
```

## 31.3 Migration Boundary

P2-5 should not create new migration files if P2-4 already implemented frozen user additive fields.

If a required field is missing, create API Gap / Revision Proposal.

---

# 32. Error Handling

Use existing P2-3 common error foundation.

Required error codes:

```text
invalid_phone_format
phone_already_exists
invalid_farmer_status
farm_id_required
farm_id_not_found
invalid_credentials
account_blocked
membership_pending_approval
membership_blocked
invalid_token
token_expired
invalid_refresh_token
validation_error
server_error
```

HTTP mapping:

```text
400 bad request
401 unauthorized
403 forbidden
404 not found
409 conflict
422 validation error
500 internal server error
```

Error response must follow the existing standard envelope.

---

# 33. Security Considerations

P2-5 must enforce:

```text
No plain password storage
No plain token storage in database unless approved
No password/token logs
JWT secret from environment only
Access token expiration
Refresh token expiration
Phone normalization before lookup
Phone uniqueness at database and service level
Generic invalid credential error
No user enumeration through login
No auth session table without approval
No token blacklist table without approval
```

P2-5 is not production hardening.

Deferred security features:

```text
OTP / SMS verification
MFA
rate limiting
device binding
server-side refresh token rotation table
password reset
email verification
audit logging
SIEM / log shipping
```

---

# 34. Testing Requirements

## 34.1 Unit Tests

Required:

```text
phone normalization
password hashing
password verification
JWT access token creation
JWT refresh token creation
JWT decode valid token
JWT reject expired/invalid token
account status guard
membership status guard
```

## 34.2 Service Tests

Required:

```text
register owner success
register owner creates/assigns organization_id
register owner sets role = farmer if roles/user_roles are confirmed
register owner sets membership_status = active
register owner sets account_status = active_pending_verification
register owner rejects duplicate phone
register owner stores password_hash only

register owner_family with valid Farm ID
register farm_staff with valid Farm ID
register owner_family/farm_staff rejects missing Farm ID
register owner_family/farm_staff rejects invalid Farm ID
register owner_family/farm_staff resolves organization_id from farm
register owner_family/farm_staff sets primary_farm_id as onboarding/default farm context
register owner_family/farm_staff sets membership_status = pending_farm_approval
register owner_family/farm_staff sets account_status = active
pending membership blocks protected farm-scoped access

login by phone success
login rejects wrong password
login rejects unknown phone
login blocks suspended/rejected/revoked accounts

refresh token success
refresh token rejects invalid token

auth/me returns onboarding state
```

## 34.3 API Tests

Required:

```text
POST /api/v1/auth/register owner
POST /api/v1/auth/register owner_family
POST /api/v1/auth/register farm_staff
POST /api/v1/auth/login
POST /api/v1/auth/refresh
GET /api/v1/auth/me
POST /api/v1/auth/logout
```

## 34.4 Regression Tests

Required:

```text
GET /health still PASS
GET /api/v1/health still PASS
alembic upgrade head still PASS
pytest still PASS
forbidden tables absent
forbidden modules absent
no disabled account_status enum unless approved
no new RBAC roles
```

---

# 35. Smoke Test Checklist

After P2-5 coding implementation is explicitly approved and completed:

```text
[ ] docker compose up works
[ ] api service starts
[ ] postgres service starts
[ ] GET /health returns expected response
[ ] GET /api/v1/health returns expected response
[ ] alembic upgrade head succeeds
[ ] pytest passes

[ ] register owner succeeds
[ ] register owner returns access_token / refresh_token
[ ] register owner returns organization_id
[ ] register owner returns membership_status = active
[ ] register owner returns account_status = active_pending_verification

[ ] register owner_family with valid farm_id succeeds
[ ] register farm_staff with valid farm_id succeeds
[ ] owner_family / farm_staff invalid farm_id returns 404
[ ] owner_family / farm_staff missing farm_id returns 422 or 400
[ ] owner_family / farm_staff primary_farm_id is onboarding/default context only
[ ] owner_family / farm_staff protected farm access is blocked until membership_status = active
[ ] duplicate phone returns 409

[ ] login by phone succeeds
[ ] login wrong password returns 401
[ ] /auth/me returns farmer_status / membership_status / account_status / primary_farm_id
[ ] refresh returns new access token
[ ] logout returns success

[ ] no farm CRUD endpoint is added by P2-5
[ ] no notebook endpoint is added by P2-5
[ ] no upload/sync endpoint is added by P2-5
[ ] no permission service exists
[ ] no farm_membership table exists
[ ] no owner/member/farmer registry exists
[ ] no disabled account_status is implemented unless approved
[ ] no owner/owner_family/farm_staff RBAC roles are created
```

---

# 36. P2-5 GitHub Issue Breakdown

## P2-5-01 — Auth Schema Foundation

Create auth request/response schemas.

Acceptance:

```text
AuthRegisterRequest
AuthLoginRequest
AuthRefreshRequest
AuthUserResponse
AuthTokenResponse
validation tests
```

## P2-5-02 — Security Utilities

Create password and JWT utilities.

Acceptance:

```text
hash_password
verify_password
create_access_token
create_refresh_token
decode_token
unit tests
```

## P2-5-03 — Phone Normalization Helper

Create phone normalization helper.

Acceptance:

```text
normalize_phone
reject invalid phone
consistent registration/login lookup
unit tests
```

## P2-5-04 — User Repository Auth Methods

Implement minimal user repository methods.

Acceptance:

```text
get_by_id
get_by_phone
phone_exists
create_user
no unrelated user management expansion
```

## P2-5-05 — Owner Registration Service

Implement owner registration flow.

Acceptance:

```text
role = farmer if roles/user_roles confirmed
organization_id created/assigned
membership_status = active
account_status = active_pending_verification
tokens returned
tests pass
```

## P2-5-06 — Family / Staff Registration Service

Implement Farm ID join flow.

Acceptance:

```text
farm_id required
farm_id exists
organization_id resolved from farm
primary_farm_id set as onboarding/default farm context
membership_status = pending_farm_approval
account_status = active
tokens returned
farm access blocked until approval
tests pass
```

## P2-5-07 — Login / Refresh / Me / Logout

Implement auth endpoints.

Acceptance:

```text
phone login works
refresh works within stateless token boundary
auth/me returns onboarding state
logout returns success
```

## P2-5-08 — Auth Dependencies and Guards

Implement basic auth dependencies.

Acceptance:

```text
get_current_user
require_active_account
require_active_membership
require_active_membership remains simple guard only
no permission service
no permission matrix
tests pass
```

## P2-5-09 — API Tests and Smoke Test Update

Add endpoint tests and update smoke checklist.

Acceptance:

```text
auth API tests pass
health tests still pass
alembic still passes
forbidden table/module tests pass if applicable
disabled account_status not implemented
new RBAC roles not implemented
```

## P2-5-10 — Documentation Update

Update backend README if needed.

Acceptance:

```text
auth endpoints documented
env vars documented
P2-5 boundary documented
forbidden additions listed
disabled account_status gap documented
roles/user_roles conditional handling documented
```

---

# 37. API Gap / Revision Proposal Handling

## 37.1 Rule

If frozen documents are unclear, missing, or inconsistent, do not invent behavior.

Create:

```text
API Gap / Revision Proposal
```

## 37.2 Storage Location

Recommended:

```text
docs/api-gaps/
```

## 37.3 Required Template

```markdown
# API Gap / Revision Proposal

## Gap ID
P2-5-GAP-XXX

## Related Document
P2-5 Auth and Mobile Onboarding Backend

## Source Conflict / Missing Detail
Describe the unclear point.

## Current Frozen Rule
Quote or summarize existing frozen rule.

## Implementation Risk
Describe risk if coding proceeds silently.

## Recommended Decision
Option A / Option B.

## Owner Decision
Pending / Approved / Rejected.

## Implementation Status
Not implemented until approved.
```

## 37.4 Expected P2-5 API Gaps

### P2-5-GAP-001 — Account Status `disabled`

The P2-5 prompt draft mentions:

```text
disabled
```

but frozen P0 Domain / P0 Database / P1-1 / P2-4 sources use:

```text
active
active_pending_verification
pending_review
suspended
rejected
revoked
```

Decision required if Owner wants to add:

```text
disabled
```

Current P2-5 rule:

```text
Do not implement disabled.
```

### P2-5-GAP-002 — Server-Side Refresh Token Persistence

Frozen scope allows refresh tokens but does not authorize:

```text
refresh_tokens table
auth_sessions table
token_blacklist table
```

Current P2-5 rule:

```text
Use signed stateless refresh token.
Client-side logout only.
```

### P2-5-GAP-003 — Organization Type Default for Owner Registration

If organization type enum requires exact value and no safe value exists, Owner decision required.

Current P2-5 rule:

```text
Do not invent enum value.
Use existing frozen enum value only.
```

### P2-5-GAP-004 — Pending Review Account Behavior

If `account_status = pending_review` appears in data, exact app access behavior may require Owner confirmation.

Current P2-5 recommendation:

```text
Allow auth/me and logout.
Block protected farm-scoped actions.
```

### P2-5-GAP-005 — Roles / User Roles Confirmation

P2-4 treats roles/user_roles as conditional.

Current P2-5 rule:

```text
Do not create roles/user_roles.
Use existing confirmed roles/user_roles only if P2-4 implementation already created them.
```

Owner or implementation status should confirm whether:

```text
roles
user_roles
```

exist before P2-5 coding starts.

---

# 38. Acceptance Criteria

P2-5 is acceptable only if:

```text
It follows frozen P0 / P1 / P2 documents
It does not redesign authentication architecture
It does not introduce new database architecture
It does not introduce new RBAC roles
It treats farmer_status as onboarding status, not RBAC role
It uses users table additive fields from P0 v1.1
It uses phone as login identity
It supports Owner / Owner Family / Farm Staff onboarding
It uses Farm ID as join reference for family/staff
It does not create farm_membership table
It does not create owner/member/farmer registry
It does not implement disabled account_status unless approved
It locks owner default account_status = active_pending_verification
It allows roles/user_roles only if already confirmed by P2-4
It does not implement Farm CRUD
It does not implement Notebook / Upload / Sync
It does not implement Mobile/Web
It defines require_active_membership as simple guard only
It does not create permission service or permission matrix
It defines clear coding boundary for Claude/Codex
It defines smoke tests and rollback criteria
It records unclear points as API Gap / Revision Proposal
```

---

# 39. Explicit Non-Goals

P2-5 does not authorize:

```text
P2-6 Farm Structure Backend
Farm CRUD
Zone CRUD
Tree CRUD
Notebook backend
Note Item backend
Follow-Up backend
Notification backend
File upload backend
Upload queue processor
Offline sync
Mobile screens
Web pages
Pending member approval UI
Owner approval UI
Full RBAC matrix
Permission service
Permission table
Farm membership table
OTP / SMS
Invite links
Password reset
Email verification
Production deployment
```

P2-5 must not create:

```text
farm_memberships table
owners table
members table
farmers table
permissions table
auth_sessions table
refresh_tokens table
token_blacklist table
qr_registry table
consultations table
knowledge table
audit_logs table
```

P2-5 must not create new:

```text
roles table
user_roles table
```

but may use existing confirmed role tables from P2-4 only to assign frozen role = farmer.

---

# 40. Ready for Owner Review Section

## 40.1 Review Checklist

```text
[ ] P2-5 scope is limited to auth and mobile onboarding backend
[ ] P2-5 does not create P2-6
[ ] P2-5 does not implement coding
[ ] P2-5 preserves One Platform / One Backend / One Database / One RBAC
[ ] P2-5 uses frozen User additive fields
[ ] P2-5 keeps farmer_status separate from RBAC roles
[ ] P2-5 uses Farm ID for owner_family / farm_staff join
[ ] P2-5 does not create farm_membership table
[ ] P2-5 does not create owner/member/farmer registry
[ ] P2-5 does not introduce token persistence tables
[ ] P2-5 records account_status disabled mismatch as API Gap
[ ] P2-5 locks owner default account_status = active_pending_verification
[ ] P2-5 clarifies primary_farm_id as onboarding/default context only for pending users
[ ] P2-5 allows roles/user_roles only if already confirmed by P2-4
[ ] P2-5 defines require_active_membership as simple guard only
[ ] P2-5 defers full farm/organization authorization to P2-6 or later
[ ] P2-5 defers Farm CRUD to P2-6
[ ] P2-5 defers Notebook / Upload / Sync to later P2 document
```

## 40.2 Final Statement

ARI V1 — P2-5 Auth and Mobile Onboarding Backend v1.0 defines the safe backend implementation boundary for authentication, phone login, JWT token handling, and mobile onboarding after the frozen database and Alembic foundation.

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

It implements only:

```text
Auth and mobile onboarding backend foundation
```

It does not implement:

```text
Farm CRUD
Notebook
Upload
Sync
Mobile App
Web App
New RBAC
New database tables
New registries
New architecture
```

```text
Document Status: Draft Final / Ready for Owner Review
Freeze Readiness: Ready after owner review
```
*****************************************************
2026-06-28
ARI V1 — P2-5 Auth and Mobile Onboarding Backend v1.0
Status: FROZEN
Freeze Confirmation: Owner confirmed
******************************************************
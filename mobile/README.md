# ARI Mobile App

ARI Agricultural Intelligence Platform — Flutter Mobile App (P2-8)

**Target Platforms:** Android, iOS  
**Flutter SDK:** >=3.19.0  
**Dart SDK:** >=3.3.0

---

## Architecture

```
mobile/
├── pubspec.yaml              # Dependencies
├── analysis_options.yaml     # Lint rules
├── lib/
│   ├── main.dart             # Entry point
│   ├── app.dart              # Provider wiring + MaterialApp
│   ├── app_router.dart       # Root routing (session restore / auth state)
│   ├── core/
│   │   ├── config/           # AppConfig — API base URL, timeouts
│   │   ├── auth/             # TokenStorage — secure Keychain/Keystore
│   │   ├── network/          # ApiClient — Bearer auth, refresh, error parsing
│   │   ├── storage/          # LocalDatabase (sqflite), LocalDraftStore, UploadQueueStore
│   │   ├── permissions/      # PermissionService — camera/mic/location/photos/notifications
│   │   ├── sync/             # SyncClient — POST /sync/batch (items[]/action)
│   │   ├── upload/           # UploadManager — upload-url → MinIO → complete
│   │   ├── errors/           # AppError sealed class hierarchy
│   │   └── utils/            # device_utils (stable device_id, UUID)
│   ├── shared/
│   │   ├── models/           # UserModel, FarmModel, ZoneModel, TreeModel,
│   │   │                     # NotebookEntryModel, NoteItemModel,
│   │   │                     # FollowUpModel, NotificationModel, UploadQueueItem
│   │   ├── providers/        # AuthProvider, FarmContextProvider, NetworkProvider
│   │   └── widgets/          # Shared widgets (AriLoadingIndicator, AriEmptyState, etc.)
│   └── features/
│       ├── auth/             # Login, Register screens
│       ├── onboarding/       # Permission onboarding, Pending approval
│       ├── home/             # Home screen (4 primary buttons + farm selector)
│       ├── farm_context/     # Farm selector screen
│       ├── farm_structure/   # Farm/Zone/Tree list, detail, create
│       ├── notebook/         # Notebook list, detail, add note, note item capture
│       ├── upload_queue/     # Upload queue screen
│       ├── follow_ups/       # Follow-up list, detail, outcome update
│       ├── notifications/    # Notification list, detail, mark read/all read
│       ├── ask_ai/           # Ask AI Now — placeholder (no AI engine in P2-8)
│       ├── qr_id/            # QR / ID helper (optional, camera scan deferred)
│       └── profile/          # Profile screen
├── test/
│   ├── unit/                 # Unit tests
│   ├── widget/               # Widget tests
│   └── helpers/              # Mock providers for tests
├── android/                  # Android native project
└── ios/                      # iOS native project
```

---

## Local Storage

Package: **sqflite** (structured relational queries for offline queue and ID mapping)

Tables:
- `local_notebook_entries` — offline notebook drafts
- `local_note_items` — offline note item timeline
- `upload_queue` — pending/failed/completed file uploads
- `id_mappings` — local_id → server_id after sync
- `sync_history` — batch sync audit

---

## State Management

Package: **provider** (ChangeNotifier-based)

Key providers:
- `AuthProvider` — session state, login, register, logout, refresh
- `FarmContextProvider` — active farm selection
- `NetworkProvider` — online/offline detection

---

## API Base URL Configuration

Set via `--dart-define` at build time:

```bash
flutter run --dart-define=ARI_API_BASE_URL=http://10.0.2.2:8000
```

Default (Android emulator): `http://10.0.2.2:8000`

---

## Running

```bash
# Install dependencies
flutter pub get

# Run on Android emulator
flutter run --dart-define=ARI_API_BASE_URL=http://10.0.2.2:8000

# Run on iOS simulator
flutter run --dart-define=ARI_API_BASE_URL=http://localhost:8000

# Build Android APK (debug)
flutter build apk --debug

# Run tests
flutter test
```

---

## Sync Contract

Uses P2-7 canonical payload format:

```json
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
```

**Does NOT use:** `operations[]` / `operation_type` (old P1-2 format).  
Reference: API-GAP-P2-7-011.

---

## client_id / local_id Rules

- `client_id` is generated once per record and **never regenerated on retry**
- `local_id` is generated once per record and **never regenerated on retry**
- `local_item_id` is generated once per item and **never regenerated on retry**
- `sequence_order` is set at item creation and **never changed on retry**
- After successful sync: `local_id → server_id` mapping stored in `id_mappings` table

**Known limitation:** Backend `notebook_entries` and `note_items` tables lack physical `client_id` columns. Duplicate prevention on backend is limited. See MOBILE-GAP-P2-8-015 and API-GAP-P2-7-017.

---

## File Upload Flow

1. Save local file
2. `POST /api/v1/files/upload-url` → get presigned MinIO URL
3. `PUT` binary directly to MinIO presigned URL
4. `POST /api/v1/files/complete`
5. Mark upload queue item as completed

On failure: `POST /api/v1/files/upload-failed` (best effort), mark failed, allow retry.

---

## Notebook Domain Rules

```
Notebook Entry = Note Session
Note Item = Timeline Item
Consultation = Notebook Entry type (not a separate entity)

Supported Entry types: note | consultation
Supported Item types: photo | video | voice | text | file | link

Save Local ≠ Upload ≠ Analyze
```

---

## Membership / Auth Rules

- `farmer_status` (owner/owner_family/farm_staff) controls UI visibility only
- Backend is the authorization authority (returns 403 for forbidden actions)
- `membership_status = pending_farm_approval` → blocks Add Note, Farm Notebook, Upload Queue, Sync
- No permission service / permission matrix / RBAC implemented in mobile

---

## Ask AI Now

P2-8: UI placeholder only. Allows creating consultation-type Notebook Entry.  
No internal AI engine, no LLM calls, no RAG.  
See MOBILE-GAP-P2-8-005.

---

## QR / ID

Optional representation-only helper.  
Parses `ari://farm/{id}`, `ari://zone/{id}`, `ari://tree/{id}` URIs.  
Camera QR scanning deferred — see MOBILE-GAP-P2-8-016.  
No QR registry, no new backend endpoint.

---

## API / Mobile Gaps

See [docs/api-gaps/MOBILE-GAP-P2-8.md](../docs/api-gaps/MOBILE-GAP-P2-8.md)

---

## Forbidden Scope (P2-8)

The following are explicitly NOT implemented:

- Backend migration or new backend API
- New backend table or entity
- Internal AI assistant / LLM / RAG / vector search
- QR registry / API / service
- Permission service / permission matrix / ABAC
- farm_memberships table
- Consultation entity / table / router
- Flutter Web or Flutter Desktop targets
- Push notification provider
- Backend scheduler
- Location table / GIS service
- Robot module / Commerce module
- OCR / Speech-to-text / Image recognition / Disease diagnosis

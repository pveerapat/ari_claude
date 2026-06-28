"""Sync service for P2-7.

Implements POST /api/v1/sync/batch.

Canonical payload format (P0 API spec):
  items[] with action field

API-GAP-P2-7-011: P1-2 Mobile uses operations[] / operation_type.
This implementation follows items[] / action only.

API-GAP-P2-7-012: Transaction policy: each item in the batch is processed
independently. A failure in one item does not roll back successful items.
Per-item status is returned in the results array.

API-GAP-P2-7-017: client_id/device_id are not stored on notebook_entries table.
Idempotency is best-effort: we check upload_queue for duplicate client_ids.
"""
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.enums import EntryContext, EntryType, UserRole
from app.core.errors import AppError
from app.models.user import User
from app.repositories.notebook_entries import NotebookEntryRepository
from app.repositories.upload_queue import UploadQueueRepository
from app.schemas.sync import SyncBatchRequest, SyncBatchResponse, SyncItem, SyncItemResult
from app.services.base import BaseService

_PRIVILEGED_ROLES = {UserRole.admin, UserRole.root, UserRole.ari_staff}

_SUPPORTED_ENTITY_TYPES = {"notebook_entry", "note_item"}
_SUPPORTED_ACTIONS = {"create", "update"}


def _is_privileged(user: User) -> bool:
    return user.role in _PRIVILEGED_ROLES


class SyncService(BaseService):
    def __init__(self, db: Session) -> None:
        self.db = db
        self.entry_repo = NotebookEntryRepository(db)
        self.queue_repo = UploadQueueRepository(db)

    def _process_item(self, user: User, item: SyncItem) -> SyncItemResult:
        if item.entity_type not in _SUPPORTED_ENTITY_TYPES:
            return SyncItemResult(
                client_id=item.client_id,
                status="failed",
                error=f"Unsupported entity_type: {item.entity_type}",
            )
        if item.action not in _SUPPORTED_ACTIONS:
            return SyncItemResult(
                client_id=item.client_id,
                status="failed",
                error=f"Unsupported action: {item.action}",
            )

        try:
            if item.entity_type == "notebook_entry" and item.action == "create":
                return self._sync_create_notebook_entry(user, item)
            return SyncItemResult(
                client_id=item.client_id,
                status="failed",
                error=f"Combination {item.entity_type}/{item.action} is not yet implemented",
            )
        except AppError as exc:
            return SyncItemResult(
                client_id=item.client_id,
                status="failed",
                error=exc.message,
            )
        except Exception as exc:
            return SyncItemResult(
                client_id=item.client_id,
                status="failed",
                error="Internal error processing sync item",
            )

    def _sync_create_notebook_entry(self, user: User, item: SyncItem) -> SyncItemResult:
        payload = item.payload

        existing = self.queue_repo.get_by_client_id_and_user(str(item.client_id), None)
        if existing and existing.upload_action == "create" and existing.upload_entity_type == "notebook_entry":
            if existing.entry_id:
                return SyncItemResult(
                    client_id=item.client_id,
                    server_id=existing.entry_id,
                    status="completed",
                )

        org_id_str = payload.get("organization_id")
        if not org_id_str:
            return SyncItemResult(
                client_id=item.client_id,
                status="failed",
                error="organization_id is required in payload",
            )
        try:
            org_id = UUID(str(org_id_str))
        except (ValueError, AttributeError):
            return SyncItemResult(
                client_id=item.client_id,
                status="failed",
                error="Invalid organization_id in payload",
            )

        if not _is_privileged(user) and user.organization_id != org_id:
            return SyncItemResult(
                client_id=item.client_id,
                status="failed",
                error="Organization not accessible",
            )

        entry_type_str = payload.get("entry_type", "note")
        entry_context_str = payload.get("entry_context", "general_note")

        try:
            entry_type = EntryType(entry_type_str)
            entry_context = EntryContext(entry_context_str)
        except ValueError as exc:
            return SyncItemResult(
                client_id=item.client_id,
                status="failed",
                error=f"Invalid enum value: {exc}",
            )

        farm_id = UUID(payload["farm_id"]) if payload.get("farm_id") else None
        zone_id = UUID(payload["zone_id"]) if payload.get("zone_id") else None
        tree_id = UUID(payload["tree_id"]) if payload.get("tree_id") else None

        entry = self.entry_repo.create(
            organization_id=org_id,
            created_by_user_id=user.id,
            entry_type=entry_type,
            entry_context=entry_context,
            farm_id=farm_id,
            zone_id=zone_id,
            tree_id=tree_id,
            title=payload.get("title"),
            summary=payload.get("summary"),
        )
        self.db.flush()

        self.queue_repo.create(
            client_id=str(item.client_id),
            upload_entity_type="notebook_entry",
            upload_action="create",
            entry_id=entry.id,
        )
        self.db.flush()

        return SyncItemResult(
            client_id=item.client_id,
            server_id=entry.id,
            status="completed",
        )

    def process_batch(self, user: User, req: SyncBatchRequest) -> SyncBatchResponse:
        results = []
        for item in req.items:
            result = self._process_item(user, item)
            results.append(result)

        try:
            self.db.commit()
        except Exception:
            self.db.rollback()
            results = [
                SyncItemResult(client_id=r.client_id, status="failed", error="Commit failed")
                for r in results
            ]

        return SyncBatchResponse(
            client_batch_id=req.client_batch_id,
            results=results,
        )

"""Note Item service for P2-7.

sequence_order rules (API-GAP-P2-7-004):
- If sequence_order is provided, use it as-is.
- If not provided, auto-assign as max(sequence_order) + 1 for the entry.

Validation rules:
- text items require content_text
- link items require url
- photo/video/voice/file items should have file_path (enforced by API layer)
"""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.enums import ItemType, UserRole
from app.core.errors import AppError
from app.models.note_item import NoteItem
from app.models.user import User
from app.repositories.note_items import NoteItemRepository
from app.repositories.notebook_entries import NotebookEntryRepository
from app.schemas.note_item import NoteItemCreate, NoteItemUpdate
from app.services.base import BaseService

_PRIVILEGED_ROLES = {UserRole.admin, UserRole.root, UserRole.ari_staff}


def _is_privileged(user: User) -> bool:
    return user.role in _PRIVILEGED_ROLES


class NoteItemService(BaseService):
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = NoteItemRepository(db)
        self.entry_repo = NotebookEntryRepository(db)

    def _get_accessible_entry(self, user: User, entry_id: UUID):
        entry = self.entry_repo.get_by_id(entry_id)
        if not entry:
            raise AppError("entry_not_found", "Notebook entry not found", 404)
        if not _is_privileged(user) and entry.organization_id != user.organization_id:
            raise AppError("entry_not_accessible", "Notebook entry is not accessible", 403)
        return entry

    def list_items(self, user: User, entry_id: UUID) -> list[NoteItem]:
        self._get_accessible_entry(user, entry_id)
        return self.repo.list_by_entry(entry_id)

    def create_item(self, user: User, entry_id: UUID, req: NoteItemCreate) -> NoteItem:
        self._get_accessible_entry(user, entry_id)

        if req.item_type == ItemType.text and not req.content_text:
            raise AppError("content_text_required", "content_text is required for text items", 422)
        if req.item_type == ItemType.link and not req.url:
            raise AppError("url_required", "url is required for link items", 422)

        if req.sequence_order is not None:
            seq = req.sequence_order
        else:
            seq = self.repo.max_sequence_order(entry_id) + 1

        item = self.repo.create(
            entry_id=entry_id,
            item_type=req.item_type,
            sequence_order=seq,
            content_text=req.content_text,
            file_path=req.file_path,
            url=req.url,
            platform=req.platform,
            content_type=req.content_type,
            file_size=req.file_size,
            upload_status=req.upload_status,
        )
        self.db.commit()
        self.db.refresh(item)
        return item

    def update_item(self, user: User, item_id: UUID, req: NoteItemUpdate) -> NoteItem:
        item = self.repo.get_by_id(item_id)
        if not item:
            raise AppError("item_not_found", "Note item not found", 404)
        self._get_accessible_entry(user, item.entry_id)

        updates: dict = {}
        if "sequence_order" in req.model_fields_set and req.sequence_order is not None:
            updates["sequence_order"] = req.sequence_order
        if "content_text" in req.model_fields_set:
            updates["content_text"] = req.content_text
        if "file_path" in req.model_fields_set:
            updates["file_path"] = req.file_path
        if "url" in req.model_fields_set:
            updates["url"] = req.url
        if "upload_status" in req.model_fields_set:
            updates["upload_status"] = req.upload_status

        if updates:
            item = self.repo.update(item, updates)
        self.db.commit()
        self.db.refresh(item)
        return item

    def get_item(self, user: User, item_id: UUID) -> NoteItem:
        item = self.repo.get_by_id(item_id)
        if not item:
            raise AppError("item_not_found", "Note item not found", 404)
        self._get_accessible_entry(user, item.entry_id)
        return item

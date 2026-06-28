from typing import Optional
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.enums import ItemType, UploadStatus
from app.models.note_item import NoteItem
from app.repositories.base import BaseRepository


class NoteItemRepository(BaseRepository[NoteItem]):
    def __init__(self, db: Session) -> None:
        super().__init__(NoteItem, db)

    def get_by_id(self, item_id: UUID) -> NoteItem | None:
        return self.db.query(NoteItem).filter(NoteItem.id == item_id).first()

    def list_by_entry(self, entry_id: UUID) -> list[NoteItem]:
        return (
            self.db.query(NoteItem)
            .filter(NoteItem.entry_id == entry_id)
            .order_by(NoteItem.sequence_order.asc())
            .all()
        )

    def max_sequence_order(self, entry_id: UUID) -> int:
        result = (
            self.db.query(func.max(NoteItem.sequence_order))
            .filter(NoteItem.entry_id == entry_id)
            .scalar()
        )
        return result or 0

    def create(
        self,
        entry_id: UUID,
        item_type: ItemType,
        sequence_order: int,
        content_text: Optional[str] = None,
        file_path: Optional[str] = None,
        url: Optional[str] = None,
        platform: Optional[str] = None,
        content_type: Optional[str] = None,
        file_size: Optional[int] = None,
        upload_status: Optional[UploadStatus] = None,
    ) -> NoteItem:
        item = NoteItem(
            entry_id=entry_id,
            item_type=item_type,
            sequence_order=sequence_order,
            content_text=content_text,
            file_path=file_path,
            url=url,
            platform=platform,
            content_type=content_type,
            file_size=file_size,
            upload_status=upload_status,
        )
        self.db.add(item)
        self.db.flush()
        return item

    def update(self, item: NoteItem, updates: dict) -> NoteItem:
        for key, value in updates.items():
            setattr(item, key, value)
        self.db.flush()
        return item

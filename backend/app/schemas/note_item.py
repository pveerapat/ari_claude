from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.core.enums import ItemType, UploadStatus


class NoteItemCreate(BaseModel):
    item_type: ItemType
    sequence_order: Optional[int] = None
    content_text: Optional[str] = None
    file_path: Optional[str] = None
    url: Optional[str] = None
    platform: Optional[str] = None
    content_type: Optional[str] = None
    file_size: Optional[int] = None
    upload_status: Optional[UploadStatus] = None


class NoteItemUpdate(BaseModel):
    sequence_order: Optional[int] = None
    content_text: Optional[str] = None
    file_path: Optional[str] = None
    url: Optional[str] = None
    upload_status: Optional[UploadStatus] = None


class NoteItemRead(BaseModel):
    item_id: UUID
    entry_id: UUID
    item_type: ItemType
    sequence_order: int
    content_text: Optional[str] = None
    file_path: Optional[str] = None
    url: Optional[str] = None
    platform: Optional[str] = None
    upload_status: Optional[UploadStatus] = None
    created_at: datetime

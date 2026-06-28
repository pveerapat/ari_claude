from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.core.enums import UploadStatus


class UploadQueueCreate(BaseModel):
    client_id: str
    entry_id: Optional[UUID] = None
    upload_entity_type: str
    upload_action: str
    status: UploadStatus = UploadStatus.pending


class UploadQueueUpdate(BaseModel):
    status: Optional[UploadStatus] = None
    retry_count: Optional[int] = None
    error_message: Optional[str] = None


class UploadQueueRead(BaseModel):
    queue_id: UUID
    entry_id: Optional[UUID] = None
    client_id: Optional[str] = None
    upload_entity_type: Optional[str] = None
    upload_action: Optional[str] = None
    status: UploadStatus
    retry_count: int
    error_message: Optional[str] = None
    created_at: datetime
    uploaded_at: Optional[datetime] = None

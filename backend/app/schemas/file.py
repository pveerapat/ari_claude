from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.core.enums import ItemType


class UploadUrlRequest(BaseModel):
    entry_id: UUID
    item_type: ItemType
    file_name: str
    content_type: str
    file_size: int


class UploadUrlResponse(BaseModel):
    file_key: str
    upload_url: str
    expires_in: int = 900


class FileCompleteRequest(BaseModel):
    entry_id: UUID
    file_key: str
    upload_status: str = "completed"


class FileFailedRequest(BaseModel):
    entry_id: UUID
    file_key: str
    reason: Optional[str] = None

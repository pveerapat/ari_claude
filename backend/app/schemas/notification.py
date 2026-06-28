from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel


class NotificationRead(BaseModel):
    notification_id: UUID
    user_id: UUID
    type: str
    message: str
    status: str
    read_at: Optional[datetime] = None
    created_at: datetime

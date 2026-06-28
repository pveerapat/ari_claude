from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class TreeCreate(BaseModel):
    zone_id: UUID
    tree_code: str = Field(..., min_length=1, max_length=100)
    status: Optional[str] = None


class TreeUpdate(BaseModel):
    tree_code: Optional[str] = Field(None, min_length=1, max_length=100)
    status: Optional[str] = None


class TreeRead(BaseModel):
    tree_id: UUID
    zone_id: UUID
    tree_code: str
    status: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

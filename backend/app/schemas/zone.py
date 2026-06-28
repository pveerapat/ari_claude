from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class ZoneCreate(BaseModel):
    farm_id: UUID
    zone_name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None


class ZoneUpdate(BaseModel):
    zone_name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None


class ZoneRead(BaseModel):
    zone_id: UUID
    farm_id: UUID
    zone_name: str
    description: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

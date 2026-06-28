from datetime import datetime
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel, Field, field_validator


class LocationData(BaseModel):
    province: Optional[str] = None
    district: Optional[str] = None
    subdistrict: Optional[str] = None
    address: Optional[str] = None
    gps_latitude: Optional[float] = None
    gps_longitude: Optional[float] = None
    source: Optional[str] = None

    @field_validator("gps_latitude")
    @classmethod
    def validate_latitude(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and not (-90.0 <= v <= 90.0):
            raise ValueError("gps_latitude must be between -90 and 90")
        return v

    @field_validator("gps_longitude")
    @classmethod
    def validate_longitude(cls, v: Optional[float]) -> Optional[float]:
        if v is not None and not (-180.0 <= v <= 180.0):
            raise ValueError("gps_longitude must be between -180 and 180")
        return v


class FarmCreate(BaseModel):
    farm_name: str = Field(..., min_length=1, max_length=255)
    location: Optional[LocationData] = None
    description: Optional[str] = None


class FarmUpdate(BaseModel):
    farm_name: Optional[str] = Field(None, min_length=1, max_length=255)
    location: Optional[LocationData] = None
    description: Optional[str] = None


class FarmRead(BaseModel):
    farm_id: UUID
    organization_id: UUID
    farm_name: str
    location: Optional[Any] = None
    description: Optional[str] = None
    status: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, field_validator

from app.core.enums import FollowUpOutcome

_VALID_DAYS = {3, 7, 14}


class FollowUpCreate(BaseModel):
    entry_id: UUID
    follow_up_day: int

    @field_validator("follow_up_day")
    @classmethod
    def validate_follow_up_day(cls, v: int) -> int:
        if v not in _VALID_DAYS:
            raise ValueError(f"follow_up_day must be one of {sorted(_VALID_DAYS)}")
        return v


class FollowUpUpdate(BaseModel):
    outcome: Optional[FollowUpOutcome] = None
    notes: Optional[str] = None


class FollowUpRead(BaseModel):
    follow_up_id: UUID
    entry_id: UUID
    follow_up_day: int
    outcome: Optional[FollowUpOutcome] = None
    notes: Optional[str] = None
    recorded_at: datetime

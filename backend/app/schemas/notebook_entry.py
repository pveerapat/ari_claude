from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.core.enums import EntryContext, EntryType, ExternalAI


class NotebookEntryCreate(BaseModel):
    client_id: Optional[UUID] = None
    organization_id: UUID
    farm_id: Optional[UUID] = None
    zone_id: Optional[UUID] = None
    tree_id: Optional[UUID] = None
    entry_type: EntryType
    entry_context: EntryContext
    title: Optional[str] = None
    summary: Optional[str] = None
    analysis_status: Optional[str] = "not_started"
    ai_provider: Optional[ExternalAI] = None
    ai_usefulness_status: Optional[str] = None
    learned_summary: Optional[str] = None


class NotebookEntryUpdate(BaseModel):
    title: Optional[str] = None
    summary: Optional[str] = None
    farm_id: Optional[UUID] = None
    zone_id: Optional[UUID] = None
    tree_id: Optional[UUID] = None
    analysis_status: Optional[str] = None
    ai_provider: Optional[ExternalAI] = None
    ai_usefulness_status: Optional[str] = None
    learned_summary: Optional[str] = None


class NotebookEntryRead(BaseModel):
    entry_id: UUID
    organization_id: UUID
    created_by_user_id: UUID
    farm_id: Optional[UUID] = None
    zone_id: Optional[UUID] = None
    tree_id: Optional[UUID] = None
    entry_type: EntryType
    entry_context: EntryContext
    title: Optional[str] = None
    summary: Optional[str] = None
    suggested_category: Optional[str] = None
    analysis_status: str
    ai_provider: Optional[ExternalAI] = None
    ai_usefulness_status: Optional[str] = None
    learned_summary: Optional[str] = None
    created_at: datetime
    updated_at: datetime

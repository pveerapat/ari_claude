"""Sync batch schemas.

API-GAP-P2-7-011: P0 API spec uses items[]/action format.
P1-2 Mobile spec uses operations[]/operation_type format.
This implementation follows the frozen P0 API spec (items[]/action).
"""
from typing import Any, Optional
from uuid import UUID

from pydantic import BaseModel


class SyncItem(BaseModel):
    client_id: UUID
    entity_type: str
    action: str
    payload: dict[str, Any] = {}


class SyncBatchRequest(BaseModel):
    device_id: UUID
    client_batch_id: UUID
    items: list[SyncItem]


class SyncItemResult(BaseModel):
    client_id: UUID
    server_id: Optional[UUID] = None
    status: str
    error: Optional[str] = None


class SyncBatchResponse(BaseModel):
    client_batch_id: UUID
    results: list[SyncItemResult]

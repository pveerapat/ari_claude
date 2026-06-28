"""Sync batch API endpoint for P2-7.

Canonical path: POST /api/v1/sync/batch
Canonical payload: items[] / action (P0 API spec)

API-GAP-P2-7-011: P1-2 Mobile uses operations[] / operation_type.
This implementation supports items[] / action only.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.response import success_response
from app.dependencies.auth import require_active_membership
from app.dependencies.db import get_db
from app.models.user import User
from app.schemas.sync import SyncBatchRequest
from app.services.sync_service import SyncService

router = APIRouter(prefix="/sync", tags=["sync"])


@router.post("/batch")
def sync_batch(
    req: SyncBatchRequest,
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = SyncService(db)
    result = svc.process_batch(user=user, req=req)
    return success_response({
        "client_batch_id": str(result.client_batch_id),
        "results": [
            {
                "client_id": str(r.client_id),
                "server_id": str(r.server_id) if r.server_id else None,
                "status": r.status,
                "error": r.error,
            }
            for r in result.results
        ],
    })

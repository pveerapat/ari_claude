"""Upload Queue API endpoints for P2-7.

Canonical path: /api/v1/upload-queue (NOT /api/v1/upload-jobs)
Canonical table: upload_queue
Python model: UploadJob

API-GAP-P2-7-010: This path is confirmed as upload-queue.
No /api/v1/upload-jobs endpoint exists.
"""
from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.response import list_response, success_response
from app.dependencies.auth import require_active_membership
from app.dependencies.db import get_db
from app.models.upload_job import UploadJob
from app.models.user import User
from app.schemas.upload_queue import UploadQueueCreate, UploadQueueUpdate
from app.services.upload_queue_service import UploadQueueService

router = APIRouter(prefix="/upload-queue", tags=["upload-queue"])


def _queue_dict(job: UploadJob) -> dict:
    return {
        "queue_id": str(job.id),
        "entry_id": str(job.entry_id) if job.entry_id else None,
        "client_id": job.client_id,
        "upload_entity_type": job.upload_entity_type,
        "upload_action": job.upload_action,
        "status": job.status.value if job.status else None,
        "retry_count": job.retry_count,
        "error_message": job.error_message,
        "created_at": job.created_at.isoformat() if job.created_at else None,
        "uploaded_at": job.uploaded_at.isoformat() if job.uploaded_at else None,
    }


@router.post("")
def create_queue_record(
    req: UploadQueueCreate,
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = UploadQueueService(db)
    job = svc.create_queue_record(user=user, req=req)
    return success_response(_queue_dict(job))


@router.get("")
def list_queue(
    status: Optional[str] = Query(None),
    upload_entity_type: Optional[str] = Query(None),
    upload_action: Optional[str] = Query(None),
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1, le=100),
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = UploadQueueService(db)
    jobs, total = svc.list_queue(
        user=user,
        status=status,
        upload_entity_type=upload_entity_type,
        upload_action=upload_action,
        page=page,
        page_size=page_size,
    )
    return list_response([_queue_dict(j) for j in jobs], page, page_size, total)


@router.get("/{queue_id}")
def get_queue_record(
    queue_id: UUID,
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = UploadQueueService(db)
    job = svc.get_queue_record(user=user, queue_id=queue_id)
    return success_response(_queue_dict(job))


@router.patch("/{queue_id}")
def update_queue_record(
    queue_id: UUID,
    req: UploadQueueUpdate,
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = UploadQueueService(db)
    job = svc.update_queue_record(user=user, queue_id=queue_id, req=req)
    return success_response(_queue_dict(job))


@router.post("/{queue_id}/retry")
def retry_queue_record(
    queue_id: UUID,
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = UploadQueueService(db)
    job = svc.retry_queue_record(user=user, queue_id=queue_id)
    return success_response(_queue_dict(job))

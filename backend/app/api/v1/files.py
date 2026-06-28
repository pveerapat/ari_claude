"""File upload API endpoints for P2-7.

Canonical paths (frozen - do not rename):
  POST /api/v1/files/upload-url
  POST /api/v1/files/complete
  POST /api/v1/files/upload-failed

API-GAP-P2-7-006: Alternative naming (presign, confirm, etc.) is NOT supported.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.response import success_response
from app.dependencies.auth import require_active_membership
from app.dependencies.db import get_db
from app.models.user import User
from app.schemas.file import FileCompleteRequest, FileFailedRequest, UploadUrlRequest
from app.services.file_service import FileService

router = APIRouter(prefix="/files", tags=["files"])


@router.post("/upload-url")
def create_upload_url(
    req: UploadUrlRequest,
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = FileService(db)
    result = svc.generate_upload_url(user=user, req=req)
    return success_response(result)


@router.post("/complete")
def complete_upload(
    req: FileCompleteRequest,
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = FileService(db)
    result = svc.complete_upload(user=user, req=req)
    return success_response(result)


@router.post("/upload-failed")
def report_upload_failed(
    req: FileFailedRequest,
    user: User = Depends(require_active_membership),
    db: Session = Depends(get_db),
):
    svc = FileService(db)
    result = svc.record_upload_failed(user=user, req=req)
    return success_response(result)

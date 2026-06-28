"""Upload Queue service for P2-7.

The upload_queue table is the canonical table for tracking offline upload lifecycle.
Python class: UploadJob (maps to upload_queue table).
API path: /api/v1/upload-queue

API-GAP-P2-7-009: UploadJob is the Python name; upload_queue is the table/API name.
No separate upload_jobs table or /api/v1/upload-jobs endpoint is created.

client_id idempotency: UploadJob.client_id exists in the model.
Retry reuses the same queue record (reset status to pending, increment retry_count).
"""
from typing import Optional
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.enums import UploadStatus, UserRole
from app.core.errors import AppError
from app.models.upload_job import UploadJob
from app.models.user import User
from app.repositories.notebook_entries import NotebookEntryRepository
from app.repositories.upload_queue import UploadQueueRepository
from app.schemas.upload_queue import UploadQueueCreate, UploadQueueUpdate
from app.services.base import BaseService
from app.utils.pagination import calc_offset, clamp_page, clamp_page_size

_PRIVILEGED_ROLES = {UserRole.admin, UserRole.root, UserRole.ari_staff}


def _is_privileged(user: User) -> bool:
    return user.role in _PRIVILEGED_ROLES


class UploadQueueService(BaseService):
    def __init__(self, db: Session) -> None:
        self.db = db
        self.repo = UploadQueueRepository(db)
        self.entry_repo = NotebookEntryRepository(db)

    def _assert_queue_access(self, user: User, job: UploadJob) -> None:
        if _is_privileged(user):
            return
        if job.entry_id:
            entry = self.entry_repo.get_by_id(job.entry_id)
            if entry and entry.organization_id != user.organization_id:
                raise AppError("upload_queue_not_accessible", "Upload queue record is not accessible", 403)

    def list_queue(
        self,
        user: User,
        status: Optional[str] = None,
        upload_entity_type: Optional[str] = None,
        upload_action: Optional[str] = None,
        page: int = 1,
        page_size: int = 20,
    ) -> tuple[list[UploadJob], int]:
        page = clamp_page(page)
        page_size = clamp_page_size(page_size)
        offset = calc_offset(page, page_size)

        jobs = self.repo.list_all(status, upload_entity_type, upload_action, offset, page_size)
        total = self.repo.count_all(status, upload_entity_type, upload_action)
        return jobs, total

    def get_queue_record(self, user: User, queue_id: UUID) -> UploadJob:
        job = self.repo.get_by_id(queue_id)
        if not job:
            raise AppError("queue_record_not_found", "Upload queue record not found", 404)
        self._assert_queue_access(user, job)
        return job

    def create_queue_record(self, user: User, req: UploadQueueCreate) -> UploadJob:
        existing = self.repo.get_by_client_id_and_user(req.client_id, req.entry_id)
        if existing:
            return existing

        if req.entry_id:
            entry = self.entry_repo.get_by_id(req.entry_id)
            if not entry:
                raise AppError("entry_not_found", "Notebook entry not found", 404)
            if not _is_privileged(user) and entry.organization_id != user.organization_id:
                raise AppError("entry_not_accessible", "Notebook entry is not accessible", 403)

        job = self.repo.create(
            client_id=req.client_id,
            upload_entity_type=req.upload_entity_type,
            upload_action=req.upload_action,
            entry_id=req.entry_id,
            status=req.status,
        )
        self.db.commit()
        self.db.refresh(job)
        return job

    def update_queue_record(
        self, user: User, queue_id: UUID, req: UploadQueueUpdate
    ) -> UploadJob:
        job = self.repo.get_by_id(queue_id)
        if not job:
            raise AppError("queue_record_not_found", "Upload queue record not found", 404)
        self._assert_queue_access(user, job)

        updates: dict = {}
        if "status" in req.model_fields_set and req.status is not None:
            updates["status"] = req.status
        if "retry_count" in req.model_fields_set and req.retry_count is not None:
            updates["retry_count"] = req.retry_count
        if "error_message" in req.model_fields_set:
            updates["error_message"] = req.error_message

        if req.status == UploadStatus.completed:
            from app.utils.datetime import utcnow
            updates["uploaded_at"] = utcnow()

        if updates:
            job = self.repo.update(job, updates)
        self.db.commit()
        self.db.refresh(job)
        return job

    def retry_queue_record(self, user: User, queue_id: UUID) -> UploadJob:
        job = self.repo.get_by_id(queue_id)
        if not job:
            raise AppError("queue_record_not_found", "Upload queue record not found", 404)
        self._assert_queue_access(user, job)

        if job.status not in (UploadStatus.failed, UploadStatus.pending):
            raise AppError(
                "retry_not_allowed",
                "Retry is only allowed for failed or pending queue records",
                409,
            )

        job = self.repo.reset_for_retry(job)
        self.db.commit()
        self.db.refresh(job)
        return job

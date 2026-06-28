from typing import Optional
from uuid import UUID

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.enums import UploadStatus
from app.models.upload_job import UploadJob
from app.repositories.base import BaseRepository


class UploadQueueRepository(BaseRepository[UploadJob]):
    def __init__(self, db: Session) -> None:
        super().__init__(UploadJob, db)

    def get_by_id(self, queue_id: UUID) -> UploadJob | None:
        return self.db.query(UploadJob).filter(UploadJob.id == queue_id).first()

    def get_by_client_id_and_user(
        self, client_id: str, entry_id: Optional[UUID]
    ) -> UploadJob | None:
        query = self.db.query(UploadJob).filter(UploadJob.client_id == client_id)
        if entry_id:
            query = query.filter(UploadJob.entry_id == entry_id)
        return query.first()

    def list_by_entry(
        self,
        entry_id: UUID,
        status: Optional[str] = None,
        upload_entity_type: Optional[str] = None,
        upload_action: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[UploadJob]:
        query = self.db.query(UploadJob).filter(UploadJob.entry_id == entry_id)
        if status:
            query = query.filter(UploadJob.status == status)
        if upload_entity_type:
            query = query.filter(UploadJob.upload_entity_type == upload_entity_type)
        if upload_action:
            query = query.filter(UploadJob.upload_action == upload_action)
        return query.order_by(UploadJob.created_at.desc()).offset(offset).limit(limit).all()

    def list_all(
        self,
        status: Optional[str] = None,
        upload_entity_type: Optional[str] = None,
        upload_action: Optional[str] = None,
        offset: int = 0,
        limit: int = 20,
    ) -> list[UploadJob]:
        query = self.db.query(UploadJob)
        if status:
            query = query.filter(UploadJob.status == status)
        if upload_entity_type:
            query = query.filter(UploadJob.upload_entity_type == upload_entity_type)
        if upload_action:
            query = query.filter(UploadJob.upload_action == upload_action)
        return query.order_by(UploadJob.created_at.desc()).offset(offset).limit(limit).all()

    def count_all(
        self,
        status: Optional[str] = None,
        upload_entity_type: Optional[str] = None,
        upload_action: Optional[str] = None,
    ) -> int:
        query = self.db.query(func.count(UploadJob.id))
        if status:
            query = query.filter(UploadJob.status == status)
        if upload_entity_type:
            query = query.filter(UploadJob.upload_entity_type == upload_entity_type)
        if upload_action:
            query = query.filter(UploadJob.upload_action == upload_action)
        return query.scalar() or 0

    def create(
        self,
        client_id: str,
        upload_entity_type: str,
        upload_action: str,
        entry_id: Optional[UUID] = None,
        status: UploadStatus = UploadStatus.pending,
    ) -> UploadJob:
        job = UploadJob(
            client_id=client_id,
            entry_id=entry_id,
            upload_entity_type=upload_entity_type,
            upload_action=upload_action,
            status=status,
        )
        self.db.add(job)
        self.db.flush()
        return job

    def update(self, job: UploadJob, updates: dict) -> UploadJob:
        for key, value in updates.items():
            setattr(job, key, value)
        self.db.flush()
        return job

    def reset_for_retry(self, job: UploadJob) -> UploadJob:
        job.status = UploadStatus.pending
        job.retry_count = (job.retry_count or 0) + 1
        self.db.flush()
        return job

"""File upload service for P2-7.

Upload flow:
1. POST /files/upload-url → generate presigned URL + object key
2. Client uploads directly to MinIO via presigned URL
3. POST /files/complete → confirm upload success
4. POST /files/upload-failed → record upload failure

API-GAP-P2-7-007: Binding of uploaded file to a Note Item is NOT done
automatically on complete. The client must create a Note Item with the
file_path set to the file_key after completing the upload.

API-GAP-P2-7-008: MinIO bucket and object key naming rules are inferred
from the API spec example only.

API-GAP-P2-7-016: Checksum/dedup behavior is not specified.
"""
from uuid import UUID

from sqlalchemy.orm import Session

from app.core.enums import UserRole
from app.core.errors import AppError
from app.models.user import User
from app.repositories.notebook_entries import NotebookEntryRepository
from app.schemas.file import FileCompleteRequest, FileFailedRequest, UploadUrlRequest
from app.services.base import BaseService
from app.utils.minio_client import generate_object_key, generate_presigned_upload_url, get_minio_client
from app.core.config import settings

_PRIVILEGED_ROLES = {UserRole.admin, UserRole.root, UserRole.ari_staff}


def _is_privileged(user: User) -> bool:
    return user.role in _PRIVILEGED_ROLES


class FileService(BaseService):
    def __init__(self, db: Session) -> None:
        self.db = db
        self.entry_repo = NotebookEntryRepository(db)

    def _get_accessible_entry(self, user: User, entry_id: UUID):
        entry = self.entry_repo.get_by_id(entry_id)
        if not entry:
            raise AppError("entry_not_found", "Notebook entry not found", 404)
        if not _is_privileged(user) and entry.organization_id != user.organization_id:
            raise AppError("entry_not_accessible", "Notebook entry is not accessible", 403)
        return entry

    def generate_upload_url(self, user: User, req: UploadUrlRequest) -> dict:
        if req.file_size <= 0:
            raise AppError("invalid_file_size", "file_size must be greater than 0", 422)

        entry = self._get_accessible_entry(user, req.entry_id)

        object_key = generate_object_key(
            str(entry.organization_id),
            str(req.entry_id),
            req.file_name,
        )

        client = get_minio_client()
        upload_url = generate_presigned_upload_url(
            client, settings.MINIO_BUCKET, object_key, expires_seconds=900
        )

        return {
            "file_key": object_key,
            "upload_url": upload_url,
            "expires_in": 900,
        }

    def complete_upload(self, user: User, req: FileCompleteRequest) -> dict:
        self._get_accessible_entry(user, req.entry_id)
        return {"success": True}

    def record_upload_failed(self, user: User, req: FileFailedRequest) -> dict:
        self._get_accessible_entry(user, req.entry_id)
        return {"success": True}

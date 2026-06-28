"""MinIO client helper for P2-7 file upload operations.

API-GAP-P2-7-008: Bucket and object key naming rules are not fully specified
in frozen docs. Object key format is inferred from API spec example:
  organizations/{org_id}/entries/{entry_id}/{file_name}
"""
import uuid
from datetime import timedelta

from minio import Minio

from app.core.config import settings


def get_minio_client() -> Minio:
    return Minio(
        settings.MINIO_ENDPOINT,
        access_key=settings.MINIO_ROOT_USER,
        secret_key=settings.MINIO_ROOT_PASSWORD,
        secure=settings.MINIO_SECURE,
    )


def generate_object_key(organization_id: str, entry_id: str, file_name: str) -> str:
    safe_name = file_name.replace("..", "").lstrip("/")
    return f"organizations/{organization_id}/entries/{entry_id}/{safe_name}"


def generate_presigned_upload_url(
    client: Minio,
    bucket: str,
    object_key: str,
    expires_seconds: int = 900,
) -> str:
    return client.presigned_put_object(
        bucket,
        object_key,
        expires=timedelta(seconds=expires_seconds),
    )


def object_exists(client: Minio, bucket: str, object_key: str) -> bool:
    try:
        client.stat_object(bucket, object_key)
        return True
    except Exception:
        return False

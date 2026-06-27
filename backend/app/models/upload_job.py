from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.enums import UploadStatus
from app.db.base import Base


class UploadJob(Base):
    __tablename__ = "upload_queue"
    __table_args__ = (
        Index("idx_upload_queue_entry_id", "entry_id"),
        Index("idx_upload_queue_status", "status"),
        Index("idx_upload_queue_client_id", "client_id"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    entry_id = Column(UUID(as_uuid=True), ForeignKey("notebook_entries.id"), nullable=True)
    client_id = Column(String(255), nullable=True)
    # API-GAP-P2-4-003: upload_entity_type and upload_action stored as String; full enum values not confirmed
    upload_entity_type = Column(String(100), nullable=True)
    upload_action = Column(String(100), nullable=True)
    status = Column(Enum(UploadStatus, name="upload_status_enum"), nullable=False, server_default="pending")
    retry_count = Column(Integer, nullable=False, server_default="0")
    error_message = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    uploaded_at = Column(DateTime(timezone=True), nullable=True)

    entry = relationship("NotebookEntry", back_populates="upload_queue")

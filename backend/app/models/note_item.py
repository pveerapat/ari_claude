from uuid import uuid4

from sqlalchemy import BigInteger, Column, DateTime, Enum, ForeignKey, Index, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.enums import ItemType, UploadStatus
from app.db.base import Base


class NoteItem(Base):
    __tablename__ = "note_items"
    __table_args__ = (
        Index("idx_note_items_entry_id_sequence_order", "entry_id", "sequence_order"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    entry_id = Column(UUID(as_uuid=True), ForeignKey("notebook_entries.id"), nullable=False)
    item_type = Column(Enum(ItemType, name="item_type_enum"), nullable=False)
    sequence_order = Column(Integer, nullable=False)
    content_text = Column(Text, nullable=True)
    file_path = Column(String(1000), nullable=True)
    file_ref = Column(String(1000), nullable=True)
    local_path = Column(String(1000), nullable=True)
    url = Column(String(2000), nullable=True)
    platform = Column(String(100), nullable=True)
    checksum = Column(String(64), nullable=True)
    duration_sec = Column(Integer, nullable=True)
    content_type = Column(String(100), nullable=True)
    file_size = Column(BigInteger, nullable=True)
    upload_status = Column(Enum(UploadStatus, name="upload_status_enum"), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())

    entry = relationship("NotebookEntry", back_populates="note_items")

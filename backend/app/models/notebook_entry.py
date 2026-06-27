from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Index, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.enums import EntryContext, EntryType, ExternalAI
from app.db.base import Base


class NotebookEntry(Base):
    __tablename__ = "notebook_entries"
    __table_args__ = (
        Index("idx_notebook_entries_organization_id", "organization_id"),
        Index("idx_notebook_entries_created_by_created_at", "created_by_user_id", "created_at"),
        Index("idx_notebook_entries_farm_id", "farm_id"),
        Index("idx_notebook_entries_zone_id", "zone_id"),
        Index("idx_notebook_entries_tree_id", "tree_id"),
        Index("idx_notebook_entries_entry_type", "entry_type"),
        Index("idx_notebook_entries_entry_context", "entry_context"),
        Index("idx_notebook_entries_created_at", "created_at"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    created_by_user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    farm_id = Column(UUID(as_uuid=True), ForeignKey("farms.id"), nullable=True)
    zone_id = Column(UUID(as_uuid=True), ForeignKey("zones.id"), nullable=True)
    tree_id = Column(UUID(as_uuid=True), ForeignKey("trees.id"), nullable=True)
    entry_type = Column(Enum(EntryType, name="entry_type_enum"), nullable=False)
    entry_context = Column(Enum(EntryContext, name="entry_context_enum"), nullable=False)
    title = Column(String(500), nullable=True)
    summary = Column(Text, nullable=True)
    suggested_category = Column(String(255), nullable=True)
    # API-GAP-P2-4-006: analysis_status stored as String; full enum values not confirmed beyond 'not_started'
    analysis_status = Column(String(50), nullable=False, server_default="not_started")
    external_ai = Column(Enum(ExternalAI, name="external_ai_enum"), nullable=True)
    # AI usefulness: useful/not_useful/later — exact enum name not confirmed in frozen DB spec
    ai_usefulness_status = Column(String(50), nullable=True)
    learned_summary = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now(), onupdate=func.now())

    organization = relationship("Organization", back_populates="notebook_entries")
    created_by_user = relationship("User", back_populates="notebook_entries")
    farm = relationship("Farm", foreign_keys=[farm_id], back_populates="notebook_entries")
    zone = relationship("Zone", foreign_keys=[zone_id], back_populates="notebook_entries")
    tree = relationship("Tree", foreign_keys=[tree_id], back_populates="notebook_entries")
    note_items = relationship("NoteItem", back_populates="entry", cascade="all, delete-orphan")
    follow_ups = relationship("FollowUp", back_populates="entry")
    upload_queue = relationship("UploadJob", back_populates="entry")

from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Index, Integer, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.enums import FollowUpOutcome
from app.db.base import Base


class FollowUp(Base):
    __tablename__ = "follow_ups"
    __table_args__ = (
        Index("idx_follow_ups_entry_id", "entry_id"),
        Index("idx_follow_ups_outcome", "outcome"),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    entry_id = Column(UUID(as_uuid=True), ForeignKey("notebook_entries.id"), nullable=False)
    follow_up_day = Column(Integer, nullable=False)
    outcome = Column(Enum(FollowUpOutcome, name="follow_up_outcome_enum"), nullable=True)
    notes = Column(Text, nullable=True)
    recorded_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())

    entry = relationship("NotebookEntry", back_populates="follow_ups")

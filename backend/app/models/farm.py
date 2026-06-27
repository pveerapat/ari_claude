from uuid import uuid4

from sqlalchemy import Column, DateTime, ForeignKey, String, Text
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base import Base


class Farm(Base):
    __tablename__ = "farms"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    location = Column(JSONB, nullable=True)
    status = Column(String(50), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())

    organization = relationship("Organization", back_populates="farms")
    zones = relationship("Zone", back_populates="farm")
    notebook_entries = relationship("NotebookEntry", foreign_keys="NotebookEntry.farm_id", back_populates="farm")
    primary_users = relationship("User", foreign_keys="User.primary_farm_id", back_populates="primary_farm")

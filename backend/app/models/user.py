from uuid import uuid4

from sqlalchemy import Column, DateTime, Enum, ForeignKey, Index, String, text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.core.enums import AccountStatus, FarmerStatus, MembershipStatus, UserRole
from app.db.base import Base


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        Index("idx_users_organization_id", "organization_id"),
        Index("idx_users_membership_status", "membership_status"),
        Index("idx_users_account_status", "account_status"),
        Index("idx_users_primary_farm_id", "primary_farm_id"),
        # API-GAP-P2-4-002: deleted_at column is required for this partial unique index.
        # frozen v1.1 schema defines this index but deleted_at is not in the base P0 domain model.
        Index(
            "uq_users_phone_not_null",
            "phone",
            unique=True,
            postgresql_where=text("phone IS NOT NULL AND deleted_at IS NULL"),
        ),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    organization_id = Column(UUID(as_uuid=True), ForeignKey("organizations.id"), nullable=False)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True, unique=True)
    password_hash = Column(String(255), nullable=True)
    phone = Column(String(30), nullable=True)
    role = Column(Enum(UserRole, name="user_role_enum"), nullable=True)
    farmer_status = Column(Enum(FarmerStatus, name="farmer_status_enum"), nullable=True)
    membership_status = Column(Enum(MembershipStatus, name="membership_status_enum"), nullable=True)
    account_status = Column(Enum(AccountStatus, name="account_status_enum"), nullable=True)
    primary_farm_id = Column(
        UUID(as_uuid=True),
        ForeignKey("farms.id", use_alter=True, name="fk_users_primary_farm_id"),
        nullable=True,
    )
    registered_at = Column(DateTime(timezone=True), nullable=True)
    deleted_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), nullable=False, server_default=func.now())
    updated_at = Column(DateTime(timezone=True), nullable=True, onupdate=func.now())

    organization = relationship("Organization", foreign_keys=[organization_id], back_populates="users")
    primary_farm = relationship("Farm", foreign_keys=[primary_farm_id], back_populates="primary_users")
    notebook_entries = relationship("NotebookEntry", back_populates="created_by_user")
    notifications = relationship("Notification", back_populates="user")

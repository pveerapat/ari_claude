"""Initial frozen schema — P2-4

Revision ID: a1b2c3d4e5f6
Revises:
Create Date: 2026-06-28

Tables created:
    organizations, farms, users, zones, trees,
    notebook_entries, note_items, follow_ups, notifications, upload_queue

Frozen enums created:
    entry_type_enum, entry_context_enum, item_type_enum, external_ai_enum,
    upload_status_enum, follow_up_outcome_enum, user_role_enum,
    farmer_status_enum, membership_status_enum, account_status_enum

API Gaps noted in this migration:
    API-GAP-P2-4-001: physical PK column name uses 'id' (not domain-specific *_id)
    API-GAP-P2-4-002: deleted_at added to users to support phone partial unique index
    API-GAP-P2-4-003: table name is upload_queue; Python class is UploadJob
    API-GAP-P2-4-004: roles/user_roles tables excluded — not confirmed in frozen DB spec
    API-GAP-P2-4-005: notification type/status stored as VARCHAR — enum values not confirmed
    API-GAP-P2-4-006: analysis_status stored as VARCHAR — full enum not confirmed
    API-GAP-P2-4-007: consultation_status not used as column — consultation is entry_type value
"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

revision: str = "a1b2c3d4e5f6"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # -------------------------------------------------------------------------
    # PostgreSQL enum types — fully frozen values only
    # -------------------------------------------------------------------------
    op.execute(sa.text(
        "CREATE TYPE entry_type_enum AS ENUM ('note', 'consultation')"
    ))
    op.execute(sa.text(
        "CREATE TYPE entry_context_enum AS ENUM "
        "('general_note', 'registered_farm', 'external_observation', 'interview')"
    ))
    op.execute(sa.text(
        "CREATE TYPE item_type_enum AS ENUM ('photo', 'video', 'voice', 'text', 'file', 'link')"
    ))
    op.execute(sa.text(
        "CREATE TYPE external_ai_enum AS ENUM ('chatgpt', 'gemini', 'claude', 'other')"
    ))
    op.execute(sa.text(
        "CREATE TYPE upload_status_enum AS ENUM ('pending', 'uploading', 'failed', 'completed')"
    ))
    op.execute(sa.text(
        "CREATE TYPE follow_up_outcome_enum AS ENUM ('improved', 'same', 'worse', 'unknown')"
    ))
    op.execute(sa.text(
        "CREATE TYPE user_role_enum AS ENUM "
        "('farmer', 'ari_staff', 'farm_coordinator', 'agronomist', 'reviewer', 'admin', 'root')"
    ))
    op.execute(sa.text(
        "CREATE TYPE farmer_status_enum AS ENUM ('owner', 'owner_family', 'farm_staff')"
    ))
    op.execute(sa.text(
        "CREATE TYPE membership_status_enum AS ENUM "
        "('pending_farm_approval', 'active', 'rejected', 'suspended', 'revoked')"
    ))
    op.execute(sa.text(
        "CREATE TYPE account_status_enum AS ENUM "
        "('active', 'active_pending_verification', 'pending_review', 'suspended', 'rejected', 'revoked')"
    ))

    # -------------------------------------------------------------------------
    # 1. organizations
    # -------------------------------------------------------------------------
    op.create_table(
        "organizations",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("type", sa.String(100), nullable=True),
        sa.Column("status", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
    )

    # -------------------------------------------------------------------------
    # 2. farms (depends on organizations)
    # -------------------------------------------------------------------------
    op.create_table(
        "farms",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("location", postgresql.JSONB, nullable=True),
        sa.Column("status", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"],
                                name="fk_farms_organization_id"),
    )
    op.create_index("idx_farms_organization_id", "farms", ["organization_id"])

    # -------------------------------------------------------------------------
    # 3. users (depends on organizations + farms for primary_farm_id)
    # API-GAP-P2-4-002: deleted_at added to support phone partial unique index
    # API-GAP-P2-4-004: role stored as column (not separate roles table)
    # -------------------------------------------------------------------------
    op.create_table(
        "users",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("password_hash", sa.String(255), nullable=True),
        sa.Column("phone", sa.String(30), nullable=True),
        sa.Column("role", postgresql.ENUM(
            "farmer", "ari_staff", "farm_coordinator", "agronomist", "reviewer", "admin", "root",
            name="user_role_enum", create_type=False,
        ), nullable=True),
        sa.Column("farmer_status", postgresql.ENUM(
            "owner", "owner_family", "farm_staff",
            name="farmer_status_enum", create_type=False,
        ), nullable=True),
        sa.Column("membership_status", postgresql.ENUM(
            "pending_farm_approval", "active", "rejected", "suspended", "revoked",
            name="membership_status_enum", create_type=False,
        ), nullable=True),
        sa.Column("account_status", postgresql.ENUM(
            "active", "active_pending_verification", "pending_review",
            "suspended", "rejected", "revoked",
            name="account_status_enum", create_type=False,
        ), nullable=True),
        sa.Column("primary_farm_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("registered_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"],
                                name="fk_users_organization_id"),
        sa.ForeignKeyConstraint(["primary_farm_id"], ["farms.id"],
                                name="fk_users_primary_farm_id"),
        sa.UniqueConstraint("email", name="uq_users_email"),
    )
    op.create_index("idx_users_organization_id", "users", ["organization_id"])
    op.create_index("idx_users_membership_status", "users", ["membership_status"])
    op.create_index("idx_users_account_status", "users", ["account_status"])
    op.create_index("idx_users_primary_farm_id", "users", ["primary_farm_id"])
    op.execute(sa.text(
        "CREATE UNIQUE INDEX uq_users_phone_not_null ON users(phone) "
        "WHERE phone IS NOT NULL AND deleted_at IS NULL"
    ))

    # -------------------------------------------------------------------------
    # 4. zones (depends on farms)
    # -------------------------------------------------------------------------
    op.create_table(
        "zones",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("farm_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("name", sa.String(255), nullable=False),
        sa.Column("description", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["farm_id"], ["farms.id"], name="fk_zones_farm_id"),
    )
    op.create_index("idx_zones_farm_id", "zones", ["farm_id"])

    # -------------------------------------------------------------------------
    # 5. trees (depends on zones)
    # -------------------------------------------------------------------------
    op.create_table(
        "trees",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("zone_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("tree_code", sa.String(100), nullable=False),
        sa.Column("status", sa.String(50), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["zone_id"], ["zones.id"], name="fk_trees_zone_id"),
    )
    op.create_index("idx_trees_zone_id", "trees", ["zone_id"])

    # -------------------------------------------------------------------------
    # 6. notebook_entries (depends on organizations, users, farms, zones, trees)
    # API-GAP-P2-4-006: analysis_status stored as VARCHAR
    # -------------------------------------------------------------------------
    op.create_table(
        "notebook_entries",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("organization_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("created_by_user_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("farm_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("zone_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("tree_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("entry_type", postgresql.ENUM(
            "note", "consultation",
            name="entry_type_enum", create_type=False,
        ), nullable=False),
        sa.Column("entry_context", postgresql.ENUM(
            "general_note", "registered_farm", "external_observation", "interview",
            name="entry_context_enum", create_type=False,
        ), nullable=False),
        sa.Column("title", sa.String(500), nullable=True),
        sa.Column("summary", sa.Text, nullable=True),
        sa.Column("suggested_category", sa.String(255), nullable=True),
        sa.Column("analysis_status", sa.String(50), nullable=False,
                  server_default="not_started"),
        sa.Column("external_ai", postgresql.ENUM(
            "chatgpt", "gemini", "claude", "other",
            name="external_ai_enum", create_type=False,
        ), nullable=True),
        sa.Column("ai_usefulness_status", sa.String(50), nullable=True),
        sa.Column("learned_summary", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("NOW()")),
        sa.ForeignKeyConstraint(["organization_id"], ["organizations.id"],
                                name="fk_notebook_entries_organization_id"),
        sa.ForeignKeyConstraint(["created_by_user_id"], ["users.id"],
                                name="fk_notebook_entries_created_by_user_id"),
        sa.ForeignKeyConstraint(["farm_id"], ["farms.id"],
                                name="fk_notebook_entries_farm_id"),
        sa.ForeignKeyConstraint(["zone_id"], ["zones.id"],
                                name="fk_notebook_entries_zone_id"),
        sa.ForeignKeyConstraint(["tree_id"], ["trees.id"],
                                name="fk_notebook_entries_tree_id"),
    )
    op.create_index("idx_notebook_entries_organization_id", "notebook_entries", ["organization_id"])
    op.create_index("idx_notebook_entries_created_by_created_at", "notebook_entries",
                    ["created_by_user_id", "created_at"])
    op.create_index("idx_notebook_entries_farm_id", "notebook_entries", ["farm_id"])
    op.create_index("idx_notebook_entries_zone_id", "notebook_entries", ["zone_id"])
    op.create_index("idx_notebook_entries_tree_id", "notebook_entries", ["tree_id"])
    op.create_index("idx_notebook_entries_entry_type", "notebook_entries", ["entry_type"])
    op.create_index("idx_notebook_entries_entry_context", "notebook_entries", ["entry_context"])
    op.create_index("idx_notebook_entries_created_at", "notebook_entries", ["created_at"])

    # -------------------------------------------------------------------------
    # 7. note_items (depends on notebook_entries)
    # -------------------------------------------------------------------------
    op.create_table(
        "note_items",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("entry_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("item_type", postgresql.ENUM(
            "photo", "video", "voice", "text", "file", "link",
            name="item_type_enum", create_type=False,
        ), nullable=False),
        sa.Column("sequence_order", sa.Integer, nullable=False),
        sa.Column("content_text", sa.Text, nullable=True),
        sa.Column("file_path", sa.String(1000), nullable=True),
        sa.Column("file_ref", sa.String(1000), nullable=True),
        sa.Column("local_path", sa.String(1000), nullable=True),
        sa.Column("url", sa.String(2000), nullable=True),
        sa.Column("platform", sa.String(100), nullable=True),
        sa.Column("checksum", sa.String(64), nullable=True),
        sa.Column("duration_sec", sa.Integer, nullable=True),
        sa.Column("content_type", sa.String(100), nullable=True),
        sa.Column("file_size", sa.BigInteger, nullable=True),
        sa.Column("upload_status", postgresql.ENUM(
            "pending", "uploading", "failed", "completed",
            name="upload_status_enum", create_type=False,
        ), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("NOW()")),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["entry_id"], ["notebook_entries.id"],
                                name="fk_note_items_entry_id"),
    )
    op.create_index("idx_note_items_entry_id_sequence_order", "note_items",
                    ["entry_id", "sequence_order"])

    # -------------------------------------------------------------------------
    # 8. follow_ups (depends on notebook_entries)
    # -------------------------------------------------------------------------
    op.create_table(
        "follow_ups",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("entry_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("follow_up_day", sa.Integer, nullable=False),
        sa.Column("outcome", postgresql.ENUM(
            "improved", "same", "worse", "unknown",
            name="follow_up_outcome_enum", create_type=False,
        ), nullable=True),
        sa.Column("notes", sa.Text, nullable=True),
        sa.Column("recorded_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("NOW()")),
        sa.ForeignKeyConstraint(["entry_id"], ["notebook_entries.id"],
                                name="fk_follow_ups_entry_id"),
    )
    op.create_index("idx_follow_ups_entry_id", "follow_ups", ["entry_id"])
    op.create_index("idx_follow_ups_outcome", "follow_ups", ["outcome"])

    # -------------------------------------------------------------------------
    # 9. notifications (depends on users)
    # API-GAP-P2-4-005: type and status stored as VARCHAR
    # -------------------------------------------------------------------------
    op.create_table(
        "notifications",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("user_id", postgresql.UUID(as_uuid=False), nullable=False),
        sa.Column("type", sa.String(100), nullable=False),
        sa.Column("message", sa.Text, nullable=False),
        sa.Column("status", sa.String(50), nullable=False, server_default="unread"),
        sa.Column("read_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("NOW()")),
        sa.ForeignKeyConstraint(["user_id"], ["users.id"],
                                name="fk_notifications_user_id"),
    )
    op.create_index("idx_notifications_user_id", "notifications", ["user_id"])
    op.create_index("idx_notifications_status", "notifications", ["status"])

    # -------------------------------------------------------------------------
    # 10. upload_queue (depends on notebook_entries)
    # API-GAP-P2-4-003: Python class = UploadJob; table name = upload_queue
    # API-GAP-P2-4-003: upload_entity_type and upload_action stored as VARCHAR
    # -------------------------------------------------------------------------
    op.create_table(
        "upload_queue",
        sa.Column("id", postgresql.UUID(as_uuid=False), primary_key=True,
                  server_default=sa.text("gen_random_uuid()")),
        sa.Column("entry_id", postgresql.UUID(as_uuid=False), nullable=True),
        sa.Column("client_id", sa.String(255), nullable=True),
        sa.Column("upload_entity_type", sa.String(100), nullable=True),
        sa.Column("upload_action", sa.String(100), nullable=True),
        sa.Column("status", postgresql.ENUM(
            "pending", "uploading", "failed", "completed",
            name="upload_status_enum", create_type=False,
        ), nullable=False, server_default="pending"),
        sa.Column("retry_count", sa.Integer, nullable=False, server_default="0"),
        sa.Column("error_message", sa.Text, nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False,
                  server_default=sa.text("NOW()")),
        sa.Column("uploaded_at", sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(["entry_id"], ["notebook_entries.id"],
                                name="fk_upload_queue_entry_id"),
    )
    op.create_index("idx_upload_queue_entry_id", "upload_queue", ["entry_id"])
    op.create_index("idx_upload_queue_status", "upload_queue", ["status"])
    op.create_index("idx_upload_queue_client_id", "upload_queue", ["client_id"])


def downgrade() -> None:
    op.drop_table("upload_queue")
    op.drop_table("notifications")
    op.drop_table("follow_ups")
    op.drop_table("note_items")
    op.drop_table("notebook_entries")
    op.drop_table("trees")
    op.drop_table("zones")
    op.drop_table("users")
    op.drop_table("farms")
    op.drop_table("organizations")

    op.execute(sa.text("DROP TYPE IF EXISTS account_status_enum"))
    op.execute(sa.text("DROP TYPE IF EXISTS membership_status_enum"))
    op.execute(sa.text("DROP TYPE IF EXISTS farmer_status_enum"))
    op.execute(sa.text("DROP TYPE IF EXISTS user_role_enum"))
    op.execute(sa.text("DROP TYPE IF EXISTS follow_up_outcome_enum"))
    op.execute(sa.text("DROP TYPE IF EXISTS upload_status_enum"))
    op.execute(sa.text("DROP TYPE IF EXISTS external_ai_enum"))
    op.execute(sa.text("DROP TYPE IF EXISTS item_type_enum"))
    op.execute(sa.text("DROP TYPE IF EXISTS entry_context_enum"))
    op.execute(sa.text("DROP TYPE IF EXISTS entry_type_enum"))

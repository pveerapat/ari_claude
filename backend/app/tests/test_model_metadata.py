"""P2-4: verify Base metadata contains expected frozen tables and no forbidden tables."""

import app.models  # noqa: F401 — ensures all models are registered
from app.db.base import Base

EXPECTED_TABLES = {
    "organizations",
    "users",
    "farms",
    "zones",
    "trees",
    "notebook_entries",
    "note_items",
    "follow_ups",
    "notifications",
    "upload_queue",
}

FORBIDDEN_TABLES = {
    "consultations",
    "qr_registry",
    "farm_memberships",
    "permissions",
    "audit_logs",
    "knowledge_assets",
    "vectors",
    "owner_registry",
    "member_registry",
    "farmer_registry",
    "upload_jobs",
}


class TestExpectedTables:
    def test_expected_tables_in_metadata(self):
        actual = set(Base.metadata.tables.keys())
        missing = EXPECTED_TABLES - actual
        assert not missing, f"Missing frozen tables in metadata: {missing}"

    def test_organizations_in_metadata(self):
        assert "organizations" in Base.metadata.tables

    def test_users_in_metadata(self):
        assert "users" in Base.metadata.tables

    def test_farms_in_metadata(self):
        assert "farms" in Base.metadata.tables

    def test_zones_in_metadata(self):
        assert "zones" in Base.metadata.tables

    def test_trees_in_metadata(self):
        assert "trees" in Base.metadata.tables

    def test_notebook_entries_in_metadata(self):
        assert "notebook_entries" in Base.metadata.tables

    def test_note_items_in_metadata(self):
        assert "note_items" in Base.metadata.tables

    def test_follow_ups_in_metadata(self):
        assert "follow_ups" in Base.metadata.tables

    def test_notifications_in_metadata(self):
        assert "notifications" in Base.metadata.tables

    def test_upload_queue_in_metadata(self):
        assert "upload_queue" in Base.metadata.tables


class TestForbiddenTables:
    def test_no_forbidden_tables_in_metadata(self):
        actual = set(Base.metadata.tables.keys())
        found = FORBIDDEN_TABLES & actual
        assert not found, f"Forbidden tables found in metadata: {found}"

    def test_no_consultations_table(self):
        assert "consultations" not in Base.metadata.tables

    def test_no_qr_registry_table(self):
        assert "qr_registry" not in Base.metadata.tables

    def test_no_farm_memberships_table(self):
        assert "farm_memberships" not in Base.metadata.tables

    def test_no_permissions_table(self):
        assert "permissions" not in Base.metadata.tables

    def test_no_audit_logs_table(self):
        assert "audit_logs" not in Base.metadata.tables

    def test_no_upload_jobs_table(self):
        assert "upload_jobs" not in Base.metadata.tables


class TestKeyColumns:
    def test_users_has_phone_column(self):
        table = Base.metadata.tables["users"]
        assert "phone" in table.c

    def test_users_has_farmer_status_column(self):
        table = Base.metadata.tables["users"]
        assert "farmer_status" in table.c

    def test_users_has_membership_status_column(self):
        table = Base.metadata.tables["users"]
        assert "membership_status" in table.c

    def test_users_has_account_status_column(self):
        table = Base.metadata.tables["users"]
        assert "account_status" in table.c

    def test_users_has_primary_farm_id_column(self):
        table = Base.metadata.tables["users"]
        assert "primary_farm_id" in table.c

    def test_users_has_deleted_at_column(self):
        table = Base.metadata.tables["users"]
        assert "deleted_at" in table.c

    def test_farms_has_location_column(self):
        table = Base.metadata.tables["farms"]
        assert "location" in table.c

    def test_notebook_entries_farm_id_nullable(self):
        table = Base.metadata.tables["notebook_entries"]
        assert table.c["farm_id"].nullable is True

    def test_notebook_entries_zone_id_nullable(self):
        table = Base.metadata.tables["notebook_entries"]
        assert table.c["zone_id"].nullable is True

    def test_notebook_entries_tree_id_nullable(self):
        table = Base.metadata.tables["notebook_entries"]
        assert table.c["tree_id"].nullable is True

    def test_upload_queue_table_name(self):
        assert "upload_queue" in Base.metadata.tables
        assert "upload_jobs" not in Base.metadata.tables

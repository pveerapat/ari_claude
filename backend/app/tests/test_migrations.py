"""P2-4: verify Alembic config and migration file are correctly structured."""

import os
from pathlib import Path


class TestAlembicConfig:
    def test_alembic_ini_exists(self):
        ini = Path(__file__).parent.parent.parent / "alembic.ini"
        assert ini.exists(), "alembic.ini not found in backend/"

    def test_migrations_dir_exists(self):
        migrations = Path(__file__).parent.parent / "db" / "migrations"
        assert migrations.is_dir(), "app/db/migrations/ directory not found"

    def test_env_py_exists(self):
        env = Path(__file__).parent.parent / "db" / "migrations" / "env.py"
        assert env.exists(), "app/db/migrations/env.py not found"

    def test_script_mako_exists(self):
        mako = Path(__file__).parent.parent / "db" / "migrations" / "script.py.mako"
        assert mako.exists(), "app/db/migrations/script.py.mako not found"

    def test_versions_dir_exists(self):
        versions = Path(__file__).parent.parent / "db" / "migrations" / "versions"
        assert versions.is_dir(), "app/db/migrations/versions/ directory not found"

    def test_initial_migration_exists(self):
        versions = Path(__file__).parent.parent / "db" / "migrations" / "versions"
        migration_files = list(versions.glob("*.py"))
        assert len(migration_files) >= 1, "No migration files found in versions/"

    def test_initial_migration_contains_frozen_tables(self):
        versions = Path(__file__).parent.parent / "db" / "migrations" / "versions"
        migration_files = list(versions.glob("*.py"))
        assert migration_files, "No migration files found"

        content = migration_files[0].read_text()
        expected_tables = [
            "organizations", "users", "farms", "zones", "trees",
            "notebook_entries", "note_items", "follow_ups", "notifications", "upload_queue",
        ]
        for table in expected_tables:
            assert table in content, f"Table '{table}' not found in migration file"

    def test_initial_migration_no_forbidden_tables(self):
        versions = Path(__file__).parent.parent / "db" / "migrations" / "versions"
        migration_files = list(versions.glob("*.py"))
        assert migration_files, "No migration files found"

        content = migration_files[0].read_text()
        forbidden = ["consultations", "qr_registry", "farm_memberships", "audit_logs"]
        for table in forbidden:
            assert f'"{table}"' not in content, f"Forbidden table '{table}' found in migration"

    def test_alembic_ini_script_location(self):
        ini = Path(__file__).parent.parent.parent / "alembic.ini"
        content = ini.read_text()
        assert "script_location = app/db/migrations" in content


class TestAlembicEnvPy:
    def test_env_py_imports_base_metadata(self):
        env = Path(__file__).parent.parent / "db" / "migrations" / "env.py"
        content = env.read_text()
        assert "target_metadata = Base.metadata" in content

    def test_env_py_imports_models(self):
        env = Path(__file__).parent.parent / "db" / "migrations" / "env.py"
        content = env.read_text()
        assert "import app.models" in content

    def test_env_py_reads_database_url_from_env(self):
        env = Path(__file__).parent.parent / "db" / "migrations" / "env.py"
        content = env.read_text()
        assert "DATABASE_URL" in content

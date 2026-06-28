"""P2-7: Forbidden scope checks — verify banned entities are absent."""
import os
import re

import pytest


def _grep_backend(pattern: str) -> list[str]:
    """Return list of file paths that match pattern (case-insensitive)."""
    backend_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    matches = []
    for root, dirs, files in os.walk(backend_root):
        dirs[:] = [d for d in dirs if d not in ("__pycache__", ".git", "migrations")]
        for fname in files:
            if not fname.endswith(".py"):
                continue
            fpath = os.path.join(root, fname)
            try:
                content = open(fpath).read()
                if re.search(pattern, content, re.IGNORECASE):
                    matches.append(fpath)
            except Exception:
                pass
    return matches


class TestForbiddenEntitiesAbsent:
    def test_no_consultations_table_defined(self):
        matches = _grep_backend(r'__tablename__\s*=\s*["\']consultations["\']')
        assert matches == [], f"consultations table found in: {matches}"

    def test_no_consultation_router(self):
        matches = _grep_backend(r'prefix\s*=\s*["\']\/consultations["\']')
        assert matches == [], f"consultation router found in: {matches}"

    def test_no_consultation_service_class(self):
        matches = _grep_backend(r'class\s+ConsultationService')
        assert matches == [], f"ConsultationService class found in: {matches}"

    def test_no_qr_registry(self):
        matches = _grep_backend(r'__tablename__\s*=\s*["\']qr_registry["\']')
        assert matches == [], f"qr_registry table found in: {matches}"

    def test_no_permission_service(self):
        matches = _grep_backend(r'class\s+PermissionService')
        assert matches == [], f"PermissionService found in: {matches}"

    def test_no_farm_memberships_table(self):
        matches = _grep_backend(r'__tablename__\s*=\s*["\']farm_memberships["\']')
        assert matches == [], f"farm_memberships table found in: {matches}"

    def test_no_knowledge_service(self):
        matches = _grep_backend(r'class\s+KnowledgeService')
        assert matches == [], f"KnowledgeService found in: {matches}"

    def test_no_vector_service(self):
        matches = _grep_backend(r'class\s+VectorService')
        assert matches == [], f"VectorService found in: {matches}"

    def test_no_rag_system(self):
        matches = _grep_backend(r'class\s+RAGService')
        assert matches == [], f"RAGService found in: {matches}"

    def test_no_upload_jobs_table(self):
        matches = _grep_backend(r'__tablename__\s*=\s*["\']upload_jobs["\']')
        assert matches == [], f"upload_jobs table found in: {matches}"

    def test_no_media_processing_worker(self):
        matches = _grep_backend(r'class\s+MediaProcessingWorker')
        assert matches == [], f"MediaProcessingWorker found in: {matches}"


class TestForbiddenApiPathsAbsent:
    def test_no_upload_jobs_api_path(self):
        matches = _grep_backend(r'prefix\s*=\s*["\']\/upload-jobs["\']')
        assert matches == [], f"/api/v1/upload-jobs path found in: {matches}"

    def test_no_consultations_api_path(self):
        matches = _grep_backend(r'prefix\s*=\s*["\']\/consultations["\']')
        assert matches == [], f"/api/v1/consultations path found in: {matches}"

    def test_no_permissions_api_path(self):
        matches = _grep_backend(r'prefix\s*=\s*["\']\/permissions["\']')
        assert matches == [], f"/api/v1/permissions path found in: {matches}"

    def test_no_farm_memberships_api_path(self):
        matches = _grep_backend(r'prefix\s*=\s*["\']\/farm-memberships["\']')
        assert matches == [], f"/api/v1/farm-memberships path found in: {matches}"


class TestP27ApiPathsPresent:
    """Verify that all required P2-7 API paths are registered."""

    @pytest.fixture
    def client(self):
        from fastapi.testclient import TestClient
        from app.main import app
        return TestClient(app)

    def test_notebook_entries_path_exists(self, client):
        resp = client.get("/api/v1/notebook-entries")
        assert resp.status_code != 404

    def test_follow_ups_path_exists(self, client):
        resp = client.get("/api/v1/follow-ups")
        assert resp.status_code != 404

    def test_notifications_path_exists(self, client):
        resp = client.get("/api/v1/notifications")
        assert resp.status_code != 404

    def test_upload_queue_path_exists(self, client):
        resp = client.get("/api/v1/upload-queue")
        assert resp.status_code != 404

    def test_sync_batch_path_exists(self, client):
        resp = client.post("/api/v1/sync/batch", json={})
        assert resp.status_code != 404

    def test_upload_jobs_path_does_not_exist(self, client):
        resp = client.get("/api/v1/upload-jobs")
        assert resp.status_code == 404

"""P2-7: API-level tests for Upload Queue endpoints.

Tests verify:
- Correct path: /api/v1/upload-queue
- No /api/v1/upload-jobs path
- client_id idempotency behavior
- Retry lifecycle
"""
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.core.enums import AccountStatus, FarmerStatus, MembershipStatus, UploadStatus, UserRole
from app.core.errors import AppError
from app.dependencies.auth import require_active_membership
from app.dependencies.db import get_db
from app.main import app


def _mock_db():
    yield MagicMock()


@pytest.fixture(autouse=True)
def override_db():
    app.dependency_overrides[get_db] = _mock_db
    yield
    app.dependency_overrides.pop(get_db, None)


@pytest.fixture
def client():
    return TestClient(app)


def _make_active_farmer(org_id=None):
    user = MagicMock()
    user.id = uuid4()
    user.organization_id = org_id or uuid4()
    user.role = UserRole.farmer
    user.farmer_status = FarmerStatus.owner
    user.membership_status = MembershipStatus.active
    user.account_status = AccountStatus.active
    return user


def _make_queue_job(job_id=None, entry_id=None, client_id=None):
    m = MagicMock()
    m.id = job_id or uuid4()
    m.entry_id = entry_id
    m.client_id = client_id or str(uuid4())
    m.upload_entity_type = "notebook_entry"
    m.upload_action = "create"
    m.status = UploadStatus.pending
    m.retry_count = 0
    m.error_message = None
    m.created_at = MagicMock(isoformat=lambda: "2026-06-29T00:00:00")
    m.uploaded_at = None
    return m


class TestCreateUploadQueue:
    _PAYLOAD = {
        "client_id": str(uuid4()),
        "upload_entity_type": "notebook_entry",
        "upload_action": "create",
        "status": "pending",
    }

    def test_active_user_can_create(self, client):
        user = _make_active_farmer()
        job = _make_queue_job(client_id=self._PAYLOAD["client_id"])
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.upload_queue.UploadQueueService") as MockSvc:
            MockSvc.return_value.create_queue_record.return_value = job
            resp = client.post("/api/v1/upload-queue", json=self._PAYLOAD)
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200
        assert resp.json()["data"]["status"] == "pending"

    def test_idempotent_same_client_id(self, client):
        user = _make_active_farmer()
        job = _make_queue_job(client_id=self._PAYLOAD["client_id"])
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.upload_queue.UploadQueueService") as MockSvc:
            MockSvc.return_value.create_queue_record.return_value = job
            resp1 = client.post("/api/v1/upload-queue", json=self._PAYLOAD)
            resp2 = client.post("/api/v1/upload-queue", json=self._PAYLOAD)
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp1.json()["data"]["client_id"] == resp2.json()["data"]["client_id"]

    def test_unauthenticated_blocked(self, client):
        resp = client.post("/api/v1/upload-queue", json=self._PAYLOAD)
        assert resp.status_code in (401, 403)

    def test_pending_membership_blocked(self, client):
        def _pending():
            raise AppError("membership_not_active", "not active", 403)
        app.dependency_overrides[require_active_membership] = _pending
        resp = client.post("/api/v1/upload-queue", json=self._PAYLOAD)
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403


class TestListUploadQueue:
    def test_active_user_can_list(self, client):
        user = _make_active_farmer()
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.upload_queue.UploadQueueService") as MockSvc:
            MockSvc.return_value.list_queue.return_value = ([], 0)
            resp = client.get("/api/v1/upload-queue")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200


class TestGetUploadQueueRecord:
    def test_active_user_can_get(self, client):
        user = _make_active_farmer()
        queue_id = uuid4()
        job = _make_queue_job(job_id=queue_id)
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.upload_queue.UploadQueueService") as MockSvc:
            MockSvc.return_value.get_queue_record.return_value = job
            resp = client.get(f"/api/v1/upload-queue/{queue_id}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200

    def test_not_found_returns_404(self, client):
        user = _make_active_farmer()
        queue_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.upload_queue.UploadQueueService") as MockSvc:
            MockSvc.return_value.get_queue_record.side_effect = AppError(
                "queue_record_not_found", "Not found", 404
            )
            resp = client.get(f"/api/v1/upload-queue/{queue_id}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 404


class TestUpdateUploadQueue:
    def test_update_status_to_uploading(self, client):
        user = _make_active_farmer()
        queue_id = uuid4()
        job = _make_queue_job(job_id=queue_id)
        job.status = UploadStatus.uploading
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.upload_queue.UploadQueueService") as MockSvc:
            MockSvc.return_value.update_queue_record.return_value = job
            resp = client.patch(f"/api/v1/upload-queue/{queue_id}", json={"status": "uploading"})
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200

    def test_update_status_to_completed(self, client):
        user = _make_active_farmer()
        queue_id = uuid4()
        job = _make_queue_job(job_id=queue_id)
        job.status = UploadStatus.completed
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.upload_queue.UploadQueueService") as MockSvc:
            MockSvc.return_value.update_queue_record.return_value = job
            resp = client.patch(f"/api/v1/upload-queue/{queue_id}", json={"status": "completed"})
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200


class TestRetryUploadQueue:
    def test_retry_failed_record(self, client):
        user = _make_active_farmer()
        queue_id = uuid4()
        job = _make_queue_job(job_id=queue_id)
        job.status = UploadStatus.pending
        job.retry_count = 1
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.upload_queue.UploadQueueService") as MockSvc:
            MockSvc.return_value.retry_queue_record.return_value = job
            resp = client.post(f"/api/v1/upload-queue/{queue_id}/retry")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200
        assert resp.json()["data"]["status"] == "pending"

    def test_retry_completed_record_blocked(self, client):
        user = _make_active_farmer()
        queue_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.upload_queue.UploadQueueService") as MockSvc:
            MockSvc.return_value.retry_queue_record.side_effect = AppError(
                "retry_not_allowed", "Retry not allowed", 409
            )
            resp = client.post(f"/api/v1/upload-queue/{queue_id}/retry")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 409


class TestUploadJobsPathAbsent:
    def test_upload_jobs_path_does_not_exist(self, client):
        user = _make_active_farmer()
        app.dependency_overrides[require_active_membership] = lambda: user
        resp = client.get("/api/v1/upload-jobs")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 404

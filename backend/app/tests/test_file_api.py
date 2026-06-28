"""P2-7: API-level tests for File upload endpoints."""
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.core.enums import AccountStatus, FarmerStatus, MembershipStatus, UserRole
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


class TestCreateUploadUrl:
    _PAYLOAD = {
        "entry_id": str(uuid4()),
        "item_type": "photo",
        "file_name": "leaf.jpg",
        "content_type": "image/jpeg",
        "file_size": 1048576,
    }

    def test_active_user_can_get_upload_url(self, client):
        user = _make_active_farmer()
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.files.FileService") as MockSvc:
            MockSvc.return_value.generate_upload_url.return_value = {
                "file_key": "organizations/org1/entries/e1/leaf.jpg",
                "upload_url": "https://minio-presigned-url",
                "expires_in": 900,
            }
            resp = client.post("/api/v1/files/upload-url", json=self._PAYLOAD)
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert "file_key" in data
        assert "upload_url" in data
        assert data["expires_in"] == 900

    def test_entry_not_found_returns_404(self, client):
        user = _make_active_farmer()
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.files.FileService") as MockSvc:
            MockSvc.return_value.generate_upload_url.side_effect = AppError(
                "entry_not_found", "Not found", 404
            )
            resp = client.post("/api/v1/files/upload-url", json=self._PAYLOAD)
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 404

    def test_unauthenticated_blocked(self, client):
        resp = client.post("/api/v1/files/upload-url", json=self._PAYLOAD)
        assert resp.status_code in (401, 403)

    def test_missing_required_fields_rejected(self, client):
        user = _make_active_farmer()
        app.dependency_overrides[require_active_membership] = lambda: user
        resp = client.post("/api/v1/files/upload-url", json={"entry_id": str(uuid4())})
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 422

    def test_pending_membership_blocked(self, client):
        def _pending():
            raise AppError("membership_not_active", "not active", 403)
        app.dependency_overrides[require_active_membership] = _pending
        resp = client.post("/api/v1/files/upload-url", json=self._PAYLOAD)
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403

    def test_parent_entry_scope_controlled(self, client):
        user = _make_active_farmer()
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.files.FileService") as MockSvc:
            MockSvc.return_value.generate_upload_url.side_effect = AppError(
                "entry_not_accessible", "Not accessible", 403
            )
            resp = client.post("/api/v1/files/upload-url", json=self._PAYLOAD)
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403


class TestCompleteUpload:
    _PAYLOAD = {
        "entry_id": str(uuid4()),
        "file_key": "organizations/org1/entries/e1/leaf.jpg",
        "upload_status": "completed",
    }

    def test_active_user_can_complete(self, client):
        user = _make_active_farmer()
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.files.FileService") as MockSvc:
            MockSvc.return_value.complete_upload.return_value = {"success": True}
            resp = client.post("/api/v1/files/complete", json=self._PAYLOAD)
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200
        assert resp.json()["data"]["success"] is True

    def test_unauthenticated_blocked(self, client):
        resp = client.post("/api/v1/files/complete", json=self._PAYLOAD)
        assert resp.status_code in (401, 403)


class TestReportUploadFailed:
    _PAYLOAD = {
        "entry_id": str(uuid4()),
        "file_key": "organizations/org1/entries/e1/leaf.jpg",
        "reason": "network_error",
    }

    def test_active_user_can_report_failure(self, client):
        user = _make_active_farmer()
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.files.FileService") as MockSvc:
            MockSvc.return_value.record_upload_failed.return_value = {"success": True}
            resp = client.post("/api/v1/files/upload-failed", json=self._PAYLOAD)
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200
        assert resp.json()["data"]["success"] is True

    def test_unauthenticated_blocked(self, client):
        resp = client.post("/api/v1/files/upload-failed", json=self._PAYLOAD)
        assert resp.status_code in (401, 403)

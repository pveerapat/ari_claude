"""P2-7: API-level tests for Notebook Entry endpoints."""
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.core.enums import AccountStatus, EntryContext, EntryType, FarmerStatus, MembershipStatus, UserRole
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


def _make_entry(org_id=None, user_id=None, entry_id=None):
    m = MagicMock()
    m.id = entry_id or uuid4()
    m.organization_id = org_id or uuid4()
    m.created_by_user_id = user_id or uuid4()
    m.farm_id = None
    m.zone_id = None
    m.tree_id = None
    m.entry_type = EntryType.note
    m.entry_context = EntryContext.general_note
    m.title = "Test Entry"
    m.summary = None
    m.suggested_category = None
    m.analysis_status = "not_started"
    m.external_ai = None
    m.ai_usefulness_status = None
    m.learned_summary = None
    m.created_at = MagicMock(isoformat=lambda: "2026-06-29T00:00:00")
    m.updated_at = MagicMock(isoformat=lambda: "2026-06-29T00:00:00")
    return m


_CREATE_PAYLOAD = {
    "organization_id": str(uuid4()),
    "entry_type": "note",
    "entry_context": "general_note",
}


class TestListNotebookEntries:
    def test_active_user_can_list(self, client):
        user = _make_active_farmer()
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.notebook_entries.NotebookService") as MockSvc:
            MockSvc.return_value.list_entries.return_value = ([], 0)
            resp = client.get("/api/v1/notebook-entries")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200
        assert "data" in resp.json()
        assert "pagination" in resp.json()

    def test_unauthenticated_blocked(self, client):
        resp = client.get("/api/v1/notebook-entries")
        assert resp.status_code in (401, 403)

    def test_pending_membership_blocked(self, client):
        def _pending():
            raise AppError("membership_not_active", "not active", 403)
        app.dependency_overrides[require_active_membership] = _pending
        resp = client.get("/api/v1/notebook-entries")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403

    def test_returns_entries_with_pagination(self, client):
        user = _make_active_farmer()
        entry = _make_entry(org_id=user.organization_id)
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.notebook_entries.NotebookService") as MockSvc:
            MockSvc.return_value.list_entries.return_value = ([entry], 1)
            resp = client.get("/api/v1/notebook-entries")
        app.dependency_overrides.pop(require_active_membership, None)
        body = resp.json()
        assert body["pagination"]["total_records"] == 1
        assert len(body["data"]) == 1

    def test_filter_by_entry_type_consultation(self, client):
        user = _make_active_farmer()
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.notebook_entries.NotebookService") as MockSvc:
            MockSvc.return_value.list_entries.return_value = ([], 0)
            resp = client.get("/api/v1/notebook-entries?entry_type=consultation")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200
        _, kwargs = MockSvc.return_value.list_entries.call_args
        assert kwargs.get("entry_type") == "consultation"


class TestGetNotebookEntry:
    def test_active_user_can_get(self, client):
        user = _make_active_farmer()
        entry_id = uuid4()
        entry = _make_entry(org_id=user.organization_id, entry_id=entry_id)
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.notebook_entries.NotebookService") as MockSvc:
            MockSvc.return_value.get_entry.return_value = entry
            resp = client.get(f"/api/v1/notebook-entries/{entry_id}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200
        assert resp.json()["data"]["entry_id"] == str(entry_id)

    def test_not_found_returns_404(self, client):
        user = _make_active_farmer()
        entry_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.notebook_entries.NotebookService") as MockSvc:
            MockSvc.return_value.get_entry.side_effect = AppError("entry_not_found", "Not found", 404)
            resp = client.get(f"/api/v1/notebook-entries/{entry_id}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 404

    def test_cross_org_access_blocked(self, client):
        user = _make_active_farmer()
        entry_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.notebook_entries.NotebookService") as MockSvc:
            MockSvc.return_value.get_entry.side_effect = AppError(
                "organization_not_accessible", "Org not accessible", 403
            )
            resp = client.get(f"/api/v1/notebook-entries/{entry_id}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403


class TestCreateNotebookEntry:
    def test_active_user_can_create(self, client):
        user = _make_active_farmer()
        org_id = user.organization_id
        payload = {
            "organization_id": str(org_id),
            "entry_type": "note",
            "entry_context": "general_note",
        }
        entry = _make_entry(org_id=org_id)
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.notebook_entries.NotebookService") as MockSvc:
            MockSvc.return_value.create_entry.return_value = entry
            resp = client.post("/api/v1/notebook-entries", json=payload)
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200

    def test_create_consultation_entry(self, client):
        user = _make_active_farmer()
        org_id = user.organization_id
        payload = {
            "organization_id": str(org_id),
            "entry_type": "consultation",
            "entry_context": "general_note",
            "ai_provider": "chatgpt",
        }
        entry = _make_entry(org_id=org_id)
        entry.entry_type = EntryType.consultation
        entry.external_ai = MagicMock(value="chatgpt")
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.notebook_entries.NotebookService") as MockSvc:
            MockSvc.return_value.create_entry.return_value = entry
            resp = client.post("/api/v1/notebook-entries", json=payload)
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200

    def test_missing_organization_id_rejected(self, client):
        user = _make_active_farmer()
        app.dependency_overrides[require_active_membership] = lambda: user
        payload = {"entry_type": "note", "entry_context": "general_note"}
        resp = client.post("/api/v1/notebook-entries", json=payload)
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 422

    def test_invalid_entry_type_rejected(self, client):
        user = _make_active_farmer()
        app.dependency_overrides[require_active_membership] = lambda: user
        payload = {
            "organization_id": str(uuid4()),
            "entry_type": "invalid_type",
            "entry_context": "general_note",
        }
        resp = client.post("/api/v1/notebook-entries", json=payload)
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 422

    def test_cross_org_create_blocked(self, client):
        user = _make_active_farmer()
        app.dependency_overrides[require_active_membership] = lambda: user
        payload = {
            "organization_id": str(uuid4()),
            "entry_type": "note",
            "entry_context": "general_note",
        }
        with patch("app.api.v1.notebook_entries.NotebookService") as MockSvc:
            MockSvc.return_value.create_entry.side_effect = AppError(
                "organization_not_accessible", "Not accessible", 403
            )
            resp = client.post("/api/v1/notebook-entries", json=payload)
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403

    def test_pending_membership_blocked_from_create(self, client):
        def _pending():
            raise AppError("membership_not_active", "not active", 403)
        app.dependency_overrides[require_active_membership] = _pending
        payload = {
            "organization_id": str(uuid4()),
            "entry_type": "note",
            "entry_context": "general_note",
        }
        resp = client.post("/api/v1/notebook-entries", json=payload)
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403

    def test_nullable_farm_zone_tree(self, client):
        user = _make_active_farmer()
        org_id = user.organization_id
        payload = {
            "organization_id": str(org_id),
            "entry_type": "note",
            "entry_context": "external_observation",
            "farm_id": None,
            "zone_id": None,
            "tree_id": None,
        }
        entry = _make_entry(org_id=org_id)
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.notebook_entries.NotebookService") as MockSvc:
            MockSvc.return_value.create_entry.return_value = entry
            resp = client.post("/api/v1/notebook-entries", json=payload)
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200


class TestUpdateNotebookEntry:
    def test_active_user_can_update(self, client):
        user = _make_active_farmer()
        entry_id = uuid4()
        entry = _make_entry(org_id=user.organization_id, entry_id=entry_id)
        entry.title = "Updated"
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.notebook_entries.NotebookService") as MockSvc:
            MockSvc.return_value.update_entry.return_value = entry
            resp = client.patch(
                f"/api/v1/notebook-entries/{entry_id}",
                json={"title": "Updated"},
            )
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200

    def test_unauthenticated_blocked_from_update(self, client):
        entry_id = uuid4()
        resp = client.patch(f"/api/v1/notebook-entries/{entry_id}", json={"title": "X"})
        assert resp.status_code in (401, 403)

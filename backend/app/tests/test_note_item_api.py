"""P2-7: API-level tests for Note Item endpoints."""
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.core.enums import AccountStatus, FarmerStatus, ItemType, MembershipStatus, UploadStatus, UserRole
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


def _make_item(entry_id=None, item_id=None, item_type=ItemType.photo, seq=1):
    m = MagicMock()
    m.id = item_id or uuid4()
    m.entry_id = entry_id or uuid4()
    m.item_type = item_type
    m.sequence_order = seq
    m.content_text = None
    m.file_path = "organizations/org1/entries/e1/photo.jpg"
    m.url = None
    m.platform = None
    m.upload_status = UploadStatus.pending
    m.created_at = MagicMock(isoformat=lambda: "2026-06-29T00:00:00")
    return m


class TestListNoteItems:
    def test_active_user_can_list(self, client):
        user = _make_active_farmer()
        entry_id = uuid4()
        item = _make_item(entry_id=entry_id)
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.note_items.NoteItemService") as MockSvc:
            MockSvc.return_value.list_items.return_value = [item]
            resp = client.get(f"/api/v1/notebook-entries/{entry_id}/items")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200
        assert len(resp.json()["data"]) == 1

    def test_entry_not_found_returns_404(self, client):
        user = _make_active_farmer()
        entry_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.note_items.NoteItemService") as MockSvc:
            MockSvc.return_value.list_items.side_effect = AppError("entry_not_found", "Not found", 404)
            resp = client.get(f"/api/v1/notebook-entries/{entry_id}/items")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 404

    def test_pending_membership_blocked(self, client):
        def _pending():
            raise AppError("membership_not_active", "not active", 403)
        app.dependency_overrides[require_active_membership] = _pending
        entry_id = uuid4()
        resp = client.get(f"/api/v1/notebook-entries/{entry_id}/items")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403


class TestCreateNoteItem:
    def test_active_user_can_create_photo(self, client):
        user = _make_active_farmer()
        entry_id = uuid4()
        item = _make_item(entry_id=entry_id)
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.note_items.NoteItemService") as MockSvc:
            MockSvc.return_value.create_item.return_value = item
            resp = client.post(
                f"/api/v1/notebook-entries/{entry_id}/items",
                json={"item_type": "photo", "file_path": "organizations/org1/entries/e1/photo.jpg"},
            )
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200

    def test_text_item_created(self, client):
        user = _make_active_farmer()
        entry_id = uuid4()
        item = _make_item(entry_id=entry_id, item_type=ItemType.text)
        item.content_text = "Field observation"
        item.file_path = None
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.note_items.NoteItemService") as MockSvc:
            MockSvc.return_value.create_item.return_value = item
            resp = client.post(
                f"/api/v1/notebook-entries/{entry_id}/items",
                json={"item_type": "text", "content_text": "Field observation"},
            )
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200

    def test_link_item_created(self, client):
        user = _make_active_farmer()
        entry_id = uuid4()
        item = _make_item(entry_id=entry_id, item_type=ItemType.link)
        item.url = "https://youtube.com/watch?v=abc"
        item.file_path = None
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.note_items.NoteItemService") as MockSvc:
            MockSvc.return_value.create_item.return_value = item
            resp = client.post(
                f"/api/v1/notebook-entries/{entry_id}/items",
                json={"item_type": "link", "url": "https://youtube.com/watch?v=abc"},
            )
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200

    def test_invalid_item_type_rejected(self, client):
        user = _make_active_farmer()
        entry_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: user
        resp = client.post(
            f"/api/v1/notebook-entries/{entry_id}/items",
            json={"item_type": "invalid_type"},
        )
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 422

    def test_parent_entry_not_accessible_blocked(self, client):
        user = _make_active_farmer()
        entry_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.note_items.NoteItemService") as MockSvc:
            MockSvc.return_value.create_item.side_effect = AppError(
                "entry_not_accessible", "Not accessible", 403
            )
            resp = client.post(
                f"/api/v1/notebook-entries/{entry_id}/items",
                json={"item_type": "photo"},
            )
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403

    def test_unauthenticated_blocked(self, client):
        entry_id = uuid4()
        resp = client.post(
            f"/api/v1/notebook-entries/{entry_id}/items",
            json={"item_type": "photo"},
        )
        assert resp.status_code in (401, 403)


class TestUpdateNoteItem:
    def test_active_user_can_update(self, client):
        user = _make_active_farmer()
        item_id = uuid4()
        item = _make_item(item_id=item_id)
        item.sequence_order = 2
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.note_items.NoteItemService") as MockSvc:
            MockSvc.return_value.update_item.return_value = item
            resp = client.patch(f"/api/v1/note-items/{item_id}", json={"sequence_order": 2})
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200

    def test_item_not_found_returns_404(self, client):
        user = _make_active_farmer()
        item_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.note_items.NoteItemService") as MockSvc:
            MockSvc.return_value.update_item.side_effect = AppError("item_not_found", "Not found", 404)
            resp = client.patch(f"/api/v1/note-items/{item_id}", json={"sequence_order": 2})
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 404

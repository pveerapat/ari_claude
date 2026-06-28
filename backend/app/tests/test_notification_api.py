"""P2-7: API-level tests for Notification endpoints."""
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.core.enums import AccountStatus, FarmerStatus, MembershipStatus, UserRole
from app.core.errors import AppError
from app.dependencies.auth import require_active_account
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


def _make_active_user(org_id=None):
    user = MagicMock()
    user.id = uuid4()
    user.organization_id = org_id or uuid4()
    user.role = UserRole.farmer
    user.farmer_status = FarmerStatus.owner
    user.membership_status = MembershipStatus.active
    user.account_status = AccountStatus.active
    return user


def _make_notification(user_id=None, notif_id=None):
    m = MagicMock()
    m.id = notif_id or uuid4()
    m.user_id = user_id or uuid4()
    m.type = "follow_up_reminder"
    m.message = "Time to check follow-up"
    m.status = "unread"
    m.read_at = None
    m.created_at = MagicMock(isoformat=lambda: "2026-06-29T00:00:00")
    return m


class TestListNotifications:
    def test_active_user_can_list(self, client):
        user = _make_active_user()
        notif = _make_notification(user_id=user.id)
        app.dependency_overrides[require_active_account] = lambda: user
        with patch("app.api.v1.notifications.NotificationService") as MockSvc:
            MockSvc.return_value.list_notifications.return_value = ([notif], 1)
            resp = client.get("/api/v1/notifications")
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 200
        assert resp.json()["pagination"]["total_records"] == 1

    def test_unauthenticated_blocked(self, client):
        resp = client.get("/api/v1/notifications")
        assert resp.status_code in (401, 403)

    def test_own_user_scope(self, client):
        user = _make_active_user()
        app.dependency_overrides[require_active_account] = lambda: user
        with patch("app.api.v1.notifications.NotificationService") as MockSvc:
            MockSvc.return_value.list_notifications.return_value = ([], 0)
            resp = client.get("/api/v1/notifications")
        app.dependency_overrides.pop(require_active_account, None)
        _, kwargs = MockSvc.return_value.list_notifications.call_args
        assert kwargs["user"].id == user.id


class TestGetNotification:
    def test_active_user_can_get_own(self, client):
        user = _make_active_user()
        notif_id = uuid4()
        notif = _make_notification(user_id=user.id, notif_id=notif_id)
        app.dependency_overrides[require_active_account] = lambda: user
        with patch("app.api.v1.notifications.NotificationService") as MockSvc:
            MockSvc.return_value.get_notification.return_value = notif
            resp = client.get(f"/api/v1/notifications/{notif_id}")
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 200

    def test_cannot_access_other_user_notification(self, client):
        user = _make_active_user()
        notif_id = uuid4()
        app.dependency_overrides[require_active_account] = lambda: user
        with patch("app.api.v1.notifications.NotificationService") as MockSvc:
            MockSvc.return_value.get_notification.side_effect = AppError(
                "notification_not_accessible", "Not accessible", 403
            )
            resp = client.get(f"/api/v1/notifications/{notif_id}")
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 403


class TestMarkNotificationRead:
    def test_mark_read_success(self, client):
        user = _make_active_user()
        notif_id = uuid4()
        notif = _make_notification(user_id=user.id, notif_id=notif_id)
        notif.status = "read"
        app.dependency_overrides[require_active_account] = lambda: user
        with patch("app.api.v1.notifications.NotificationService") as MockSvc:
            MockSvc.return_value.mark_read.return_value = notif
            resp = client.patch(f"/api/v1/notifications/{notif_id}/read")
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 200
        assert resp.json()["data"]["status"] == "read"

    def test_mark_read_not_found(self, client):
        user = _make_active_user()
        notif_id = uuid4()
        app.dependency_overrides[require_active_account] = lambda: user
        with patch("app.api.v1.notifications.NotificationService") as MockSvc:
            MockSvc.return_value.mark_read.side_effect = AppError(
                "notification_not_found", "Not found", 404
            )
            resp = client.patch(f"/api/v1/notifications/{notif_id}/read")
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 404


class TestMarkAllNotificationsRead:
    def test_mark_all_read_success(self, client):
        user = _make_active_user()
        app.dependency_overrides[require_active_account] = lambda: user
        with patch("app.api.v1.notifications.NotificationService") as MockSvc:
            MockSvc.return_value.mark_all_read.return_value = 5
            resp = client.post("/api/v1/notifications/mark-all-read")
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 200
        assert resp.json()["data"]["success"] is True
        assert resp.json()["data"]["updated_count"] == 5

    def test_unauthenticated_blocked(self, client):
        resp = client.post("/api/v1/notifications/mark-all-read")
        assert resp.status_code in (401, 403)

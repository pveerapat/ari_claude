"""P2-7: API-level tests for Follow-Up endpoints."""
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.core.enums import AccountStatus, FarmerStatus, FollowUpOutcome, MembershipStatus, UserRole
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


def _make_follow_up(entry_id=None, fu_id=None, day=7):
    m = MagicMock()
    m.id = fu_id or uuid4()
    m.entry_id = entry_id or uuid4()
    m.follow_up_day = day
    m.outcome = None
    m.notes = None
    m.recorded_at = MagicMock(isoformat=lambda: "2026-06-29T00:00:00")
    return m


class TestListFollowUps:
    def test_active_user_can_list(self, client):
        user = _make_active_farmer()
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.follow_ups.FollowUpService") as MockSvc:
            MockSvc.return_value.list_follow_ups.return_value = ([], 0)
            resp = client.get("/api/v1/follow-ups")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200

    def test_unauthenticated_blocked(self, client):
        resp = client.get("/api/v1/follow-ups")
        assert resp.status_code in (401, 403)

    def test_pending_membership_blocked(self, client):
        def _pending():
            raise AppError("membership_not_active", "not active", 403)
        app.dependency_overrides[require_active_membership] = _pending
        resp = client.get("/api/v1/follow-ups")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403


class TestGetFollowUp:
    def test_active_user_can_get(self, client):
        user = _make_active_farmer()
        fu_id = uuid4()
        fu = _make_follow_up(fu_id=fu_id)
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.follow_ups.FollowUpService") as MockSvc:
            MockSvc.return_value.get_follow_up.return_value = fu
            resp = client.get(f"/api/v1/follow-ups/{fu_id}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200

    def test_not_found_returns_404(self, client):
        user = _make_active_farmer()
        fu_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.follow_ups.FollowUpService") as MockSvc:
            MockSvc.return_value.get_follow_up.side_effect = AppError("follow_up_not_found", "Not found", 404)
            resp = client.get(f"/api/v1/follow-ups/{fu_id}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 404


class TestCreateFollowUp:
    def test_active_user_can_create_7_day(self, client):
        user = _make_active_farmer()
        entry_id = uuid4()
        fu = _make_follow_up(entry_id=entry_id, day=7)
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.follow_ups.FollowUpService") as MockSvc:
            MockSvc.return_value.create_follow_up.return_value = fu
            resp = client.post("/api/v1/follow-ups", json={"entry_id": str(entry_id), "follow_up_day": 7})
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200

    def test_create_3_day_follow_up(self, client):
        user = _make_active_farmer()
        entry_id = uuid4()
        fu = _make_follow_up(entry_id=entry_id, day=3)
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.follow_ups.FollowUpService") as MockSvc:
            MockSvc.return_value.create_follow_up.return_value = fu
            resp = client.post("/api/v1/follow-ups", json={"entry_id": str(entry_id), "follow_up_day": 3})
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200

    def test_create_14_day_follow_up(self, client):
        user = _make_active_farmer()
        entry_id = uuid4()
        fu = _make_follow_up(entry_id=entry_id, day=14)
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.follow_ups.FollowUpService") as MockSvc:
            MockSvc.return_value.create_follow_up.return_value = fu
            resp = client.post("/api/v1/follow-ups", json={"entry_id": str(entry_id), "follow_up_day": 14})
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200

    def test_invalid_follow_up_day_rejected(self, client):
        user = _make_active_farmer()
        entry_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: user
        resp = client.post(
            "/api/v1/follow-ups", json={"entry_id": str(entry_id), "follow_up_day": 5}
        )
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 422

    def test_parent_entry_inaccessible_blocked(self, client):
        user = _make_active_farmer()
        entry_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.follow_ups.FollowUpService") as MockSvc:
            MockSvc.return_value.create_follow_up.side_effect = AppError(
                "entry_not_accessible", "Not accessible", 403
            )
            resp = client.post("/api/v1/follow-ups", json={"entry_id": str(entry_id), "follow_up_day": 7})
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403


class TestUpdateFollowUp:
    def test_active_user_can_record_outcome(self, client):
        user = _make_active_farmer()
        fu_id = uuid4()
        fu = _make_follow_up(fu_id=fu_id)
        fu.outcome = FollowUpOutcome.improved
        fu.notes = "Symptoms improved"
        app.dependency_overrides[require_active_membership] = lambda: user
        with patch("app.api.v1.follow_ups.FollowUpService") as MockSvc:
            MockSvc.return_value.update_follow_up.return_value = fu
            resp = client.patch(
                f"/api/v1/follow-ups/{fu_id}",
                json={"outcome": "improved", "notes": "Symptoms improved"},
            )
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200

    def test_invalid_outcome_rejected(self, client):
        user = _make_active_farmer()
        fu_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: user
        resp = client.patch(f"/api/v1/follow-ups/{fu_id}", json={"outcome": "bad_outcome"})
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 422

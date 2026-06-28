"""P2-6: API-level tests for Zone endpoints with mocked service and dependencies."""

from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.core.enums import AccountStatus, FarmerStatus, MembershipStatus, UserRole
from app.core.errors import AppError
from app.dependencies.auth import require_active_account, require_active_membership
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


def _make_owner(org_id=None):
    user = MagicMock()
    user.id = uuid4()
    user.organization_id = org_id or uuid4()
    user.role = UserRole.farmer
    user.farmer_status = FarmerStatus.owner
    user.membership_status = MembershipStatus.active
    user.account_status = AccountStatus.active_pending_verification
    user.primary_farm_id = None
    return user


def _make_member(farmer_status=FarmerStatus.owner_family, membership=MembershipStatus.pending_farm_approval):
    user = MagicMock()
    user.id = uuid4()
    user.organization_id = uuid4()
    user.role = UserRole.farmer
    user.farmer_status = farmer_status
    user.membership_status = membership
    user.account_status = AccountStatus.active
    user.primary_farm_id = uuid4()
    return user


def _make_mock_zone(farm_id=None):
    z = MagicMock()
    z.id = uuid4()
    z.farm_id = farm_id or uuid4()
    z.name = "North Zone"
    z.description = None
    z.created_at = None
    z.updated_at = None
    return z


# ---------------------------------------------------------------------------
# GET /api/v1/zones
# ---------------------------------------------------------------------------

class TestListZones:
    def test_owner_can_list_zones(self, client):
        owner = _make_owner()
        farm_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: owner
        mock_zone = _make_mock_zone(farm_id)
        with patch("app.api.v1.zones.ZoneService") as MockSvc:
            MockSvc.return_value.list_zones.return_value = ([mock_zone], 1)
            resp = client.get(f"/api/v1/zones?farm_id={farm_id}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200
        body = resp.json()
        assert "data" in body
        assert "pagination" in body

    def test_list_zones_filters_by_accessible_farm(self, client):
        owner = _make_owner()
        farm_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: owner
        with patch("app.api.v1.zones.ZoneService") as MockSvc:
            MockSvc.return_value.list_zones.side_effect = AppError(
                "farm_not_accessible", "Farm is not accessible", 403
            )
            resp = client.get(f"/api/v1/zones?farm_id={farm_id}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403

    def test_pending_membership_blocked_from_list(self, client):
        from app.core.errors import AppError as _AppError
        def _pending():
            raise _AppError("membership_not_active", "Farm membership is not active", 403)
        app.dependency_overrides[require_active_membership] = _pending
        resp = client.get("/api/v1/zones")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# GET /api/v1/zones/{zone_id}
# ---------------------------------------------------------------------------

class TestGetZone:
    def test_owner_can_get_zone(self, client):
        owner = _make_owner()
        zone_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: owner
        mock_zone = _make_mock_zone()
        mock_zone.id = zone_id
        with patch("app.api.v1.zones.ZoneService") as MockSvc:
            MockSvc.return_value.get_zone.return_value = mock_zone
            resp = client.get(f"/api/v1/zones/{zone_id}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200

    def test_inaccessible_zone_blocked(self, client):
        owner = _make_owner()
        zone_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: owner
        with patch("app.api.v1.zones.ZoneService") as MockSvc:
            MockSvc.return_value.get_zone.side_effect = AppError(
                "farm_not_accessible", "Farm is not accessible", 403
            )
            resp = client.get(f"/api/v1/zones/{zone_id}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403

    def test_missing_zone_returns_404(self, client):
        owner = _make_owner()
        zone_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: owner
        with patch("app.api.v1.zones.ZoneService") as MockSvc:
            MockSvc.return_value.get_zone.side_effect = AppError("zone_not_found", "Zone not found", 404)
            resp = client.get(f"/api/v1/zones/{zone_id}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# POST /api/v1/zones
# ---------------------------------------------------------------------------

class TestCreateZone:
    def _payload(self, farm_id=None):
        return {"farm_id": str(farm_id or uuid4()), "zone_name": "North Zone"}

    def test_owner_can_create_zone_under_own_farm(self, client):
        owner = _make_owner()
        farm_id = uuid4()
        app.dependency_overrides[require_active_account] = lambda: owner
        mock_zone = _make_mock_zone(farm_id)
        with patch("app.api.v1.zones.ZoneService") as MockSvc:
            MockSvc.return_value.create_zone.return_value = mock_zone
            resp = client.post("/api/v1/zones", json=self._payload(farm_id))
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 200

    def test_owner_cannot_create_zone_under_inaccessible_farm(self, client):
        owner = _make_owner()
        farm_id = uuid4()
        app.dependency_overrides[require_active_account] = lambda: owner
        with patch("app.api.v1.zones.ZoneService") as MockSvc:
            MockSvc.return_value.create_zone.side_effect = AppError(
                "farm_not_accessible", "Farm is not accessible", 403
            )
            resp = client.post("/api/v1/zones", json=self._payload(farm_id))
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 403

    def test_owner_family_cannot_create_zone(self, client):
        user = _make_member(FarmerStatus.owner_family, MembershipStatus.active)
        app.dependency_overrides[require_active_account] = lambda: user
        with patch("app.api.v1.zones.ZoneService") as MockSvc:
            MockSvc.return_value.create_zone.side_effect = AppError(
                "zone_create_forbidden", "Only farm owners can perform this action", 403
            )
            resp = client.post("/api/v1/zones", json=self._payload())
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 403

    def test_farm_staff_cannot_create_zone(self, client):
        user = _make_member(FarmerStatus.farm_staff, MembershipStatus.active)
        app.dependency_overrides[require_active_account] = lambda: user
        with patch("app.api.v1.zones.ZoneService") as MockSvc:
            MockSvc.return_value.create_zone.side_effect = AppError(
                "zone_create_forbidden", "Only farm owners can perform this action", 403
            )
            resp = client.post("/api/v1/zones", json=self._payload())
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 403

    def test_missing_farm_id_rejected(self, client):
        owner = _make_owner()
        app.dependency_overrides[require_active_account] = lambda: owner
        resp = client.post("/api/v1/zones", json={"zone_name": "Zone"})
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 422

    def test_missing_zone_name_rejected(self, client):
        owner = _make_owner()
        app.dependency_overrides[require_active_account] = lambda: owner
        resp = client.post("/api/v1/zones", json={"farm_id": str(uuid4())})
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# PATCH /api/v1/zones/{zone_id}
# ---------------------------------------------------------------------------

class TestUpdateZone:
    def test_owner_can_update_zone(self, client):
        owner = _make_owner()
        zone_id = uuid4()
        app.dependency_overrides[require_active_account] = lambda: owner
        mock_zone = _make_mock_zone()
        mock_zone.id = zone_id
        mock_zone.name = "Updated Zone"
        with patch("app.api.v1.zones.ZoneService") as MockSvc:
            MockSvc.return_value.update_zone.return_value = mock_zone
            resp = client.patch(f"/api/v1/zones/{zone_id}", json={"zone_name": "Updated Zone"})
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 200
        assert resp.json()["data"]["zone_name"] == "Updated Zone"

    def test_cannot_move_zone_to_another_farm(self, client):
        """farm_id reassignment is not allowed; ZoneUpdate schema has no farm_id field."""
        owner = _make_owner()
        zone_id = uuid4()
        app.dependency_overrides[require_active_account] = lambda: owner
        mock_zone = _make_mock_zone()
        mock_zone.id = zone_id
        with patch("app.api.v1.zones.ZoneService") as MockSvc:
            MockSvc.return_value.update_zone.return_value = mock_zone
            # farm_id in body is silently ignored (not a ZoneUpdate field)
            resp = client.patch(
                f"/api/v1/zones/{zone_id}",
                json={"zone_name": "Zone", "farm_id": str(uuid4())},
            )
        app.dependency_overrides.pop(require_active_account, None)
        # Request is accepted but farm_id is not changed
        assert resp.status_code == 200

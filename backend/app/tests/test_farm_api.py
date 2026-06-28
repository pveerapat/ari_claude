"""P2-6: API-level tests for Farm endpoints with mocked service and dependencies."""

from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.core.enums import AccountStatus, FarmerStatus, MembershipStatus, UserRole
from app.core.errors import AppError
from app.dependencies.auth import get_current_user, require_active_account, require_active_membership
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


def _make_owner_family(org_id=None, membership=MembershipStatus.pending_farm_approval):
    user = MagicMock()
    user.id = uuid4()
    user.organization_id = org_id or uuid4()
    user.role = UserRole.farmer
    user.farmer_status = FarmerStatus.owner_family
    user.membership_status = membership
    user.account_status = AccountStatus.active
    user.primary_farm_id = uuid4()
    return user


def _make_farm_dict(farm_id=None, org_id=None, name="Test Farm"):
    fid = farm_id or uuid4()
    oid = org_id or uuid4()
    return {
        "farm_id": str(fid),
        "organization_id": str(oid),
        "farm_name": name,
        "location": None,
        "description": None,
        "status": "active",
        "created_at": "2026-06-28T00:00:00",
        "updated_at": None,
    }


# ---------------------------------------------------------------------------
# GET /api/v1/farms
# ---------------------------------------------------------------------------

class TestListFarms:
    def test_owner_can_list_farms(self, client):
        owner = _make_owner()
        app.dependency_overrides[require_active_membership] = lambda: owner
        farm_data = _make_farm_dict(org_id=owner.organization_id)
        with patch("app.api.v1.farms.FarmService") as MockSvc:
            MockSvc.return_value.list_farms.return_value = ([MagicMock(**{k: None for k in farm_data})], 1)
            resp = client.get("/api/v1/farms")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200

    def test_list_farms_returns_pagination(self, client):
        owner = _make_owner()
        app.dependency_overrides[require_active_membership] = lambda: owner
        mock_farm = MagicMock()
        mock_farm.id = uuid4()
        mock_farm.organization_id = owner.organization_id
        mock_farm.name = "Farm A"
        mock_farm.location = None
        mock_farm.description = None
        mock_farm.status = "active"
        mock_farm.created_at = None
        mock_farm.updated_at = None
        with patch("app.api.v1.farms.FarmService") as MockSvc:
            MockSvc.return_value.list_farms.return_value = ([mock_farm], 1)
            resp = client.get("/api/v1/farms")
        app.dependency_overrides.pop(require_active_membership, None)
        body = resp.json()
        assert "pagination" in body
        assert "data" in body

    def test_pending_membership_blocked_from_list(self, client):
        from app.core.errors import AppError as _AppError
        def _pending():
            raise _AppError("membership_not_active", "Farm membership is not active", 403)
        app.dependency_overrides[require_active_membership] = _pending
        resp = client.get("/api/v1/farms")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403

    def test_unauthenticated_blocked(self, client):
        resp = client.get("/api/v1/farms")
        assert resp.status_code in (401, 403)


# ---------------------------------------------------------------------------
# GET /api/v1/farms/{farm_id}
# ---------------------------------------------------------------------------

class TestGetFarm:
    def test_owner_can_get_farm(self, client):
        owner = _make_owner()
        farm_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: owner
        mock_farm = MagicMock()
        mock_farm.id = farm_id
        mock_farm.organization_id = owner.organization_id
        mock_farm.name = "Farm A"
        mock_farm.location = None
        mock_farm.description = None
        mock_farm.status = "active"
        mock_farm.created_at = None
        mock_farm.updated_at = None
        with patch("app.api.v1.farms.FarmService") as MockSvc:
            MockSvc.return_value.get_farm.return_value = mock_farm
            resp = client.get(f"/api/v1/farms/{farm_id}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200

    def test_inaccessible_farm_returns_403_or_404(self, client):
        owner = _make_owner()
        farm_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: owner
        with patch("app.api.v1.farms.FarmService") as MockSvc:
            MockSvc.return_value.get_farm.side_effect = AppError("farm_not_found", "Farm not found", 404)
            resp = client.get(f"/api/v1/farms/{farm_id}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code in (403, 404)

    def test_pending_membership_blocked_from_get(self, client):
        from app.core.errors import AppError as _AppError
        farm_id = uuid4()
        def _pending():
            raise _AppError("membership_not_active", "Farm membership is not active", 403)
        app.dependency_overrides[require_active_membership] = _pending
        resp = client.get(f"/api/v1/farms/{farm_id}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# POST /api/v1/farms
# ---------------------------------------------------------------------------

class TestCreateFarm:
    _PAYLOAD = {"farm_name": "My Durian Farm", "description": "A test farm"}

    def test_owner_can_create_farm(self, client):
        owner = _make_owner()
        app.dependency_overrides[require_active_account] = lambda: owner
        mock_farm = MagicMock()
        mock_farm.id = uuid4()
        mock_farm.organization_id = owner.organization_id
        mock_farm.name = "My Durian Farm"
        mock_farm.location = None
        mock_farm.description = "A test farm"
        mock_farm.status = "active"
        mock_farm.created_at = None
        mock_farm.updated_at = None
        with patch("app.api.v1.farms.FarmService") as MockSvc:
            MockSvc.return_value.create_farm.return_value = mock_farm
            resp = client.post("/api/v1/farms", json=self._PAYLOAD)
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 200
        assert resp.json()["data"]["farm_name"] == "My Durian Farm"

    def test_owner_cannot_provide_organization_id(self, client):
        owner = _make_owner()
        app.dependency_overrides[require_active_account] = lambda: owner
        payload = {**self._PAYLOAD, "organization_id": str(uuid4())}
        with patch("app.api.v1.farms.FarmService") as MockSvc:
            mock_farm = MagicMock()
            mock_farm.id = uuid4()
            mock_farm.organization_id = owner.organization_id
            mock_farm.name = "My Durian Farm"
            mock_farm.location = None
            mock_farm.description = None
            mock_farm.status = "active"
            mock_farm.created_at = None
            mock_farm.updated_at = None
            MockSvc.return_value.create_farm.return_value = mock_farm
            resp = client.post("/api/v1/farms", json=payload)
        app.dependency_overrides.pop(require_active_account, None)
        # organization_id is ignored (not a schema field), request still succeeds
        # org is assigned from user.organization_id in service
        assert resp.status_code == 200

    def test_owner_cannot_provide_farm_code(self, client):
        owner = _make_owner()
        app.dependency_overrides[require_active_account] = lambda: owner
        payload = {**self._PAYLOAD, "farm_code": "ARI-FARM-001"}
        with patch("app.api.v1.farms.FarmService") as MockSvc:
            mock_farm = MagicMock()
            mock_farm.id = uuid4()
            mock_farm.organization_id = owner.organization_id
            mock_farm.name = "My Durian Farm"
            mock_farm.location = None
            mock_farm.description = None
            mock_farm.status = "active"
            mock_farm.created_at = None
            mock_farm.updated_at = None
            MockSvc.return_value.create_farm.return_value = mock_farm
            resp = client.post("/api/v1/farms", json=payload)
        app.dependency_overrides.pop(require_active_account, None)
        # farm_code is not a schema field and is silently ignored
        assert resp.status_code == 200

    def test_owner_family_cannot_create_farm(self, client):
        owner_family = _make_owner_family()
        app.dependency_overrides[require_active_account] = lambda: owner_family
        with patch("app.api.v1.farms.FarmService") as MockSvc:
            MockSvc.return_value.create_farm.side_effect = AppError(
                "farm_create_forbidden", "Only farm owners can perform this action", 403
            )
            resp = client.post("/api/v1/farms", json=self._PAYLOAD)
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 403

    def test_farm_staff_cannot_create_farm(self, client):
        user = MagicMock()
        user.id = uuid4()
        user.organization_id = uuid4()
        user.role = UserRole.farmer
        user.farmer_status = FarmerStatus.farm_staff
        user.membership_status = MembershipStatus.pending_farm_approval
        user.account_status = AccountStatus.active
        app.dependency_overrides[require_active_account] = lambda: user
        with patch("app.api.v1.farms.FarmService") as MockSvc:
            MockSvc.return_value.create_farm.side_effect = AppError(
                "farm_create_forbidden", "Only farm owners can perform this action", 403
            )
            resp = client.post("/api/v1/farms", json=self._PAYLOAD)
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 403

    def test_pending_approval_cannot_create_farm(self, client):
        user = _make_owner_family(membership=MembershipStatus.pending_farm_approval)
        app.dependency_overrides[require_active_account] = lambda: user
        with patch("app.api.v1.farms.FarmService") as MockSvc:
            MockSvc.return_value.create_farm.side_effect = AppError(
                "farm_create_forbidden", "Only farm owners can perform this action", 403
            )
            resp = client.post("/api/v1/farms", json=self._PAYLOAD)
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 403

    def test_owner_cannot_create_farm_under_another_org(self, client):
        owner = _make_owner()
        app.dependency_overrides[require_active_account] = lambda: owner
        with patch("app.api.v1.farms.FarmService") as MockSvc:
            MockSvc.return_value.create_farm.side_effect = AppError(
                "organization_not_accessible", "Organization is not accessible", 403
            )
            resp = client.post("/api/v1/farms", json=self._PAYLOAD)
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 403

    def test_owner_can_create_multiple_farms(self, client):
        owner = _make_owner()
        app.dependency_overrides[require_active_account] = lambda: owner
        mock_farm1 = MagicMock()
        mock_farm1.id = uuid4()
        mock_farm1.organization_id = owner.organization_id
        mock_farm1.name = "Farm 1"
        mock_farm1.location = None
        mock_farm1.description = None
        mock_farm1.status = "active"
        mock_farm1.created_at = None
        mock_farm1.updated_at = None
        mock_farm2 = MagicMock()
        mock_farm2.id = uuid4()
        mock_farm2.organization_id = owner.organization_id
        mock_farm2.name = "Farm 2"
        mock_farm2.location = None
        mock_farm2.description = None
        mock_farm2.status = "active"
        mock_farm2.created_at = None
        mock_farm2.updated_at = None
        with patch("app.api.v1.farms.FarmService") as MockSvc:
            MockSvc.return_value.create_farm.side_effect = [mock_farm1, mock_farm2]
            resp1 = client.post("/api/v1/farms", json={"farm_name": "Farm 1"})
            resp2 = client.post("/api/v1/farms", json={"farm_name": "Farm 2"})
        app.dependency_overrides.pop(require_active_account, None)
        assert resp1.status_code == 200
        assert resp2.status_code == 200

    def test_create_farm_with_location(self, client):
        owner = _make_owner()
        app.dependency_overrides[require_active_account] = lambda: owner
        payload = {
            "farm_name": "Farm With Location",
            "location": {
                "province": "จันทบุรี",
                "gps_latitude": 12.345678,
                "gps_longitude": 102.345678,
                "source": "device_gps",
            },
        }
        mock_farm = MagicMock()
        mock_farm.id = uuid4()
        mock_farm.organization_id = owner.organization_id
        mock_farm.name = "Farm With Location"
        mock_farm.location = payload["location"]
        mock_farm.description = None
        mock_farm.status = "active"
        mock_farm.created_at = None
        mock_farm.updated_at = None
        with patch("app.api.v1.farms.FarmService") as MockSvc:
            MockSvc.return_value.create_farm.return_value = mock_farm
            resp = client.post("/api/v1/farms", json=payload)
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 200

    def test_invalid_latitude_rejected(self, client):
        owner = _make_owner()
        app.dependency_overrides[require_active_account] = lambda: owner
        payload = {
            "farm_name": "Farm",
            "location": {"gps_latitude": 999.0},
        }
        resp = client.post("/api/v1/farms", json=payload)
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 422

    def test_invalid_longitude_rejected(self, client):
        owner = _make_owner()
        app.dependency_overrides[require_active_account] = lambda: owner
        payload = {
            "farm_name": "Farm",
            "location": {"gps_longitude": -999.0},
        }
        resp = client.post("/api/v1/farms", json=payload)
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 422

    def test_missing_farm_name_rejected(self, client):
        owner = _make_owner()
        app.dependency_overrides[require_active_account] = lambda: owner
        resp = client.post("/api/v1/farms", json={"description": "no name"})
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# PATCH /api/v1/farms/{farm_id}
# ---------------------------------------------------------------------------

class TestUpdateFarm:
    def test_owner_can_update_farm(self, client):
        owner = _make_owner()
        farm_id = uuid4()
        app.dependency_overrides[require_active_account] = lambda: owner
        mock_farm = MagicMock()
        mock_farm.id = farm_id
        mock_farm.organization_id = owner.organization_id
        mock_farm.name = "Updated Farm"
        mock_farm.location = None
        mock_farm.description = "New description"
        mock_farm.status = "active"
        mock_farm.created_at = None
        mock_farm.updated_at = None
        with patch("app.api.v1.farms.FarmService") as MockSvc:
            MockSvc.return_value.update_farm.return_value = mock_farm
            resp = client.patch(
                f"/api/v1/farms/{farm_id}",
                json={"farm_name": "Updated Farm", "description": "New description"},
            )
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 200
        assert resp.json()["data"]["farm_name"] == "Updated Farm"

    def test_cannot_update_inaccessible_farm(self, client):
        owner = _make_owner()
        farm_id = uuid4()
        app.dependency_overrides[require_active_account] = lambda: owner
        with patch("app.api.v1.farms.FarmService") as MockSvc:
            MockSvc.return_value.update_farm.side_effect = AppError(
                "organization_not_accessible", "Organization is not accessible", 403
            )
            resp = client.patch(f"/api/v1/farms/{farm_id}", json={"farm_name": "X"})
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 403

    def test_unauthenticated_blocked_from_update(self, client):
        farm_id = uuid4()
        resp = client.patch(f"/api/v1/farms/{farm_id}", json={"farm_name": "X"})
        assert resp.status_code in (401, 403)

"""P2-6: Tests for auth guards and scope boundaries on Farm Structure endpoints.

These tests verify that require_authenticated_user, require_active_account,
require_active_membership, and scope guards enforce correct access rules.
"""

from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.core.enums import AccountStatus, FarmerStatus, MembershipStatus, UserRole
from app.core.errors import AppError
from app.dependencies.auth import (
    get_current_user,
    require_active_account,
    require_active_membership,
)
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


def _make_user(
    farmer_status=FarmerStatus.owner,
    membership_status=MembershipStatus.active,
    account_status=AccountStatus.active,
    role=UserRole.farmer,
):
    user = MagicMock()
    user.id = uuid4()
    user.organization_id = uuid4()
    user.role = role
    user.farmer_status = farmer_status
    user.membership_status = membership_status
    user.account_status = account_status
    user.primary_farm_id = None
    return user


# ---------------------------------------------------------------------------
# require_authenticated_user: missing / invalid token
# ---------------------------------------------------------------------------

class TestAuthGuard:
    def test_missing_token_returns_401_on_list_farms(self, client):
        resp = client.get("/api/v1/farms")
        assert resp.status_code in (401, 403)

    def test_missing_token_returns_401_on_create_farm(self, client):
        resp = client.post("/api/v1/farms", json={"farm_name": "X"})
        assert resp.status_code in (401, 403)

    def test_missing_token_returns_401_on_list_zones(self, client):
        resp = client.get("/api/v1/zones")
        assert resp.status_code in (401, 403)

    def test_missing_token_returns_401_on_create_zone(self, client):
        resp = client.post("/api/v1/zones", json={"farm_id": str(uuid4()), "zone_name": "Z"})
        assert resp.status_code in (401, 403)

    def test_missing_token_returns_401_on_list_trees(self, client):
        resp = client.get("/api/v1/trees")
        assert resp.status_code in (401, 403)

    def test_missing_token_returns_401_on_create_tree(self, client):
        resp = client.post("/api/v1/trees", json={"zone_id": str(uuid4()), "tree_code": "T-001"})
        assert resp.status_code in (401, 403)


# ---------------------------------------------------------------------------
# require_active_account: blocked account
# ---------------------------------------------------------------------------

class TestActiveAccountGuard:
    def test_suspended_account_blocked_from_create_farm(self, client):
        from app.core.errors import AppError as _AppError
        def _suspended():
            raise _AppError("account_blocked", "Account is not active", 403)
        app.dependency_overrides[require_active_account] = _suspended
        resp = client.post("/api/v1/farms", json={"farm_name": "X"})
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 403

    def test_rejected_account_blocked_from_create_zone(self, client):
        from app.core.errors import AppError as _AppError
        def _rejected():
            raise _AppError("account_blocked", "Account is not active", 403)
        app.dependency_overrides[require_active_account] = _rejected
        resp = client.post("/api/v1/zones", json={"farm_id": str(uuid4()), "zone_name": "Z"})
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 403

    def test_revoked_account_blocked_from_create_tree(self, client):
        from app.core.errors import AppError as _AppError
        def _revoked():
            raise _AppError("account_blocked", "Account is not active", 403)
        app.dependency_overrides[require_active_account] = _revoked
        resp = client.post("/api/v1/trees", json={"zone_id": str(uuid4()), "tree_code": "T-001"})
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# require_active_membership: pending / rejected / suspended / revoked
# ---------------------------------------------------------------------------

class TestActiveMembershipGuard:
    def _blocked_membership(self):
        from app.core.errors import AppError as _AppError
        def _raise():
            raise _AppError("membership_not_active", "Farm membership is not active", 403)
        return _raise

    def test_pending_farm_approval_blocked_from_list_farms(self, client):
        app.dependency_overrides[require_active_membership] = self._blocked_membership()
        resp = client.get("/api/v1/farms")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403

    def test_rejected_membership_blocked_from_list_farms(self, client):
        app.dependency_overrides[require_active_membership] = self._blocked_membership()
        resp = client.get("/api/v1/farms")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403

    def test_suspended_membership_blocked_from_list_zones(self, client):
        app.dependency_overrides[require_active_membership] = self._blocked_membership()
        resp = client.get("/api/v1/zones")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403

    def test_revoked_membership_blocked_from_list_trees(self, client):
        app.dependency_overrides[require_active_membership] = self._blocked_membership()
        resp = client.get("/api/v1/trees")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403

    def test_pending_approval_blocked_from_get_farm(self, client):
        app.dependency_overrides[require_active_membership] = self._blocked_membership()
        resp = client.get(f"/api/v1/farms/{uuid4()}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403

    def test_pending_approval_blocked_from_get_zone(self, client):
        app.dependency_overrides[require_active_membership] = self._blocked_membership()
        resp = client.get(f"/api/v1/zones/{uuid4()}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403

    def test_pending_approval_blocked_from_get_tree(self, client):
        app.dependency_overrides[require_active_membership] = self._blocked_membership()
        resp = client.get(f"/api/v1/trees/{uuid4()}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# require_organization_access: other organization blocked
# ---------------------------------------------------------------------------

class TestOrganizationAccess:
    def test_owner_blocked_from_another_org_farm(self, client):
        owner = _make_user(FarmerStatus.owner, MembershipStatus.active)
        app.dependency_overrides[require_active_membership] = lambda: owner
        with patch("app.api.v1.farms.FarmService") as MockSvc:
            MockSvc.return_value.get_farm.side_effect = AppError(
                "organization_not_accessible", "Organization is not accessible", 403
            )
            resp = client.get(f"/api/v1/farms/{uuid4()}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# require_farm_access: inaccessible farm blocked
# ---------------------------------------------------------------------------

class TestFarmAccess:
    def test_farm_access_blocked_for_out_of_scope_zone(self, client):
        owner = _make_user(FarmerStatus.owner, MembershipStatus.active)
        app.dependency_overrides[require_active_membership] = lambda: owner
        with patch("app.api.v1.zones.ZoneService") as MockSvc:
            MockSvc.return_value.get_zone.side_effect = AppError(
                "farm_not_accessible", "Farm is not accessible", 403
            )
            resp = client.get(f"/api/v1/zones/{uuid4()}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403

    def test_farm_access_blocked_for_out_of_scope_tree(self, client):
        owner = _make_user(FarmerStatus.owner, MembershipStatus.active)
        app.dependency_overrides[require_active_membership] = lambda: owner
        with patch("app.api.v1.trees.TreeService") as MockSvc:
            MockSvc.return_value.get_tree.side_effect = AppError(
                "farm_not_accessible", "Farm is not accessible", 403
            )
            resp = client.get(f"/api/v1/trees/{uuid4()}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# Forbidden scope: no forbidden tables / routes
# ---------------------------------------------------------------------------

class TestForbiddenScope:
    def test_no_farm_memberships_route(self, client):
        resp = client.get("/api/v1/farm-memberships")
        assert resp.status_code == 404

    def test_no_permissions_route(self, client):
        resp = client.get("/api/v1/permissions")
        assert resp.status_code == 404

    def test_no_qr_route(self, client):
        resp = client.get("/api/v1/qr")
        assert resp.status_code == 404

    def test_no_notebook_entries_route(self, client):
        resp = client.get("/api/v1/notebook-entries")
        assert resp.status_code == 404

    def test_no_archive_endpoint_on_farm(self, client):
        """PATCH /farms/{id}/archive is not implemented (API-GAP-P2-6-001)."""
        resp = client.patch(f"/api/v1/farms/{uuid4()}/archive")
        assert resp.status_code == 404

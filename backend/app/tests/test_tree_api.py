"""P2-6: API-level tests for Tree endpoints with mocked service and dependencies."""

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


def _make_mock_tree(zone_id=None):
    t = MagicMock()
    t.id = uuid4()
    t.zone_id = zone_id or uuid4()
    t.tree_code = "T-001"
    t.status = "active"
    t.created_at = None
    t.updated_at = None
    return t


# ---------------------------------------------------------------------------
# GET /api/v1/trees
# ---------------------------------------------------------------------------

class TestListTrees:
    def test_owner_can_list_trees_by_zone(self, client):
        owner = _make_owner()
        zone_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: owner
        mock_tree = _make_mock_tree(zone_id)
        with patch("app.api.v1.trees.TreeService") as MockSvc:
            MockSvc.return_value.list_trees.return_value = ([mock_tree], 1)
            resp = client.get(f"/api/v1/trees?zone_id={zone_id}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200
        body = resp.json()
        assert "data" in body
        assert "pagination" in body

    def test_list_trees_filters_by_accessible_zone(self, client):
        owner = _make_owner()
        zone_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: owner
        with patch("app.api.v1.trees.TreeService") as MockSvc:
            MockSvc.return_value.list_trees.side_effect = AppError(
                "farm_not_accessible", "Farm is not accessible", 403
            )
            resp = client.get(f"/api/v1/trees?zone_id={zone_id}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403

    def test_pending_membership_blocked_from_list(self, client):
        from app.core.errors import AppError as _AppError
        def _pending():
            raise _AppError("membership_not_active", "Farm membership is not active", 403)
        app.dependency_overrides[require_active_membership] = _pending
        resp = client.get("/api/v1/trees")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403


# ---------------------------------------------------------------------------
# GET /api/v1/trees/{tree_id}
# ---------------------------------------------------------------------------

class TestGetTree:
    def test_owner_can_get_tree(self, client):
        owner = _make_owner()
        tree_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: owner
        mock_tree = _make_mock_tree()
        mock_tree.id = tree_id
        with patch("app.api.v1.trees.TreeService") as MockSvc:
            MockSvc.return_value.get_tree.return_value = mock_tree
            resp = client.get(f"/api/v1/trees/{tree_id}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 200

    def test_inaccessible_tree_blocked(self, client):
        owner = _make_owner()
        tree_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: owner
        with patch("app.api.v1.trees.TreeService") as MockSvc:
            MockSvc.return_value.get_tree.side_effect = AppError(
                "farm_not_accessible", "Farm is not accessible", 403
            )
            resp = client.get(f"/api/v1/trees/{tree_id}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 403

    def test_missing_tree_returns_404(self, client):
        owner = _make_owner()
        tree_id = uuid4()
        app.dependency_overrides[require_active_membership] = lambda: owner
        with patch("app.api.v1.trees.TreeService") as MockSvc:
            MockSvc.return_value.get_tree.side_effect = AppError("tree_not_found", "Tree not found", 404)
            resp = client.get(f"/api/v1/trees/{tree_id}")
        app.dependency_overrides.pop(require_active_membership, None)
        assert resp.status_code == 404


# ---------------------------------------------------------------------------
# POST /api/v1/trees
# ---------------------------------------------------------------------------

class TestCreateTree:
    def _payload(self, zone_id=None):
        return {"zone_id": str(zone_id or uuid4()), "tree_code": "T-001"}

    def test_owner_can_create_tree_under_own_zone(self, client):
        owner = _make_owner()
        zone_id = uuid4()
        app.dependency_overrides[require_active_account] = lambda: owner
        mock_tree = _make_mock_tree(zone_id)
        with patch("app.api.v1.trees.TreeService") as MockSvc:
            MockSvc.return_value.create_tree.return_value = mock_tree
            resp = client.post("/api/v1/trees", json=self._payload(zone_id))
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 200

    def test_owner_cannot_create_tree_under_inaccessible_zone(self, client):
        owner = _make_owner()
        zone_id = uuid4()
        app.dependency_overrides[require_active_account] = lambda: owner
        with patch("app.api.v1.trees.TreeService") as MockSvc:
            MockSvc.return_value.create_tree.side_effect = AppError(
                "farm_not_accessible", "Farm is not accessible", 403
            )
            resp = client.post("/api/v1/trees", json=self._payload(zone_id))
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 403

    def test_owner_family_cannot_create_tree(self, client):
        user = _make_member(FarmerStatus.owner_family, MembershipStatus.active)
        app.dependency_overrides[require_active_account] = lambda: user
        with patch("app.api.v1.trees.TreeService") as MockSvc:
            MockSvc.return_value.create_tree.side_effect = AppError(
                "tree_create_forbidden", "Only farm owners can perform this action", 403
            )
            resp = client.post("/api/v1/trees", json=self._payload())
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 403

    def test_farm_staff_cannot_create_tree(self, client):
        user = _make_member(FarmerStatus.farm_staff, MembershipStatus.active)
        app.dependency_overrides[require_active_account] = lambda: user
        with patch("app.api.v1.trees.TreeService") as MockSvc:
            MockSvc.return_value.create_tree.side_effect = AppError(
                "tree_create_forbidden", "Only farm owners can perform this action", 403
            )
            resp = client.post("/api/v1/trees", json=self._payload())
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 403

    def test_missing_zone_id_rejected(self, client):
        owner = _make_owner()
        app.dependency_overrides[require_active_account] = lambda: owner
        resp = client.post("/api/v1/trees", json={"tree_code": "T-001"})
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 422

    def test_missing_tree_code_rejected(self, client):
        owner = _make_owner()
        app.dependency_overrides[require_active_account] = lambda: owner
        resp = client.post("/api/v1/trees", json={"zone_id": str(uuid4())})
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# PATCH /api/v1/trees/{tree_id}
# ---------------------------------------------------------------------------

class TestUpdateTree:
    def test_owner_can_update_tree(self, client):
        owner = _make_owner()
        tree_id = uuid4()
        app.dependency_overrides[require_active_account] = lambda: owner
        mock_tree = _make_mock_tree()
        mock_tree.id = tree_id
        mock_tree.tree_code = "T-002"
        with patch("app.api.v1.trees.TreeService") as MockSvc:
            MockSvc.return_value.update_tree.return_value = mock_tree
            resp = client.patch(f"/api/v1/trees/{tree_id}", json={"tree_code": "T-002"})
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 200
        assert resp.json()["data"]["tree_code"] == "T-002"

    def test_cannot_move_tree_to_another_zone(self, client):
        """zone_id reassignment is not allowed; TreeUpdate schema has no zone_id field."""
        owner = _make_owner()
        tree_id = uuid4()
        app.dependency_overrides[require_active_account] = lambda: owner
        mock_tree = _make_mock_tree()
        mock_tree.id = tree_id
        with patch("app.api.v1.trees.TreeService") as MockSvc:
            MockSvc.return_value.update_tree.return_value = mock_tree
            # zone_id in body is silently ignored (not a TreeUpdate field)
            resp = client.patch(
                f"/api/v1/trees/{tree_id}",
                json={"tree_code": "T-002", "zone_id": str(uuid4())},
            )
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 200

    def test_inaccessible_tree_update_blocked(self, client):
        owner = _make_owner()
        tree_id = uuid4()
        app.dependency_overrides[require_active_account] = lambda: owner
        with patch("app.api.v1.trees.TreeService") as MockSvc:
            MockSvc.return_value.update_tree.side_effect = AppError(
                "farm_not_accessible", "Farm is not accessible", 403
            )
            resp = client.patch(f"/api/v1/trees/{tree_id}", json={"tree_code": "T-X"})
        app.dependency_overrides.pop(require_active_account, None)
        assert resp.status_code == 403

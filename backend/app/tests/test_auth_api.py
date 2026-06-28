"""P2-5: API-level tests for auth endpoints with mocked service and dependencies."""

from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.core.enums import AccountStatus, FarmerStatus, MembershipStatus, UserRole
from app.core.errors import AppError
from app.dependencies.auth import get_current_user
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


def _make_mock_user(
    farmer_status=FarmerStatus.owner,
    membership_status=MembershipStatus.active,
    account_status=AccountStatus.active_pending_verification,
    primary_farm_id=None,
):
    user = MagicMock()
    user.id = uuid4()
    user.organization_id = uuid4()
    user.phone = "0812345678"
    user.name = "Somchai"
    user.role = UserRole.farmer
    user.farmer_status = farmer_status
    user.membership_status = membership_status
    user.account_status = account_status
    user.primary_farm_id = primary_farm_id
    return user


# ---------------------------------------------------------------------------
# POST /api/v1/auth/register
# ---------------------------------------------------------------------------

class TestRegisterEndpoint:
    _OWNER_PAYLOAD = {
        "phone": "0812345678",
        "name": "Somchai",
        "password": "1234",
        "farmer_status": "owner",
    }

    def test_register_owner_returns_200(self, client):
        user = _make_mock_user()
        with patch("app.api.v1.auth.AuthService") as MockSvc:
            MockSvc.return_value.register.return_value = (user, "access_tok", "refresh_tok")
            resp = client.post("/api/v1/auth/register", json=self._OWNER_PAYLOAD)
        assert resp.status_code == 200

    def test_register_owner_response_has_tokens(self, client):
        user = _make_mock_user()
        with patch("app.api.v1.auth.AuthService") as MockSvc:
            MockSvc.return_value.register.return_value = (user, "access_tok", "refresh_tok")
            resp = client.post("/api/v1/auth/register", json=self._OWNER_PAYLOAD)
        data = resp.json()["data"]
        assert data["access_token"] == "access_tok"
        assert data["refresh_token"] == "refresh_tok"

    def test_register_owner_response_has_farmer_status(self, client):
        user = _make_mock_user()
        with patch("app.api.v1.auth.AuthService") as MockSvc:
            MockSvc.return_value.register.return_value = (user, "a", "r")
            resp = client.post("/api/v1/auth/register", json=self._OWNER_PAYLOAD)
        data = resp.json()["data"]
        assert data["farmer_status"] == "owner"

    def test_register_owner_response_has_account_status(self, client):
        user = _make_mock_user()
        with patch("app.api.v1.auth.AuthService") as MockSvc:
            MockSvc.return_value.register.return_value = (user, "a", "r")
            resp = client.post("/api/v1/auth/register", json=self._OWNER_PAYLOAD)
        data = resp.json()["data"]
        assert data["account_status"] == "active_pending_verification"

    def test_register_owner_response_has_organization_id(self, client):
        user = _make_mock_user()
        with patch("app.api.v1.auth.AuthService") as MockSvc:
            MockSvc.return_value.register.return_value = (user, "a", "r")
            resp = client.post("/api/v1/auth/register", json=self._OWNER_PAYLOAD)
        data = resp.json()["data"]
        assert "organization_id" in data

    def test_register_duplicate_phone_returns_409(self, client):
        with patch("app.api.v1.auth.AuthService") as MockSvc:
            MockSvc.return_value.register.side_effect = AppError("phone_conflict", "Phone already registered", 409)
            resp = client.post("/api/v1/auth/register", json=self._OWNER_PAYLOAD)
        assert resp.status_code == 409

    def test_register_owner_family_missing_farm_id_returns_422(self, client):
        with patch("app.api.v1.auth.AuthService") as MockSvc:
            MockSvc.return_value.register.side_effect = AppError("farm_id_required", "farm_id required", 422)
            resp = client.post("/api/v1/auth/register", json={
                "phone": "0819999999", "name": "Worker",
                "password": "1234", "farmer_status": "owner_family",
            })
        assert resp.status_code == 422

    def test_register_farm_staff_invalid_farm_id_returns_404(self, client):
        with patch("app.api.v1.auth.AuthService") as MockSvc:
            MockSvc.return_value.register.side_effect = AppError("farm_not_found", "Farm not found", 404)
            resp = client.post("/api/v1/auth/register", json={
                "phone": "0819999999", "name": "Worker", "password": "1234",
                "farmer_status": "farm_staff", "farm_id": str(uuid4()),
            })
        assert resp.status_code == 404

    def test_register_owner_family_response_has_membership_status(self, client):
        farm_id = uuid4()
        user = _make_mock_user(
            farmer_status=FarmerStatus.owner_family,
            membership_status=MembershipStatus.pending_farm_approval,
            account_status=AccountStatus.active,
            primary_farm_id=farm_id,
        )
        with patch("app.api.v1.auth.AuthService") as MockSvc:
            MockSvc.return_value.register.return_value = (user, "a", "r")
            resp = client.post("/api/v1/auth/register", json={
                "phone": "0819999999", "name": "Worker", "password": "1234",
                "farmer_status": "owner_family", "farm_id": str(farm_id),
            })
        data = resp.json()["data"]
        assert data["membership_status"] == "pending_farm_approval"
        assert data["primary_farm_id"] == str(farm_id)

    def test_register_missing_required_field_returns_422(self, client):
        resp = client.post("/api/v1/auth/register", json={"phone": "0812345678"})
        assert resp.status_code == 422


# ---------------------------------------------------------------------------
# POST /api/v1/auth/login
# ---------------------------------------------------------------------------

class TestLoginEndpoint:
    _PAYLOAD = {"phone": "0812345678", "password": "1234"}

    def test_login_success_returns_200(self, client):
        with patch("app.api.v1.auth.AuthService") as MockSvc:
            MockSvc.return_value.login.return_value = ("access_tok", "refresh_tok")
            resp = client.post("/api/v1/auth/login", json=self._PAYLOAD)
        assert resp.status_code == 200

    def test_login_success_returns_tokens(self, client):
        with patch("app.api.v1.auth.AuthService") as MockSvc:
            MockSvc.return_value.login.return_value = ("access_tok", "refresh_tok")
            resp = client.post("/api/v1/auth/login", json=self._PAYLOAD)
        data = resp.json()["data"]
        assert data["access_token"] == "access_tok"
        assert data["refresh_token"] == "refresh_tok"
        assert data["token_type"] == "bearer"

    def test_login_wrong_password_returns_401(self, client):
        with patch("app.api.v1.auth.AuthService") as MockSvc:
            MockSvc.return_value.login.side_effect = AppError("invalid_credentials", "Bad credentials", 401)
            resp = client.post("/api/v1/auth/login", json=self._PAYLOAD)
        assert resp.status_code == 401

    def test_login_unknown_phone_returns_401(self, client):
        with patch("app.api.v1.auth.AuthService") as MockSvc:
            MockSvc.return_value.login.side_effect = AppError("invalid_credentials", "Bad credentials", 401)
            resp = client.post("/api/v1/auth/login", json={"phone": "0800000000", "password": "x"})
        assert resp.status_code == 401


# ---------------------------------------------------------------------------
# POST /api/v1/auth/refresh
# ---------------------------------------------------------------------------

class TestRefreshEndpoint:
    def test_refresh_returns_200(self, client):
        with patch("app.api.v1.auth.AuthService") as MockSvc:
            MockSvc.return_value.refresh.return_value = "new_access_token"
            resp = client.post("/api/v1/auth/refresh", json={"refresh_token": "some_token"})
        assert resp.status_code == 200

    def test_refresh_response_has_access_token(self, client):
        with patch("app.api.v1.auth.AuthService") as MockSvc:
            MockSvc.return_value.refresh.return_value = "new_access_token"
            resp = client.post("/api/v1/auth/refresh", json={"refresh_token": "some_token"})
        data = resp.json()["data"]
        assert data["access_token"] == "new_access_token"
        assert data["token_type"] == "bearer"
        assert "expires_in" in data

    def test_refresh_invalid_token_returns_401(self, client):
        with patch("app.api.v1.auth.AuthService") as MockSvc:
            MockSvc.return_value.refresh.side_effect = AppError("invalid_token", "Bad token", 401)
            resp = client.post("/api/v1/auth/refresh", json={"refresh_token": "bad_token"})
        assert resp.status_code == 401


# ---------------------------------------------------------------------------
# GET /api/v1/auth/me
# ---------------------------------------------------------------------------

class TestMeEndpoint:
    def test_me_returns_200(self, client):
        user = _make_mock_user()
        app.dependency_overrides[get_current_user] = lambda: user
        try:
            resp = client.get("/api/v1/auth/me")
        finally:
            app.dependency_overrides.pop(get_current_user, None)
        assert resp.status_code == 200

    def test_me_returns_farmer_status(self, client):
        user = _make_mock_user()
        app.dependency_overrides[get_current_user] = lambda: user
        try:
            resp = client.get("/api/v1/auth/me")
        finally:
            app.dependency_overrides.pop(get_current_user, None)
        data = resp.json()["data"]
        assert data["farmer_status"] == "owner"

    def test_me_returns_membership_status(self, client):
        user = _make_mock_user(membership_status=MembershipStatus.active)
        app.dependency_overrides[get_current_user] = lambda: user
        try:
            resp = client.get("/api/v1/auth/me")
        finally:
            app.dependency_overrides.pop(get_current_user, None)
        data = resp.json()["data"]
        assert data["membership_status"] == "active"

    def test_me_returns_account_status(self, client):
        user = _make_mock_user()
        app.dependency_overrides[get_current_user] = lambda: user
        try:
            resp = client.get("/api/v1/auth/me")
        finally:
            app.dependency_overrides.pop(get_current_user, None)
        data = resp.json()["data"]
        assert data["account_status"] == "active_pending_verification"

    def test_me_returns_primary_farm_id(self, client):
        farm_id = uuid4()
        user = _make_mock_user(
            farmer_status=FarmerStatus.owner_family,
            membership_status=MembershipStatus.pending_farm_approval,
            account_status=AccountStatus.active,
            primary_farm_id=farm_id,
        )
        app.dependency_overrides[get_current_user] = lambda: user
        try:
            resp = client.get("/api/v1/auth/me")
        finally:
            app.dependency_overrides.pop(get_current_user, None)
        data = resp.json()["data"]
        assert data["primary_farm_id"] == str(farm_id)

    def test_me_returns_all_onboarding_fields(self, client):
        user = _make_mock_user()
        app.dependency_overrides[get_current_user] = lambda: user
        try:
            resp = client.get("/api/v1/auth/me")
        finally:
            app.dependency_overrides.pop(get_current_user, None)
        data = resp.json()["data"]
        for field in ("farmer_status", "membership_status", "account_status", "primary_farm_id"):
            assert field in data, f"Missing field in /me response: {field}"

    def test_me_no_token_returns_401_or_403(self, client):
        # Without an Authorization header HTTPBearer rejects the request (401 or 403 depending on version)
        resp = client.get("/api/v1/auth/me")
        assert resp.status_code in (401, 403)


# ---------------------------------------------------------------------------
# POST /api/v1/auth/logout
# ---------------------------------------------------------------------------

class TestLogoutEndpoint:
    def test_logout_returns_200(self, client):
        user = _make_mock_user()
        app.dependency_overrides[get_current_user] = lambda: user
        try:
            resp = client.post("/api/v1/auth/logout")
        finally:
            app.dependency_overrides.pop(get_current_user, None)
        assert resp.status_code == 200

    def test_logout_returns_success_true(self, client):
        user = _make_mock_user()
        app.dependency_overrides[get_current_user] = lambda: user
        try:
            resp = client.post("/api/v1/auth/logout")
        finally:
            app.dependency_overrides.pop(get_current_user, None)
        assert resp.json()["data"]["success"] is True

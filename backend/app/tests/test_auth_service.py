"""P2-5: service-level unit tests for AuthService with mocked repository."""

from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from app.core.enums import AccountStatus, FarmerStatus, MembershipStatus, UserRole
from app.core.errors import AppError
from app.schemas.auth import RegisterRequest
from app.services.auth import AuthService


def _make_mock_user(
    farmer_status=FarmerStatus.owner,
    membership_status=MembershipStatus.active,
    account_status=AccountStatus.active_pending_verification,
    primary_farm_id=None,
    phone="0812345678",
    role=UserRole.farmer,
):
    user = MagicMock()
    user.id = uuid4()
    user.organization_id = uuid4()
    user.phone = phone
    user.name = "Test User"
    user.role = role
    user.farmer_status = farmer_status
    user.membership_status = membership_status
    user.account_status = account_status
    user.primary_farm_id = primary_farm_id
    user.password_hash = "$2b$12$fakehash"
    return user


def _make_mock_org():
    org = MagicMock()
    org.id = uuid4()
    return org


def _make_mock_farm(org_id=None):
    farm = MagicMock()
    farm.id = uuid4()
    farm.organization_id = org_id or uuid4()
    return farm


def _make_service_with_mock_repo(db=None):
    if db is None:
        db = MagicMock()
    svc = AuthService(db)
    svc.repo = MagicMock()
    return svc


class TestRegisterOwner:
    def test_register_owner_success(self):
        svc = _make_service_with_mock_repo()
        org = _make_mock_org()
        user = _make_mock_user()

        svc.repo.get_by_phone.return_value = None
        svc.repo.create_organization.return_value = org
        svc.repo.create_user.return_value = user

        req = RegisterRequest(phone="0812345678", name="Test", password="1234", farmer_status=FarmerStatus.owner)
        result_user, access_token, refresh_token = svc.register(req)

        assert result_user is user
        assert isinstance(access_token, str)
        assert isinstance(refresh_token, str)
        svc.repo.create_organization.assert_called_once()
        svc.repo.create_user.assert_called_once()

    def test_register_owner_sets_membership_status_active(self):
        svc = _make_service_with_mock_repo()
        org = _make_mock_org()
        user = _make_mock_user(membership_status=MembershipStatus.active)

        svc.repo.get_by_phone.return_value = None
        svc.repo.create_organization.return_value = org
        svc.repo.create_user.return_value = user

        req = RegisterRequest(phone="0812345678", name="Test", password="1234", farmer_status=FarmerStatus.owner)
        result_user, _, _ = svc.register(req)

        call_kwargs = svc.repo.create_user.call_args.kwargs
        assert call_kwargs["membership_status"] == MembershipStatus.active

    def test_register_owner_sets_account_status_active_pending_verification(self):
        svc = _make_service_with_mock_repo()
        org = _make_mock_org()
        user = _make_mock_user()

        svc.repo.get_by_phone.return_value = None
        svc.repo.create_organization.return_value = org
        svc.repo.create_user.return_value = user

        req = RegisterRequest(phone="0812345678", name="Test", password="1234", farmer_status=FarmerStatus.owner)
        svc.register(req)

        call_kwargs = svc.repo.create_user.call_args.kwargs
        assert call_kwargs["account_status"] == AccountStatus.active_pending_verification

    def test_register_owner_creates_organization(self):
        svc = _make_service_with_mock_repo()
        org = _make_mock_org()
        user = _make_mock_user()

        svc.repo.get_by_phone.return_value = None
        svc.repo.create_organization.return_value = org
        svc.repo.create_user.return_value = user

        req = RegisterRequest(phone="0812345678", name="Somchai", password="1234", farmer_status=FarmerStatus.owner)
        svc.register(req)

        svc.repo.create_organization.assert_called_once_with(name="Somchai")

    def test_register_owner_assigns_role_farmer(self):
        svc = _make_service_with_mock_repo()
        org = _make_mock_org()
        user = _make_mock_user()

        svc.repo.get_by_phone.return_value = None
        svc.repo.create_organization.return_value = org
        svc.repo.create_user.return_value = user

        req = RegisterRequest(phone="0812345678", name="Test", password="1234", farmer_status=FarmerStatus.owner)
        svc.register(req)

        call_kwargs = svc.repo.create_user.call_args.kwargs
        assert call_kwargs["role"] == UserRole.farmer

    def test_register_owner_primary_farm_id_is_none(self):
        svc = _make_service_with_mock_repo()
        org = _make_mock_org()
        user = _make_mock_user(primary_farm_id=None)

        svc.repo.get_by_phone.return_value = None
        svc.repo.create_organization.return_value = org
        svc.repo.create_user.return_value = user

        req = RegisterRequest(phone="0812345678", name="Test", password="1234", farmer_status=FarmerStatus.owner)
        svc.register(req)

        call_kwargs = svc.repo.create_user.call_args.kwargs
        assert call_kwargs["primary_farm_id"] is None

    def test_register_duplicate_phone_raises_conflict(self):
        svc = _make_service_with_mock_repo()
        existing = _make_mock_user()
        svc.repo.get_by_phone.return_value = existing

        req = RegisterRequest(phone="0812345678", name="Test", password="1234", farmer_status=FarmerStatus.owner)
        with pytest.raises(AppError) as exc_info:
            svc.register(req)
        assert exc_info.value.status_code == 409

    def test_phone_is_normalized_before_lookup(self):
        svc = _make_service_with_mock_repo()
        org = _make_mock_org()
        user = _make_mock_user()

        svc.repo.get_by_phone.return_value = None
        svc.repo.create_organization.return_value = org
        svc.repo.create_user.return_value = user

        req = RegisterRequest(phone="081 234 5678", name="Test", password="1234", farmer_status=FarmerStatus.owner)
        svc.register(req)

        svc.repo.get_by_phone.assert_called_once_with("0812345678")


class TestRegisterOwnerFamilyAndFarmStaff:
    def _register_member(self, farmer_status: FarmerStatus, farm_id=None):
        svc = _make_service_with_mock_repo()
        farm = _make_mock_farm()
        user = _make_mock_user(
            farmer_status=farmer_status,
            membership_status=MembershipStatus.pending_farm_approval,
            account_status=AccountStatus.active,
            primary_farm_id=farm.id,
        )

        svc.repo.get_by_phone.return_value = None
        svc.repo.get_farm_by_id.return_value = farm
        svc.repo.create_user.return_value = user

        req = RegisterRequest(
            phone="0819999999",
            name="Worker",
            password="1234",
            farmer_status=farmer_status,
            farm_id=farm_id or farm.id,
        )
        return svc, farm, req

    def test_register_owner_family_success(self):
        svc, farm, req = self._register_member(FarmerStatus.owner_family)
        user, at, rt = svc.register(req)
        assert isinstance(at, str)
        svc.repo.create_user.assert_called_once()

    def test_register_farm_staff_success(self):
        svc, farm, req = self._register_member(FarmerStatus.farm_staff)
        user, at, rt = svc.register(req)
        assert isinstance(at, str)
        svc.repo.create_user.assert_called_once()

    def test_owner_family_sets_membership_pending_farm_approval(self):
        svc, farm, req = self._register_member(FarmerStatus.owner_family)
        svc.register(req)
        call_kwargs = svc.repo.create_user.call_args.kwargs
        assert call_kwargs["membership_status"] == MembershipStatus.pending_farm_approval

    def test_owner_family_sets_account_status_active(self):
        svc, farm, req = self._register_member(FarmerStatus.owner_family)
        svc.register(req)
        call_kwargs = svc.repo.create_user.call_args.kwargs
        assert call_kwargs["account_status"] == AccountStatus.active

    def test_owner_family_sets_primary_farm_id(self):
        svc, farm, req = self._register_member(FarmerStatus.owner_family)
        svc.register(req)
        call_kwargs = svc.repo.create_user.call_args.kwargs
        assert call_kwargs["primary_farm_id"] == farm.id

    def test_owner_family_resolves_organization_id_from_farm(self):
        svc, farm, req = self._register_member(FarmerStatus.owner_family)
        svc.register(req)
        call_kwargs = svc.repo.create_user.call_args.kwargs
        assert call_kwargs["organization_id"] == farm.organization_id

    def test_farm_staff_sets_membership_pending_farm_approval(self):
        svc, farm, req = self._register_member(FarmerStatus.farm_staff)
        svc.register(req)
        call_kwargs = svc.repo.create_user.call_args.kwargs
        assert call_kwargs["membership_status"] == MembershipStatus.pending_farm_approval

    def test_farm_staff_sets_primary_farm_id(self):
        svc, farm, req = self._register_member(FarmerStatus.farm_staff)
        svc.register(req)
        call_kwargs = svc.repo.create_user.call_args.kwargs
        assert call_kwargs["primary_farm_id"] == farm.id

    def test_missing_farm_id_raises_422(self):
        svc = _make_service_with_mock_repo()
        svc.repo.get_by_phone.return_value = None

        req = RegisterRequest(
            phone="0819999999", name="Worker", password="1234",
            farmer_status=FarmerStatus.owner_family, farm_id=None
        )
        with pytest.raises(AppError) as exc_info:
            svc.register(req)
        assert exc_info.value.status_code == 422

    def test_invalid_farm_id_raises_404(self):
        svc = _make_service_with_mock_repo()
        svc.repo.get_by_phone.return_value = None
        svc.repo.get_farm_by_id.return_value = None

        req = RegisterRequest(
            phone="0819999999", name="Worker", password="1234",
            farmer_status=FarmerStatus.farm_staff, farm_id=uuid4()
        )
        with pytest.raises(AppError) as exc_info:
            svc.register(req)
        assert exc_info.value.status_code == 404

    def test_no_new_org_created_for_owner_family(self):
        svc, farm, req = self._register_member(FarmerStatus.owner_family)
        svc.register(req)
        svc.repo.create_organization.assert_not_called()


class TestLogin:
    def test_login_success(self):
        from app.core.security import hash_password

        svc = _make_service_with_mock_repo()
        user = _make_mock_user()
        user.password_hash = hash_password("correct_pass")

        svc.repo.get_by_phone.return_value = user

        access_token, refresh_token = svc.login("0812345678", "correct_pass")
        assert isinstance(access_token, str)
        assert isinstance(refresh_token, str)

    def test_login_wrong_password_raises_401(self):
        from app.core.security import hash_password

        svc = _make_service_with_mock_repo()
        user = _make_mock_user()
        user.password_hash = hash_password("correct_pass")

        svc.repo.get_by_phone.return_value = user

        with pytest.raises(AppError) as exc_info:
            svc.login("0812345678", "wrong_pass")
        assert exc_info.value.status_code == 401

    def test_login_unknown_phone_raises_401(self):
        svc = _make_service_with_mock_repo()
        svc.repo.get_by_phone.return_value = None

        with pytest.raises(AppError) as exc_info:
            svc.login("0800000000", "any_pass")
        assert exc_info.value.status_code == 401

    def test_login_normalizes_phone(self):
        from app.core.security import hash_password

        svc = _make_service_with_mock_repo()
        user = _make_mock_user()
        user.password_hash = hash_password("pass")

        svc.repo.get_by_phone.return_value = user

        svc.login("081 234 5678", "pass")
        svc.repo.get_by_phone.assert_called_once_with("0812345678")


class TestRefresh:
    def test_refresh_valid_token_returns_new_access_token(self):
        from app.core.security import create_refresh_token

        svc = _make_service_with_mock_repo()
        user = _make_mock_user()
        svc.repo.get_by_id.return_value = user

        refresh_token = create_refresh_token(str(user.id))
        new_access = svc.refresh(refresh_token)

        assert isinstance(new_access, str)
        assert len(new_access) > 0

    def test_refresh_invalid_token_raises_401(self):
        svc = _make_service_with_mock_repo()

        with pytest.raises(AppError) as exc_info:
            svc.refresh("not.a.real.token")
        assert exc_info.value.status_code == 401

    def test_refresh_with_access_token_raises_401(self):
        from app.core.security import create_access_token

        svc = _make_service_with_mock_repo()
        access_token = create_access_token("uid", "org", "farmer")

        with pytest.raises(AppError) as exc_info:
            svc.refresh(access_token)
        assert exc_info.value.status_code == 401

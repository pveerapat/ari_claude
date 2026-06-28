"""P2-7: Unit tests for NotebookService."""
from unittest.mock import MagicMock, patch
from uuid import uuid4

import pytest

from app.core.enums import EntryContext, EntryType, FarmerStatus, MembershipStatus, UserRole
from app.core.errors import AppError
from app.services.notebook_service import NotebookService


def _make_user(org_id=None, role=UserRole.farmer):
    user = MagicMock()
    user.id = uuid4()
    user.organization_id = org_id or uuid4()
    user.role = role
    user.farmer_status = FarmerStatus.owner
    user.membership_status = MembershipStatus.active
    return user


def _make_entry(org_id=None, entry_id=None, user_id=None):
    entry = MagicMock()
    entry.id = entry_id or uuid4()
    entry.organization_id = org_id or uuid4()
    entry.created_by_user_id = user_id or uuid4()
    entry.farm_id = None
    entry.zone_id = None
    entry.tree_id = None
    entry.entry_type = EntryType.note
    entry.entry_context = EntryContext.general_note
    entry.title = None
    entry.summary = None
    entry.analysis_status = "not_started"
    entry.external_ai = None
    entry.ai_usefulness_status = None
    entry.learned_summary = None
    entry.suggested_category = None
    return entry


def _make_create_req(org_id=None):
    req = MagicMock()
    req.organization_id = org_id or uuid4()
    req.farm_id = None
    req.zone_id = None
    req.tree_id = None
    req.entry_type = EntryType.note
    req.entry_context = EntryContext.general_note
    req.title = None
    req.summary = None
    req.analysis_status = "not_started"
    req.ai_provider = None
    req.ai_usefulness_status = None
    req.learned_summary = None
    return req


class TestNotebookServiceHierarchyValidation:
    def test_farm_in_different_org_blocked(self):
        db = MagicMock()
        svc = NotebookService(db)
        user = _make_user()
        req = _make_create_req(org_id=user.organization_id)
        req.farm_id = uuid4()

        mock_farm = MagicMock()
        mock_farm.organization_id = uuid4()
        svc.farm_repo.get_by_id = MagicMock(return_value=mock_farm)

        with pytest.raises(AppError) as exc_info:
            svc.create_entry(user, req)
        assert exc_info.value.status_code == 403
        assert "farm" in exc_info.value.code

    def test_zone_without_farm_id_blocked(self):
        db = MagicMock()
        svc = NotebookService(db)
        user = _make_user()
        req = _make_create_req(org_id=user.organization_id)
        req.zone_id = uuid4()

        with pytest.raises(AppError) as exc_info:
            svc.create_entry(user, req)
        assert exc_info.value.status_code == 422
        assert "farm_id" in exc_info.value.code

    def test_tree_without_zone_id_blocked(self):
        db = MagicMock()
        svc = NotebookService(db)
        user = _make_user()
        req = _make_create_req(org_id=user.organization_id)
        req.farm_id = uuid4()
        req.tree_id = uuid4()

        mock_farm = MagicMock()
        mock_farm.organization_id = user.organization_id
        svc.farm_repo.get_by_id = MagicMock(return_value=mock_farm)

        with pytest.raises(AppError) as exc_info:
            svc.create_entry(user, req)
        assert exc_info.value.status_code == 422
        assert "zone_id" in exc_info.value.code

    def test_cross_org_access_blocked(self):
        db = MagicMock()
        svc = NotebookService(db)
        user = _make_user()
        req = _make_create_req(org_id=uuid4())

        with pytest.raises(AppError) as exc_info:
            svc.create_entry(user, req)
        assert exc_info.value.status_code == 403

    def test_nullable_farm_zone_tree_allowed(self):
        db = MagicMock()
        svc = NotebookService(db)
        user = _make_user()
        req = _make_create_req(org_id=user.organization_id)
        req.farm_id = None
        req.zone_id = None
        req.tree_id = None

        entry = _make_entry(org_id=user.organization_id)
        svc.repo.create = MagicMock(return_value=entry)
        db.commit = MagicMock()
        db.refresh = MagicMock()

        result = svc.create_entry(user, req)
        assert result is not None
        svc.repo.create.assert_called_once()

    def test_zone_not_in_farm_blocked(self):
        db = MagicMock()
        svc = NotebookService(db)
        user = _make_user()
        farm_id = uuid4()
        zone_id = uuid4()
        req = _make_create_req(org_id=user.organization_id)
        req.farm_id = farm_id
        req.zone_id = zone_id

        mock_farm = MagicMock()
        mock_farm.organization_id = user.organization_id
        svc.farm_repo.get_by_id = MagicMock(return_value=mock_farm)

        mock_zone = MagicMock()
        mock_zone.farm_id = uuid4()
        svc.zone_repo.get_by_id = MagicMock(return_value=mock_zone)

        with pytest.raises(AppError) as exc_info:
            svc.create_entry(user, req)
        assert exc_info.value.status_code == 403


class TestNotebookServiceGetEntry:
    def test_entry_not_found_raises_404(self):
        db = MagicMock()
        svc = NotebookService(db)
        user = _make_user()
        svc.repo.get_by_id = MagicMock(return_value=None)

        with pytest.raises(AppError) as exc_info:
            svc.get_entry(user, uuid4())
        assert exc_info.value.status_code == 404

    def test_cross_org_access_blocked(self):
        db = MagicMock()
        svc = NotebookService(db)
        user = _make_user()
        entry = _make_entry(org_id=uuid4())
        svc.repo.get_by_id = MagicMock(return_value=entry)

        with pytest.raises(AppError) as exc_info:
            svc.get_entry(user, entry.id)
        assert exc_info.value.status_code == 403

    def test_privileged_user_can_access_any_org(self):
        db = MagicMock()
        svc = NotebookService(db)
        admin = _make_user(role=UserRole.admin)
        entry = _make_entry(org_id=uuid4())
        svc.repo.get_by_id = MagicMock(return_value=entry)

        result = svc.get_entry(admin, entry.id)
        assert result == entry

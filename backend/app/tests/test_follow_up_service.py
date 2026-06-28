"""P2-7: Unit tests for FollowUpService."""
from unittest.mock import MagicMock
from uuid import uuid4

import pytest

from app.core.enums import EntryContext, EntryType, FarmerStatus, MembershipStatus, UserRole
from app.core.errors import AppError
from app.services.follow_up_service import FollowUpService


def _make_user(org_id=None):
    user = MagicMock()
    user.id = uuid4()
    user.organization_id = org_id or uuid4()
    user.role = UserRole.farmer
    user.farmer_status = FarmerStatus.owner
    user.membership_status = MembershipStatus.active
    return user


def _make_entry(org_id=None):
    entry = MagicMock()
    entry.id = uuid4()
    entry.organization_id = org_id or uuid4()
    return entry


def _make_create_req(entry_id=None, day=7):
    req = MagicMock()
    req.entry_id = entry_id or uuid4()
    req.follow_up_day = day
    return req


def _make_update_req(outcome=None, notes=None):
    req = MagicMock()
    req.outcome = outcome
    req.notes = notes
    req.model_fields_set = set()
    if outcome is not None:
        req.model_fields_set.add("outcome")
    if notes is not None:
        req.model_fields_set.add("notes")
    return req


class TestFollowUpValidation:
    def test_valid_follow_up_days(self):
        db = MagicMock()
        svc = FollowUpService(db)
        user = _make_user()
        for day in [3, 7, 14]:
            entry = _make_entry(org_id=user.organization_id)
            svc.entry_repo.get_by_id = MagicMock(return_value=entry)
            req = _make_create_req(entry_id=entry.id, day=day)

            fu = MagicMock()
            fu.id = uuid4()
            fu.entry_id = entry.id
            fu.follow_up_day = day
            svc.repo.create = MagicMock(return_value=fu)
            db.commit = MagicMock()
            db.refresh = MagicMock()

            result = svc.create_follow_up(user, req)
            assert result.follow_up_day == day

    def test_invalid_follow_up_day_5_blocked(self):
        db = MagicMock()
        svc = FollowUpService(db)
        user = _make_user()
        entry = _make_entry(org_id=user.organization_id)
        svc.entry_repo.get_by_id = MagicMock(return_value=entry)
        req = _make_create_req(entry_id=entry.id, day=5)

        with pytest.raises(AppError) as exc_info:
            svc.create_follow_up(user, req)
        assert exc_info.value.status_code == 422

    def test_entry_not_found_blocks_create(self):
        db = MagicMock()
        svc = FollowUpService(db)
        user = _make_user()
        svc.entry_repo.get_by_id = MagicMock(return_value=None)
        req = _make_create_req()

        with pytest.raises(AppError) as exc_info:
            svc.create_follow_up(user, req)
        assert exc_info.value.status_code == 404

    def test_cross_org_entry_blocks_follow_up(self):
        db = MagicMock()
        svc = FollowUpService(db)
        user = _make_user()
        entry = _make_entry(org_id=uuid4())
        svc.entry_repo.get_by_id = MagicMock(return_value=entry)
        req = _make_create_req(entry_id=entry.id)

        with pytest.raises(AppError) as exc_info:
            svc.create_follow_up(user, req)
        assert exc_info.value.status_code == 403

    def test_get_follow_up_not_found(self):
        db = MagicMock()
        svc = FollowUpService(db)
        user = _make_user()
        svc.repo.get_by_id = MagicMock(return_value=None)

        with pytest.raises(AppError) as exc_info:
            svc.get_follow_up(user, uuid4())
        assert exc_info.value.status_code == 404

    def test_update_outcome_and_notes(self):
        db = MagicMock()
        svc = FollowUpService(db)
        user = _make_user()

        entry = _make_entry(org_id=user.organization_id)
        fu = MagicMock()
        fu.id = uuid4()
        fu.entry_id = entry.id
        fu.follow_up_day = 7
        fu.outcome = None
        fu.notes = None

        svc.repo.get_by_id = MagicMock(return_value=fu)
        svc.entry_repo.get_by_id = MagicMock(return_value=entry)

        from app.core.enums import FollowUpOutcome
        req = _make_update_req(outcome=FollowUpOutcome.improved, notes="Getting better")

        updated_fu = MagicMock()
        updated_fu.outcome = FollowUpOutcome.improved
        updated_fu.notes = "Getting better"
        svc.repo.update = MagicMock(return_value=updated_fu)
        db.commit = MagicMock()
        db.refresh = MagicMock()

        result = svc.update_follow_up(user, fu.id, req)
        assert result.outcome == FollowUpOutcome.improved
